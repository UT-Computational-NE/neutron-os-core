"""Full-screen chat TUI — fixed bottom input with scrollable output.

Replaces the sequential print-based REPL with a prompt_toolkit Application
using a split layout:

    ┌─────────────────────────────────────┐
    │  Output (scrollable, styled)        │  Buffer + BufferControl + Lexer
    │  you> Hey there.                    │
    │  Hello! I'm neut...                 │
    │  · Thinking… (3s · esc to cancel)   │  ConditionalContainer
    │     claude-sonnet · 245in/1840out   │  FormattedTextControl (status, right)
    │  ─────────────────────────────────  │  FormattedTextControl (border)
    │  you> [cursor here]                 │  Buffer + BufferControl + BeforeInput
    │  ─────────────────────────────────  │  FormattedTextControl (border)
    │  >> ask mode  (shift+tab)  · ctrl+d │  FormattedTextControl (toolbar)
    └─────────────────────────────────────┘

Threading model:
    Main thread  — prompt_toolkit event loop (app.run())
    Agent thread — agent.turn() in daemon Thread
    Spinner      — animates FormattedText at 60ms, calls app.invalidate()
    Approval     — agent thread blocks on Event; main thread unblocks
"""

from __future__ import annotations

import os
import re
import textwrap
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Iterator, Optional, TYPE_CHECKING

from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.filters import Condition
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding import KeyBindings, ConditionalKeyBindings, merge_key_bindings
from prompt_toolkit.layout.containers import (
    ConditionalContainer,
    HSplit,
    Window,
)
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.dimension import Dimension as D
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.processors import BeforeInput, Processor, Transformation
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles import Style

from tools.agents.chat.providers.base import RenderProvider
from tools.agents.chat.pulse_spinner import (
    PULSE_FRAMES,
    _FRAME_INTERVAL,
    _format_elapsed,
    _format_tokens,
)

if TYPE_CHECKING:
    from tools.agents.chat.agent import ChatAgent
    from tools.agents.orchestrator.actions import Action
    from tools.agents.orchestrator.session import SessionStore
    from tools.agents.sense.gateway import StreamChunk


# ---------------------------------------------------------------------------
# Color theme — matches Cherenkov blue brand from setup/renderer.py
# ---------------------------------------------------------------------------

_CHERENKOV = "#00cfff"

_CHERENKOV_DIM = "#009fcc"  # Slightly muted Cherenkov for secondary elements

_STYLE = Style.from_dict({
    # Markdown in output
    "md.heading":      f"{_CHERENKOV} bold",
    "md.bold":         "bold",
    "md.code":         _CHERENKOV_DIM,
    "md.list-bullet":  _CHERENKOV_DIM,
    "md.blockquote":   "#6c6c6c italic",
    # Semantic lines
    "dim":             "#6c6c6c",
    "user-prefix":     f"{_CHERENKOV} bold",
    "success":         "#5faf5f",
    "error":           "#d75f5f",
    "warning":         "#d7af5f",
    "welcome":         f"{_CHERENKOV} bold",
    "gateway.ok":      "#5faf5f",
    "gateway.stub":    "#d7af5f",
    "slash-cmd":       _CHERENKOV_DIM,
    # UI chrome
    "border":          "#6c6c6c",
    "prompt":          f"{_CHERENKOV} bold",
    "toolbar.arrow":   _CHERENKOV,
    "toolbar.mode":    f"{_CHERENKOV} bold",
    "toolbar.dim":     "#6c6c6c",
    "toolbar.approval": "#d7af5f",
    "status":          "#6c6c6c",
    "spinner.detail":  "#6c6c6c",
    "placeholder":     "#585858 italic",
    # Tables
    "table.pipe":      _CHERENKOV_DIM,
    "table.header":    f"{_CHERENKOV_DIM} bold",
    "table.separator": "#6c6c6c",
    # Mermaid / diagrams
    "diagram.label":   f"{_CHERENKOV} bold",
    "diagram.code":    "#7a9cc7",
    "diagram.keyword": f"#7a9cc7 bold",
    # Session picker
    "picker.header":   f"{_CHERENKOV} bold",
    "picker.cursor":   f"{_CHERENKOV} bold",
    "picker.check":    "#5faf5f bold",
    "picker.uncheck":  "#6c6c6c",
    "picker.sid":      _CHERENKOV_DIM,
    "picker.meta":     "#6c6c6c",
})


# ---------------------------------------------------------------------------
# Output lexer — styles each line of the output buffer
# ---------------------------------------------------------------------------

_RE_HEADING = re.compile(r"^(\s*)(#{1,3})\s+(.+)$")
_RE_BOLD = re.compile(r"\*\*(.+?)\*\*")
_RE_CODE = re.compile(r"`([^`]+)`")
_RE_LIST = re.compile(r"^(\s*)[-*]\s+(.+)$")
_RE_ORDERED = re.compile(r"^(\s*)\d+\.\s+(.+)$")
_RE_STATUS = re.compile(r"^\s+\S.*\d+in/\d+out")
_RE_SLASH = re.compile(r"^(\s+)(/\w+)(\s+.*)$")
_RE_TABLE_ROW = re.compile(r"^(\s*)\|(.+)\|\s*$")
_RE_TABLE_SEP = re.compile(r"^(\s*)\|[\s:]*-[-\s:|]*\|\s*$")

# Mermaid keywords for syntax highlighting
_MERMAID_KEYWORDS = {
    "graph", "subgraph", "end", "flowchart", "sequenceDiagram",
    "classDiagram", "stateDiagram", "erDiagram", "gantt", "pie",
    "gitgraph", "mindmap", "timeline", "style", "class", "click",
    "participant", "actor", "note", "loop", "alt", "opt", "par",
    "LR", "RL", "TB", "BT", "TD",
}


class _OutputLexer(Lexer):
    """Applies markdown-like styling to the output buffer line-by-line."""

    def lex_document(self, document):
        lines = document.lines

        # Pre-process: track code-fence state and language across lines
        styled: list[list[tuple[str, str]]] = []
        in_code = False
        code_lang = ""
        table_header_next = False  # the row after a separator is still "header zone"

        for i, line in enumerate(lines):
            stripped = line.strip()

            # --- Code fences ---
            if stripped.startswith("```"):
                if not in_code:
                    in_code = True
                    code_lang = stripped[3:].strip().lower()
                    if code_lang == "mermaid":
                        styled.append([
                            ("class:dim", line[: line.find("```")]),
                            ("class:diagram.label", "\u25b8 Mermaid Diagram"),
                        ])
                        continue
                    styled.append([("class:dim", line)])
                    continue
                else:
                    in_code = False
                    if code_lang == "mermaid":
                        styled.append([
                            ("class:dim", line[: line.find("```")]),
                            ("class:diagram.label", "\u25c2 end diagram"),
                        ])
                    else:
                        styled.append([("class:dim", line)])
                    code_lang = ""
                    continue

            if in_code:
                if code_lang == "mermaid":
                    styled.append(self._style_mermaid_line(line))
                else:
                    styled.append([("class:dim", line)])
                continue

            # --- Table rows ---
            if _RE_TABLE_SEP.match(line):
                styled.append([("class:table.separator", line)])
                table_header_next = False
                continue

            m = _RE_TABLE_ROW.match(line)
            if m:
                # Check if next line is a separator → this is a header row
                is_header = False
                if i + 1 < len(lines) and _RE_TABLE_SEP.match(lines[i + 1]):
                    is_header = True
                styled.append(self._style_table_row(line, is_header))
                continue

            styled.append(self._style_line(line))

        def get_line(lineno: int) -> list[tuple[str, str]]:
            if lineno < len(styled):
                return styled[lineno]
            return [("", "")]

        return get_line

    # -- line-level dispatch ------------------------------------------------

    def _style_line(self, line: str) -> list[tuple[str, str]]:
        stripped = line.strip()

        # Picker lines
        if stripped.startswith(("Select a session", "Archive sessions")):
            return [("class:picker.header", line)]
        if line.startswith(" > "):
            return [("class:picker.cursor", line)]
        if stripped.startswith(("[x]", "[ ]")):
            # Multi-select row (not highlighted)
            idx = line.index("[")
            check = line[idx:idx + 3]
            rest = line[idx + 3:]
            style = "class:picker.check" if check == "[x]" else "class:picker.uncheck"
            return [
                ("", line[:idx]),
                (style, check),
                ("class:picker.meta", rest),
            ]
        # Single-select non-cursor rows: "   <12-char-hex>  ..."
        if (len(stripped) > 12
                and re.match(r"^[0-9a-f]{12}\b", stripped)
                and not stripped.startswith("you> ")):
            idx = line.index(stripped[:12])
            return [
                ("", line[:idx]),
                ("class:picker.sid", stripped[:12]),
                ("class:picker.meta", line[idx + 12:]),
            ]

        # User message echo: "you> ..."
        if stripped.startswith("you> "):
            idx = line.index("you> ")
            return [
                ("", line[:idx]),
                ("class:user-prefix", "you> "),
                ("class:md.bold", line[idx + 5:]),
            ]

        # Headings: ## ...
        m = _RE_HEADING.match(line)
        if m:
            return [("class:md.heading", line)]

        # Status line: model | 1234in/567out
        if _RE_STATUS.match(line):
            return [("class:dim", line)]

        # Tool results
        if stripped.startswith("v ") and "(" in stripped:
            return [("class:success", line)]
        if stripped.startswith("x ") and ("failed" in stripped or "(" in stripped):
            return [("class:error", line)]

        # System / thinking / status
        if stripped.startswith("[system]") or stripped.startswith("[thinking]"):
            return [("class:dim", line)]
        if stripped.startswith("[skipped]"):
            return [("class:warning", line)]
        if stripped.startswith("[failed]") or stripped.startswith("[error]"):
            return [("class:error", line)]

        # Approval prompt
        if stripped.startswith("--- Write operation") or stripped == "-" * 30:
            return [("class:warning", line)]

        # Mascot / banner (box-drawing characters)
        if any(ch in stripped for ch in "\u256d\u256e\u2570\u256f\u25d5\u2550\u2518\u2514"):
            return [("class:welcome", line)]

        # Welcome version line: "  Neut v0.1.0 — ..."
        if stripped.startswith("Neut v") and "\u2014" in stripped:
            return [("class:welcome", line)]

        # Metadata lines: "  model: ... | commit: ..."
        if stripped.startswith("model:") or stripped.startswith("cwd:"):
            return [("class:dim", line)]

        # Help hint line
        if stripped.startswith("Type /help"):
            return self._style_help_hint(line)

        # Slash command in help listing: "  /help   Show this help"
        m = _RE_SLASH.match(line)
        if m:
            return [
                ("", m.group(1)),
                ("class:slash-cmd", m.group(2)),
                ("", m.group(3)),
            ]

        # Bold section headers (e.g., "  Chat Commands:")
        if stripped.endswith(":") and not stripped.startswith("-"):
            if _RE_BOLD.search(stripped) is None and len(stripped) < 60:
                return [("class:md.bold", line)]

        # List items: - ...
        m = _RE_LIST.match(line)
        if m:
            return self._style_list_item(m.group(1), "-", m.group(2))

        m = _RE_ORDERED.match(line)
        if m:
            indent = m.group(1)
            rest = line[len(indent):]
            dot_pos = rest.index(". ")
            num = rest[: dot_pos + 2]
            content = rest[dot_pos + 2 :]
            return [
                ("", indent),
                ("class:md.list-bullet", num),
                *self._parse_inline(content),
            ]

        # Blockquote: > ...
        if stripped.startswith(">"):
            return [("class:md.blockquote", line)]

        # Default: inline markdown
        return self._parse_inline(line)

    # -- helpers ------------------------------------------------------------

    def _style_list_item(
        self, indent: str, bullet: str, content: str,
    ) -> list[tuple[str, str]]:
        return [
            ("", indent),
            ("class:md.list-bullet", f"{bullet} "),
            *self._parse_inline(content),
        ]

    def _parse_inline(self, line: str) -> list[tuple[str, str]]:
        """Parse **bold** and `code` inline markers."""
        if not line:
            return [("", "")]

        # Collect matches
        matches: list[tuple[int, int, str, str]] = []
        for m in _RE_BOLD.finditer(line):
            matches.append((m.start(), m.end(), "class:md.bold", m.group(1)))
        for m in _RE_CODE.finditer(line):
            matches.append(
                (m.start(), m.end(), "class:md.code", f"`{m.group(1)}`"),
            )

        # Sort by position, drop overlaps
        matches.sort(key=lambda x: x[0])
        filtered: list[tuple[int, int, str, str]] = []
        last_end = 0
        for start, end, style, text in matches:
            if start >= last_end:
                filtered.append((start, end, style, text))
                last_end = end

        # Build fragments
        fragments: list[tuple[str, str]] = []
        pos = 0
        for start, end, style, text in filtered:
            if start > pos:
                fragments.append(("", line[pos:start]))
            fragments.append((style, text))
            pos = end

        if pos < len(line):
            fragments.append(("", line[pos:]))

        return fragments if fragments else [("", line)]

    def _style_mermaid_line(self, line: str) -> list[tuple[str, str]]:
        """Style a line inside a ```mermaid block with keyword highlighting."""
        stripped = line.strip()
        if not stripped:
            return [("class:diagram.code", line)]

        # Highlight keywords at the start of lines
        first_word = stripped.split()[0].rstrip(":")
        if first_word in _MERMAID_KEYWORDS:
            idx = line.index(first_word)
            return [
                ("class:diagram.code", line[:idx]),
                ("class:diagram.keyword", first_word),
                ("class:diagram.code", line[idx + len(first_word):]),
            ]

        # Style directives (e.g., "style A fill:#ff5722,color:#fff")
        if stripped.startswith("style ") or stripped.startswith("class "):
            return [("class:dim", line)]

        return [("class:diagram.code", line)]

    def _style_table_row(
        self, line: str, is_header: bool,
    ) -> list[tuple[str, str]]:
        """Style a markdown table row with colored pipes and header bold."""
        fragments: list[tuple[str, str]] = []
        cell_style = "class:table.header" if is_header else ""
        parts = line.split("|")

        for i, part in enumerate(parts):
            if i > 0:
                fragments.append(("class:table.pipe", "\u2502"))  # │ instead of |
            if part:
                if is_header:
                    fragments.append(("class:table.header", part))
                else:
                    fragments.extend(self._parse_inline(part))

        return fragments if fragments else [("", line)]

    def _style_help_hint(self, line: str) -> list[tuple[str, str]]:
        parts: list[tuple[str, str]] = []
        pos = 0
        for cmd in ("/help", "/exit"):
            idx = line.find(cmd, pos)
            if idx >= 0:
                if idx > pos:
                    parts.append(("class:dim", line[pos:idx]))
                parts.append(("class:slash-cmd", cmd))
                pos = idx + len(cmd)
        if pos < len(line):
            parts.append(("class:dim", line[pos:]))
        return parts if parts else [("class:dim", line)]


# ---------------------------------------------------------------------------
# Table alignment — reformats markdown tables with padded columns
# ---------------------------------------------------------------------------

def _align_table(lines: list[str], max_width: int) -> list[str]:
    """Reformat a markdown table block with aligned, padded columns."""
    if not lines:
        return lines

    # Parse each row into cells
    rows: list[tuple[str, list[str], bool]] = []  # (indent, cells, is_sep)
    for line in lines:
        stripped = line.lstrip()
        indent = line[: len(line) - len(stripped)]
        is_sep = bool(_RE_TABLE_SEP.match(line))
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        rows.append((indent, cells, is_sep))

    if not rows:
        return lines

    # Calculate column widths (ignore separators for width calc)
    num_cols = max(len(cells) for _, cells, _ in rows)
    widths = [0] * num_cols
    for indent, cells, is_sep in rows:
        if is_sep:
            continue
        for j, cell in enumerate(cells):
            if j < num_cols:
                widths[j] = max(widths[j], len(cell))

    # Ensure minimum width of 3 per column
    widths = [max(w, 3) for w in widths]

    # Reformat rows
    result: list[str] = []
    for indent, cells, is_sep in rows:
        padded: list[str] = []
        for j in range(num_cols):
            cell = cells[j] if j < len(cells) else ""
            if is_sep:
                padded.append("-" * widths[j])
            else:
                padded.append(cell.ljust(widths[j]))
        result.append(f"{indent}| {' | '.join(padded)} |")

    return result


# ---------------------------------------------------------------------------
# ANSI stripper for slash command output
# ---------------------------------------------------------------------------

_ANSI_RE = re.compile(r"\x1b\[[^m]*m|\x1b\]8;;[^\x07]*\x07")


def _strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)


# ---------------------------------------------------------------------------
# Session picker state
# ---------------------------------------------------------------------------

class PickerMode(Enum):
    SELECT = "select"   # /sessions: pick one to resume
    MULTI = "multi"     # /archive: checkboxes to archive multiple


@dataclass
class PickerState:
    mode: PickerMode
    items: list[dict[str, Any]]  # session metadata from load_meta()
    cursor: int = 0
    checked: set[int] = field(default_factory=set)
    saved_output: str = ""       # output buffer to restore on dismiss


def _relative_time(iso_str: str) -> str:
    """Convert an ISO-8601 timestamp to a human-readable relative time."""
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        delta = now - dt
        secs = int(delta.total_seconds())
        if secs < 60:
            return "just now"
        if secs < 3600:
            m = secs // 60
            return f"{m}m ago"
        if secs < 86400:
            h = secs // 3600
            return f"{h}h ago"
        if secs < 172800:
            return "yesterday"
        if secs < 604800:
            d = secs // 86400
            return f"{d}d ago"
        return dt.strftime("%b %d")
    except (ValueError, TypeError):
        return iso_str[:10] if len(iso_str) >= 10 else iso_str


# ---------------------------------------------------------------------------
# Placeholder processor — greyed-out suggestion text in the input bar
# ---------------------------------------------------------------------------

class _PlaceholderProcessor(Processor):
    """Shows greyed-out suggestion text when the input buffer is empty."""

    def __init__(self, get_text):
        self._get_text = get_text

    def apply_transformation(self, ti):
        if not ti.document.text and ti.lineno == 0:
            placeholder = self._get_text()
            if placeholder:
                return Transformation(
                    fragments=ti.fragments + [("class:placeholder", placeholder)],
                )
        return Transformation(ti.fragments)


# ---------------------------------------------------------------------------
# Suggestion intelligence — context-aware input hints
# ---------------------------------------------------------------------------

# Suggestions keyed by conversation state.
# Each entry is a list to allow rotation on repeated visits.
_SUGGESTIONS: dict[str, list[str]] = {
    "welcome": [
        "Ask anything about Neutron OS, or /help for commands",
    ],
    "after_turn": [
        "Ask a follow-up question...",
        "Try /status, or ask something new",
        "What else would you like to know?",
    ],
    "after_error": [
        "Try rephrasing, or /new for a fresh session",
    ],
    "after_tool": [
        "What would you like to do next?",
    ],
    "after_slash": [
        "Ask me anything, or try another /command",
    ],
    "after_approval": [
        "Continue, or /status to review",
    ],
}


# ---------------------------------------------------------------------------
# Approval bridge
# ---------------------------------------------------------------------------

@dataclass
class _ApprovalRequest:
    """Bridges the agent thread (which needs a choice) to the main thread."""
    action: Action
    event: threading.Event = field(default_factory=threading.Event)
    choice: str = "r"


# ---------------------------------------------------------------------------
# Interaction modes (mirroring InputProvider._MODES)
# ---------------------------------------------------------------------------

_MODES = ("ask", "plan", "agent")


# ---------------------------------------------------------------------------
# FullScreenChat
# ---------------------------------------------------------------------------

class FullScreenChat:
    """Full-screen TUI for neut chat with fixed input at the bottom."""

    def __init__(
        self,
        agent: ChatAgent,
        store: SessionStore,
        stream: bool = True,
        show_banner: bool = False,
    ):
        self._agent = agent
        self._store = store
        self._stream = stream
        self._show_banner = show_banner

        # State
        self._busy = False
        self._interrupted = False
        self._mode_idx = 0  # index into _MODES
        self._spinner_visible = False
        self._spinner_text: FormattedText = FormattedText([])
        self._approval_pending: Optional[_ApprovalRequest] = None
        self._output_lock = threading.Lock()
        self._last_model = ""
        self._last_tokens = ""
        self._last_cost = ""
        self._picker: Optional[PickerState] = None

        # Suggestion state — drives placeholder text in input bar
        self._suggestion_key = "welcome"
        self._suggestion_idx = 0

        # Spinner state (updated from spinner thread)
        self._spinner_label = "Thinking"
        self._spinner_sub_state = ""
        self._spinner_input_tokens = 0
        self._spinner_output_tokens = 0
        self._spinner_start: float = 0.0
        self._spinner_stop_event = threading.Event()
        self._spinner_thread: Optional[threading.Thread] = None

        # Build UI
        self._output_buffer = Buffer(read_only=True, name="output")
        self._input_buffer = Buffer(
            name="input",
            accept_handler=self._on_accept,
            multiline=False,
        )
        self._app = self._build_app()

    # -- Layout & keybindings ------------------------------------------------

    def _build_app(self) -> Application:
        kb = KeyBindings()

        @kb.add("c-d")
        def _exit(event):
            event.app.exit()

        @kb.add("c-c")
        def _clear_or_cancel(event):
            if self._picker is not None:
                self._dismiss_picker()
                return
            if self._busy:
                self._interrupted = True
            else:
                self._input_buffer.reset()

        @kb.add("escape")
        def _escape(event):
            if self._picker is not None:
                self._dismiss_picker()
                return
            if self._busy:
                self._interrupted = True
            else:
                event.app.exit()

        @kb.add("s-tab")
        def _cycle_mode(event):
            if self._picker is not None:
                return
            self._mode_idx = (self._mode_idx + 1) % len(_MODES)
            event.app.invalidate()

        # -- Picker keybindings (active only when picker is open) --
        picker_kb = KeyBindings()

        @picker_kb.add("up")
        def _picker_up(event):
            p = self._picker
            if p and p.cursor > 0:
                p.cursor -= 1
                self._render_picker()

        @picker_kb.add("down")
        def _picker_down(event):
            p = self._picker
            if p and p.cursor < len(p.items) - 1:
                p.cursor += 1
                self._render_picker()

        @picker_kb.add(" ")
        def _picker_toggle(event):
            p = self._picker
            if p and p.mode == PickerMode.MULTI:
                if p.cursor in p.checked:
                    p.checked.discard(p.cursor)
                else:
                    p.checked.add(p.cursor)
                self._render_picker()

        @picker_kb.add("enter")
        def _picker_confirm(event):
            if self._picker is not None:
                self._confirm_picker()

        conditional_picker = ConditionalKeyBindings(
            picker_kb,
            filter=Condition(lambda: self._picker is not None),
        )
        combined_kb = merge_key_bindings([kb, conditional_picker])

        # Output area — fills ALL remaining vertical space, pushing
        # the fixed-height bottom elements to the terminal floor.
        output_window = Window(
            content=BufferControl(
                buffer=self._output_buffer,
                focusable=False,
                lexer=_OutputLexer(),
            ),
            wrap_lines=True,
            height=D(min=1, weight=1),
        )

        # Spinner bar — visible only when busy
        spinner_bar = ConditionalContainer(
            content=Window(
                content=FormattedTextControl(lambda: self._spinner_text),
                height=1,
            ),
            filter=Condition(lambda: self._spinner_visible),
        )

        # Horizontal border
        border = Window(
            content=FormattedTextControl(self._get_border_text),
            height=1,
        )

        # Input area with "you>" prompt and contextual placeholder
        input_window = Window(
            content=BufferControl(
                buffer=self._input_buffer,
                input_processors=[
                    BeforeInput(self._get_input_prefix),
                    _PlaceholderProcessor(self._get_suggestion),
                ],
            ),
            height=1,
        )

        # Toolbar — mode switcher
        toolbar = Window(
            content=FormattedTextControl(self._get_toolbar_text),
            height=1,
        )

        # Persistent status line — model, tokens, cost
        status_line = Window(
            content=FormattedTextControl(self._get_status_text),
            height=1,
        )

        # Bottom border — closes the input frame
        bottom_border = Window(
            content=FormattedTextControl(self._get_border_text),
            height=1,
        )

        layout = Layout(
            HSplit([
                output_window,
                spinner_bar,
                status_line,
                border,
                input_window,
                bottom_border,
                toolbar,
                Window(height=1),
            ]),
            focused_element=input_window,
        )

        return Application(
            layout=layout,
            key_bindings=combined_kb,
            full_screen=True,
            mouse_support=False,
            style=_STYLE,
        )

    def _get_input_prefix(self) -> list[tuple[str, str]]:
        """Dynamic input prompt: changes during approval/picker mode."""
        if self._picker is not None:
            return [("", "")]
        if self._approval_pending:
            return [("class:warning", "  > ")]
        return [("class:prompt", "you> ")]

    def _get_border_text(self) -> FormattedText:
        try:
            width = self._app.output.get_size().columns
        except Exception:
            width = 80
        return FormattedText([("class:border", "\u2500" * width)])

    def _get_toolbar_text(self) -> FormattedText:
        if self._picker is not None:
            if self._picker.mode == PickerMode.MULTI:
                return FormattedText([
                    ("class:toolbar.dim",
                     " \u2191\u2193 navigate  \u00b7  Space toggle"
                     "  \u00b7  Enter confirm  \u00b7  Esc cancel"),
                ])
            return FormattedText([
                ("class:toolbar.dim",
                 " \u2191\u2193 navigate  \u00b7  Enter to load"
                 "  \u00b7  Esc cancel"),
            ])
        mode = _MODES[self._mode_idx]
        parts: list[tuple[str, str]] = [
            ("class:toolbar.arrow", " \u23f5\u23f5 "),
            ("class:toolbar.mode", f"{mode} mode"),
            ("class:toolbar.dim", "  (shift+tab to switch)"),
            ("class:toolbar.dim", "  \u00b7  esc to exit"),
        ]
        if self._approval_pending:
            parts.append(
                ("class:toolbar.approval",
                 "  \u00b7  [a]pprove [A]lways [r]eject [s]kip"),
            )
        return FormattedText(parts)

    def _get_status_text(self) -> FormattedText:
        """Persistent status bar: model · tokens · cost, right-justified."""
        pieces: list[str] = []
        if self._last_model:
            pieces.append(self._last_model)
        if self._last_tokens:
            pieces.append(self._last_tokens)
        if self._last_cost:
            pieces.append(self._last_cost)
        if not pieces:
            return FormattedText([("class:status", "")])
        content = " \u00b7 ".join(pieces)
        try:
            width = self._app.output.get_size().columns
        except Exception:
            width = 80
        padded = content.rjust(width)
        return FormattedText([("class:status", padded)])

    # -- Suggestion intelligence ----------------------------------------------

    def _get_suggestion(self) -> str:
        """Return the current contextual suggestion for the input placeholder."""
        if self._picker is not None:
            return ""
        if self._approval_pending:
            return "Type a/A/r/s to respond to the approval prompt"
        if self._busy:
            return ""
        entries = _SUGGESTIONS.get(self._suggestion_key, [])
        if not entries:
            return ""
        return entries[self._suggestion_idx % len(entries)]

    def _set_suggestion(self, key: str) -> None:
        """Advance the suggestion state. Rotates within a category."""
        if key == self._suggestion_key:
            entries = _SUGGESTIONS.get(key, [])
            if len(entries) > 1:
                self._suggestion_idx = (self._suggestion_idx + 1) % len(entries)
        else:
            self._suggestion_key = key
            self._suggestion_idx = 0

    # -- Thread-safe output --------------------------------------------------

    def _get_wrap_width(self) -> int:
        """Terminal width available for output text."""
        try:
            return self._app.output.get_size().columns - 1
        except Exception:
            return 79

    def _word_wrap(self, text: str, width: int) -> str:
        """Word-wrap complete lines, preserving tables and indentation."""
        lines = text.split("\n")
        result: list[str] = []
        i = 0
        while i < len(lines):
            line = lines[i]

            # --- Table block: collect consecutive rows, align columns ---
            if _RE_TABLE_ROW.match(line) or _RE_TABLE_SEP.match(line):
                table_lines: list[str] = []
                while i < len(lines) and (
                    _RE_TABLE_ROW.match(lines[i])
                    or _RE_TABLE_SEP.match(lines[i])
                ):
                    table_lines.append(lines[i])
                    i += 1
                result.extend(_align_table(table_lines, width))
                continue

            # --- Regular line ---
            if len(line) <= width or not line.strip():
                result.append(line)
            else:
                stripped = line.lstrip()
                indent = line[: len(line) - len(stripped)]
                wrapped = textwrap.fill(
                    stripped,
                    width=max(width - len(indent), 20),
                    initial_indent=indent,
                    subsequent_indent=indent + "  ",
                    break_long_words=False,
                    break_on_hyphens=False,
                )
                result.append(wrapped)
            i += 1
        return "\n".join(result)

    def _append_output(self, text: str) -> None:
        """Append text to the output buffer, word-wrapped (thread-safe).

        Only complete lines (terminated by \\n) are word-wrapped.
        Partial lines (streaming) are left for the Window's fallback
        character wrap until the next newline finalises them.
        """
        with self._output_lock:
            width = self._get_wrap_width()
            old = self._output_buffer.text

            # Pull the trailing partial line out of the buffer so we can
            # re-wrap it together with the new text.
            if old and not old.endswith("\n"):
                last_nl = old.rfind("\n")
                if last_nl >= 0:
                    complete_old = old[: last_nl + 1]
                    partial = old[last_nl + 1 :]
                else:
                    complete_old = ""
                    partial = old
            else:
                complete_old = old
                partial = ""

            combined = partial + text

            if "\n" in combined:
                last_nl = combined.rfind("\n")
                to_wrap = combined[: last_nl + 1]
                new_partial = combined[last_nl + 1 :]
                wrapped = self._word_wrap(to_wrap, width)
                new_text = complete_old + wrapped + new_partial
            else:
                # All partial — no wrapping yet
                new_text = complete_old + combined

            self._output_buffer.set_document(
                Document(new_text, len(new_text)),
                bypass_readonly=True,
            )
        self._app.invalidate()

    # -- Input accept handler ------------------------------------------------

    def _on_accept(self, buff: Buffer) -> bool:
        """Called when user presses Enter in the input buffer.

        Returns True to keep text in buffer, False to clear it.
        """
        # Picker handles Enter via its own keybinding
        if self._picker is not None:
            return True

        text = buff.text.strip()
        if not text:
            return True  # no-op, keep empty buffer

        # If we're waiting for an approval response
        if self._approval_pending:
            self._handle_approval_input(text)
            return False

        # Don't allow input while agent is working
        if self._busy:
            return True  # keep text so user can send it later

        # Slash commands
        if text.startswith("/"):
            self._handle_slash_command(text)
            return False

        # Legacy exit
        if text.lower() in ("exit", "quit"):
            self._app.exit()
            return False

        # Normal chat — spawn agent thread
        self._busy = True
        self._interrupted = False
        self._append_output(f"you> {text}\n\n")

        t = threading.Thread(
            target=self._run_agent_turn,
            args=(text,),
            daemon=True,
        )
        t.start()
        return False

    # -- Slash commands ------------------------------------------------------

    def _handle_slash_command(self, text: str) -> None:
        parts = text.split()
        cmd = parts[0].lower()

        if cmd in ("/exit", "/quit"):
            self._app.exit()
            return

        # Interactive session picker for /sessions
        if cmd == "/sessions":
            self._open_picker(PickerMode.SELECT)
            return

        # Interactive archive picker for bare /archive (no args)
        if cmd == "/archive" and len(parts) == 1:
            self._open_picker(PickerMode.MULTI)
            return

        from tools.agents.chat.cli import _handle_slash_command
        result = _handle_slash_command(text, self._agent, self._store)
        if result == "exit":
            self._app.exit()
            return
        if result:
            clean = _strip_ansi(result)
            self._append_output(clean + "\n")
        self._set_suggestion("after_slash")

    # -- Session picker ------------------------------------------------------

    def _open_picker(self, mode: PickerMode) -> None:
        """Open the interactive session picker overlay."""
        session_ids = self._store.list_sessions()
        if not session_ids:
            self._append_output("\n  No saved sessions.\n\n")
            return

        items: list[dict[str, Any]] = []
        for sid in session_ids[:20]:
            meta = self._store.load_meta(sid)
            if meta:
                items.append(meta)

        if not items:
            self._append_output("\n  No saved sessions.\n\n")
            return

        # Save current output so we can restore on dismiss
        saved = self._output_buffer.text

        self._picker = PickerState(
            mode=mode,
            items=items,
            cursor=0,
            checked=set(),
            saved_output=saved,
        )
        self._render_picker()

    def _render_picker(self) -> None:
        """Render the picker list into the output buffer."""
        p = self._picker
        if p is None:
            return

        lines: list[str] = [p.saved_output.rstrip("\n"), ""]

        if p.mode == PickerMode.MULTI:
            lines.append(
                "  Archive sessions"
                " (\u2191\u2193 navigate \u00b7 Space toggle"
                " \u00b7 Enter confirm \u00b7 Esc cancel)"
            )
        else:
            lines.append(
                "  Select a session"
                " (\u2191\u2193 navigate \u00b7 Enter to load"
                " \u00b7 Esc cancel)"
            )
        lines.append("")

        for i, item in enumerate(p.items):
            sid = item.get("id", "?")[:12]
            title = item.get("title") or "(untitled)"
            if len(title) > 30:
                title = title[:27] + "..."
            msg_count = item.get("message_count", 0)
            updated = _relative_time(item.get("updated_at", ""))

            pointer = " > " if i == p.cursor else "   "

            if p.mode == PickerMode.MULTI:
                check = "[x]" if i in p.checked else "[ ]"
                lines.append(
                    f"{pointer}{check} {sid}  {title:<30s}"
                    f"  {msg_count:>3d} msgs  {updated}"
                )
            else:
                lines.append(
                    f"{pointer}{sid}  {title:<30s}"
                    f"  {msg_count:>3d} msgs  {updated}"
                )

        lines.append("")
        text = "\n".join(lines)

        with self._output_lock:
            self._output_buffer.set_document(
                Document(text, len(text)),
                bypass_readonly=True,
            )
        self._app.invalidate()

    def _confirm_picker(self) -> None:
        """Handle Enter in the picker — resume or archive selected sessions."""
        p = self._picker
        if p is None:
            return

        from tools.agents.chat.commands import cmd_resume, cmd_archive

        if p.mode == PickerMode.SELECT:
            item = p.items[p.cursor]
            sid = item["id"]
            self._dismiss_picker()
            result = cmd_resume(sid, self._store, self._agent)
            clean = _strip_ansi(result)
            self._append_output(clean + "\n")
        elif p.mode == PickerMode.MULTI:
            checked = sorted(p.checked)
            if not checked:
                # Nothing selected — dismiss silently
                self._dismiss_picker()
                return
            sids = [p.items[i]["id"] for i in checked]
            self._dismiss_picker()
            for sid in sids:
                result = cmd_archive(sid, self._store, self._agent)
                clean = _strip_ansi(result)
                self._append_output(clean + "\n")

        self._set_suggestion("after_slash")

    def _dismiss_picker(self) -> None:
        """Close picker and restore original output."""
        p = self._picker
        if p is None:
            return
        saved = p.saved_output
        self._picker = None
        with self._output_lock:
            self._output_buffer.set_document(
                Document(saved, len(saved)),
                bypass_readonly=True,
            )
        self._app.invalidate()

    # -- Agent turn (background thread) --------------------------------------

    def _run_agent_turn(self, text: str) -> None:
        try:
            self._start_spinner("Thinking")

            if self._stream and self._agent.gateway.available:
                response = self._agent.turn(text, stream=True)
            else:
                response = self._agent.turn(text, stream=False)

            self._stop_spinner()
            self._append_output("\n")

            # Update persistent status bar (not output)
            if self._agent.gateway.active_provider:
                self._last_model = self._agent.gateway.active_provider.model
            usage = self._agent.usage
            if usage.turns:
                last = usage.turns[-1]
                self._last_tokens = (
                    f"{last.input_tokens}in/{last.output_tokens}out"
                )
                if last.cost > 0:
                    self._last_cost = f"${last.cost:.4f}"

            self._store.save(self._agent.session)
            self._set_suggestion("after_turn")
        except Exception as e:
            self._stop_spinner()
            self._append_output(f"\n  [error] {e}\n\n")
            self._set_suggestion("after_error")
        finally:
            self._busy = False
            self._app.invalidate()

    # -- Spinner -------------------------------------------------------------

    def _start_spinner(self, label: str = "Thinking") -> None:
        self._spinner_label = label
        self._spinner_sub_state = ""
        self._spinner_input_tokens = 0
        self._spinner_output_tokens = 0
        self._spinner_start = time.monotonic()
        self._spinner_stop_event.clear()
        self._spinner_visible = True

        self._spinner_thread = threading.Thread(
            target=self._spinner_loop, daemon=True,
        )
        self._spinner_thread.start()

    def _stop_spinner(self) -> None:
        self._spinner_stop_event.set()
        if self._spinner_thread is not None:
            self._spinner_thread.join(timeout=1.0)
            self._spinner_thread = None
        self._spinner_visible = False
        self._app.invalidate()

    def _spinner_loop(self) -> None:
        idx = 0
        while not self._spinner_stop_event.is_set():
            frame = PULSE_FRAMES[idx % len(PULSE_FRAMES)]
            elapsed = time.monotonic() - self._spinner_start

            label = self._spinner_label
            sub = self._spinner_sub_state
            in_tok = self._spinner_input_tokens
            out_tok = self._spinner_output_tokens

            # Build FormattedText with 24-bit color
            color = f"fg:#{frame.r:02x}{frame.g:02x}{frame.b:02x}"
            parts: list[tuple[str, str]] = [
                ("", "  "),
                (color, frame.symbol),
                ("", f" {label}\u2026 "),
            ]

            # Detail parts
            detail_items = [_format_elapsed(elapsed)]
            total_tok = in_tok + out_tok
            if total_tok > 0:
                detail_items.append(
                    f"\u2193 {_format_tokens(total_tok)} tokens",
                )
            if sub:
                detail_items.append(sub)
            detail_items.append("esc to interrupt")
            detail = " \u00b7 ".join(detail_items)
            parts.append(("class:spinner.detail", f"({detail})"))

            self._spinner_text = FormattedText(parts)
            self._app.invalidate()

            idx += 1
            self._spinner_stop_event.wait(_FRAME_INTERVAL)

    # -- Approval handling ---------------------------------------------------

    def _handle_approval_input(self, text: str) -> None:
        req = self._approval_pending
        if req is None:
            return

        raw = text.strip()
        if raw == "A":
            req.choice = "A"
        elif raw.lower() in ("a", "approve"):
            req.choice = "a"
        elif raw.lower() in ("r", "reject", "s", "skip"):
            req.choice = "r"
        else:
            self._append_output(
                "  Choose [a]pprove, [A]lways allow, [r]eject, or [s]kip\n",
            )
            return

        self._approval_pending = None
        self._set_suggestion("after_approval")
        req.event.set()

    # -- Run -----------------------------------------------------------------

    def run(self) -> None:
        """Start the full-screen TUI."""
        # Wire our TUI render provider into the agent
        provider = _TuiRenderProvider(self)
        self._agent.set_render_provider(provider)

        # Initialize status bar with gateway model before first turn
        gw = self._agent.gateway
        if gw and gw.active_provider:
            self._last_model = gw.active_provider.model

        # Show welcome
        provider.render_welcome(
            gateway=self._agent.gateway,
            show_banner=self._show_banner,
        )

        # Suppress direnv noise when the fullscreen app exits and the
        # terminal restores (direnv re-evaluates .envrc on every cd/exec).
        old_log = os.environ.get("DIRENV_LOG_FORMAT")
        os.environ["DIRENV_LOG_FORMAT"] = ""
        try:
            self._app.run()
        finally:
            if old_log is None:
                os.environ.pop("DIRENV_LOG_FORMAT", None)
            else:
                os.environ["DIRENV_LOG_FORMAT"] = old_log


# ---------------------------------------------------------------------------
# TUI Render Provider
# ---------------------------------------------------------------------------

class _TuiRenderProvider(RenderProvider):
    """Render provider that writes to the FullScreenChat output buffer.

    All output is plain text — the _OutputLexer handles styling at
    render time based on markdown patterns.
    """

    def __init__(self, tui: FullScreenChat):
        self._tui = tui

    def stream_text(self, chunks: Iterator[StreamChunk]) -> str:
        accumulated = ""
        first_text = True

        for chunk in chunks:
            if chunk.type == "text":
                if first_text:
                    self._tui._stop_spinner()
                    first_text = False
                accumulated += chunk.text
                self._tui._append_output(chunk.text)

            elif chunk.type == "thinking_delta":
                self._tui._spinner_label = "Reasoning"

            elif chunk.type == "usage":
                self._tui._spinner_input_tokens += chunk.input_tokens
                self._tui._spinner_output_tokens += chunk.output_tokens

            elif chunk.type == "tool_use_start":
                self._tui._stop_spinner()

            elif chunk.type == "done":
                self._tui._stop_spinner()
                if accumulated and not accumulated.endswith("\n"):
                    self._tui._append_output("\n")
                break

        return accumulated

    def render_welcome(
        self, gateway: Any = None, show_banner: bool = False,
    ) -> None:
        from importlib.metadata import version as pkg_version
        from pathlib import Path
        import subprocess

        # ASCII mascot — always shown
        mascot = (
            "       \u256d\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u256e\n"
            "       \u2502 \u25d5    \u25d5 \u2502   \u2572\u2502\u2571\n"
            "       \u2502  \u256e\u2500\u2500\u256d  \u2550\u2550\u2550\u2550\u2550*\u2550\u2550\n"
            "       \u2570\u2500\u2500\u252c\u2500\u2500\u252c\u2500\u2500\u256f   \u2571\u2502\u2572\n"
            "          \u2518  \u2514\n"
        )

        # Version
        try:
            ver = pkg_version("neutron-os")
        except Exception:
            ver = "dev"

        # Model
        model_name = "no LLM configured"
        if gateway and gateway.active_provider:
            model_name = gateway.active_provider.model

        # Project path
        cwd = Path.cwd()

        # Git commit
        git_hash = ""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True, cwd=str(cwd),
                timeout=2,
            )
            if result.returncode == 0:
                git_hash = result.stdout.strip()
        except Exception:
            pass

        lines = [mascot]
        lines.append(f"  Neut v{ver} — Neutron OS interactive agent\n")

        meta_parts = [f"model: {model_name}"]
        if git_hash:
            meta_parts.append(f"commit: {git_hash}")
        lines.append(f"  {' | '.join(meta_parts)}\n")

        lines.append(f"  cwd: {cwd}\n")
        lines.append(f"\n  Type /help for commands, ctrl+d to exit.\n\n")

        self._tui._append_output("".join(lines))

    def render_tool_start(self, name: str, params: dict[str, Any]) -> None:
        self._tui._start_spinner(f"Running {name}")

    def render_tool_result(
        self, name: str, result: dict[str, Any], elapsed: float,
    ) -> None:
        self._tui._stop_spinner()
        if "error" in result:
            self._tui._append_output(
                f"  x {name} failed ({elapsed:.1f}s): {result['error']}\n",
            )
        else:
            self._tui._append_output(f"  v {name} ({elapsed:.1f}s)\n")

    def render_approval_prompt(self, action: Action) -> str:
        text = (
            f"\n  --- Write operation ---\n"
            f"  {action.name}: {_format_params(action.params)}\n"
            f"  {'-' * 30}\n"
            f"  [a]pprove  [A]lways allow  [r]eject  [s]kip\n\n"
        )
        self._tui._append_output(text)

        req = _ApprovalRequest(action=action)
        self._tui._approval_pending = req
        self._tui._app.invalidate()

        # Block agent thread until user responds
        req.event.wait()
        return req.choice

    def render_action_result(self, action: Action) -> None:
        from tools.agents.orchestrator.actions import ActionStatus

        if action.status == ActionStatus.COMPLETED:
            result = action.result or {}
            if "error" in result:
                self._tui._append_output(f"  x {result['error']}\n")
            else:
                for k, v in result.items():
                    self._tui._append_output(f"  {k}: {v}\n")
        elif action.status == ActionStatus.REJECTED:
            self._tui._append_output(f"  [skipped] {action.name}\n")
        elif action.status == ActionStatus.FAILED:
            self._tui._append_output(f"  [failed] {action.error}\n")

    def render_status(
        self, model: str, tokens_in: int, tokens_out: int, cost: float,
    ) -> None:
        # Status handled in _run_agent_turn; no-op to avoid double-print
        pass

    def render_thinking(self, text: str, collapsed: bool = True) -> None:
        if not text:
            return
        lines = text.splitlines()
        if collapsed and len(lines) > 3:
            display = lines[:3] + [f"... ({len(lines) - 3} more lines)"]
        else:
            display = lines
        for line in display:
            self._tui._append_output(f"  [thinking] {line}\n")

    def render_message(self, role: str, content: str) -> None:
        if role == "assistant" and content:
            self._tui._append_output(f"{content}\n")
        elif role == "system" and content:
            self._tui._append_output(f"  [system] {content}\n")

    def render_session_list(self, sessions: list[dict[str, Any]]) -> None:
        if not sessions:
            self._tui._append_output("  No saved sessions.\n")
            return
        self._tui._append_output("\n  Saved sessions:\n")
        for s in sessions:
            sid = s.get("id", "?")
            msgs = s.get("messages", 0)
            updated = s.get("updated", "")
            self._tui._append_output(
                f"  {sid}  {msgs} messages  {updated}\n",
            )
        self._tui._append_output("\n")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _format_params(params: dict[str, Any]) -> str:
    if not params:
        return "(no parameters)"
    return "  |  ".join(f"{k}={v}" for k, v in params.items())
