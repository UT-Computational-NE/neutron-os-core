"""Terminal rendering for chat: streaming, markdown, approval prompts.

Reuses color infrastructure from tools.agents.setup.renderer and adds
streaming display, basic markdown formatting, and spinners.
"""

from __future__ import annotations

import re
import sys
import threading
import time
from contextlib import contextmanager
from typing import Any, Iterator, TYPE_CHECKING

from tools.agents.orchestrator.actions import Action, ActionStatus
from tools.agents.setup.renderer import _c, _Colors, _use_color

if TYPE_CHECKING:
    from tools.agents.sense.gateway import StreamChunk


# ---------------------------------------------------------------------------
# Markdown formatting (basic line-level)
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^(#{1,3})\s+(.+)$")
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_INLINE_CODE_RE = re.compile(r"`([^`]+)`")
_LIST_RE = re.compile(r"^(\s*)-\s+(.+)$")


def format_markdown_line(line: str) -> str:
    """Apply basic ANSI formatting to a single markdown line.

    Handles: headings, **bold**, `code`, and - list items.
    Falls back to plain text when color is disabled.
    """
    if not _use_color():
        return line

    # Code block fences — render dim
    if line.strip().startswith("```"):
        return _c(_Colors.DIM, line)

    # Headings
    m = _HEADING_RE.match(line)
    if m:
        return _c(_Colors.BOLD + _Colors.BRIGHT_BLUE, line)

    # List items — bullet in cyan
    m = _LIST_RE.match(line)
    if m:
        indent, content = m.group(1), m.group(2)
        content = _apply_inline(content)
        return f"{indent}{_c(_Colors.CYAN, '-')} {content}"

    return _apply_inline(line)


def _apply_inline(text: str) -> str:
    """Apply inline formatting: **bold** and `code`."""
    if not _use_color():
        return text
    text = _BOLD_RE.sub(lambda m: _c(_Colors.BOLD, m.group(1)), text)
    text = _INLINE_CODE_RE.sub(lambda m: _c(_Colors.CYAN, f"`{m.group(1)}`"), text)
    return text


# ---------------------------------------------------------------------------
# Streaming display
# ---------------------------------------------------------------------------

def stream_text(chunks: Iterator[StreamChunk]) -> str:
    """Write streaming text deltas to stdout, return accumulated text.

    Handles text chunks and tool-use indicators.
    """
    accumulated = ""
    in_code_block = False

    for chunk in chunks:
        if chunk.type == "text":
            text = chunk.text
            # Format line-by-line when we hit newlines
            if "\n" in text:
                parts = text.split("\n")
                for i, part in enumerate(parts):
                    if i > 0:
                        sys.stdout.write("\n")
                    if part:
                        # Check for code block toggles
                        if part.strip().startswith("```"):
                            in_code_block = not in_code_block
                        if _use_color() and not in_code_block:
                            part = _apply_inline(part)
                        sys.stdout.write(part)
            else:
                if _use_color() and not in_code_block:
                    text = _apply_inline(text)
                sys.stdout.write(text)
            sys.stdout.flush()
            accumulated += chunk.text

        elif chunk.type == "tool_use_start":
            msg = f"\n  {_c(_Colors.DIM, f'[calling {chunk.tool_name}...]')}\n"
            sys.stdout.write(msg)
            sys.stdout.flush()

        elif chunk.type == "tool_use_end":
            pass  # Tool results rendered separately

        elif chunk.type == "done":
            if accumulated and not accumulated.endswith("\n"):
                sys.stdout.write("\n")
                sys.stdout.flush()
            break

    return accumulated


# ---------------------------------------------------------------------------
# Thinking spinner
# ---------------------------------------------------------------------------

@contextmanager
def render_thinking_spinner(label: str = "Thinking"):
    """Context manager showing a braille spinner while work happens.

    Falls back to a static message in non-TTY environments.
    """
    if not (hasattr(sys.stdout, "isatty") and sys.stdout.isatty()):
        sys.stdout.write(f"  {label}...\n")
        sys.stdout.flush()
        yield
        return

    braille = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    stop = threading.Event()
    idx = [0]

    def spin():
        while not stop.is_set():
            char = braille[idx[0] % len(braille)]
            msg = f"  {_c(_Colors.DIM, f'{char} {label}')}"
            sys.stdout.write(f"\r{msg}")
            sys.stdout.flush()
            idx[0] += 1
            stop.wait(0.08)
        # Clear the spinner line
        sys.stdout.write("\r" + " " * 60 + "\r")
        sys.stdout.flush()

    t = threading.Thread(target=spin, daemon=True)
    t.start()
    try:
        yield
    finally:
        stop.set()
        t.join(timeout=1)


# ---------------------------------------------------------------------------
# Message rendering
# ---------------------------------------------------------------------------

def render_message(role: str, content: str) -> None:
    """Print a chat message with role prefix and markdown formatting."""
    if role == "assistant":
        prefix = _c(_Colors.BOLD + _Colors.BRIGHT_BLUE, "neut>") if _use_color() else "neut>"
        print()
        for line in content.splitlines():
            formatted = format_markdown_line(line)
            print(f"  {formatted}")
        print()
    elif role == "user":
        pass  # User messages are already printed by the REPL
    elif role == "system":
        print(f"  {_c(_Colors.DIM, f'[system] {content}')}")
    elif role == "tool_result":
        print(f"  {_c(_Colors.DIM, content)}")


def render_welcome(gateway=None) -> None:
    """Print the chat welcome message with gateway status."""
    print()
    print(f"  {_c(_Colors.BOLD + _Colors.BRIGHT_BLUE, 'neut chat')} — interactive agent")

    if gateway is not None:
        provider = gateway.active_provider
        if provider:
            status = _c(_Colors.GREEN, f"{provider.name} ({provider.model})")
        else:
            status = _c(_Colors.YELLOW, "stub mode (no LLM configured)")
        print(f"  Gateway: {status}")

    print(f"  Type {_c(_Colors.CYAN, '/help')} for commands, "
          f"{_c(_Colors.CYAN, '/exit')} to quit.")
    print()


# ---------------------------------------------------------------------------
# Approval UI
# ---------------------------------------------------------------------------

def render_approval_prompt(action: Action) -> str:
    """Render an approval prompt and get user response.

    Returns:
        "a" for approve, "r" for reject
    """
    print()
    if _use_color():
        print(f"  {_c(_Colors.YELLOW, '--- Write operation ---')}")
        print(f"  {_c(_Colors.BOLD, action.name)}: {_format_params(action.params)}")
        print(f"  {_c(_Colors.YELLOW, '-' * 30)}")
    else:
        print("  --- Write operation ---")
        print(f"  {action.name}: {_format_params(action.params)}")
        print("  " + "-" * 30)
    print(f"  [{_c(_Colors.GREEN, 'a')}]pprove  "
          f"[{_c(_Colors.RED, 'r')}]eject  "
          f"[{_c(_Colors.YELLOW, 's')}]kip")
    print()

    while True:
        try:
            choice = input("  > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return "r"
        if choice in ("a", "approve"):
            return "a"
        elif choice in ("r", "reject", "s", "skip"):
            return "r"
        else:
            print("  Choose [a]pprove, [r]eject, or [s]kip")


def render_action_result(action: Action) -> None:
    """Print the result of a completed action."""
    if action.status == ActionStatus.COMPLETED:
        result = action.result or {}
        if "error" in result:
            print(f"  {_c(_Colors.RED, '!')} {result['error']}")
        elif "url" in result:
            print(f"  {_c(_Colors.GREEN, 'Published:')} {result['url']} "
                  f"({result.get('version', '')})")
        elif "output" in result:
            print(f"  {_c(_Colors.GREEN, 'Generated:')} {result['output']}")
        elif "documents" in result:
            docs = result["documents"]
            if not docs:
                print("  No tracked documents.")
            else:
                for d in docs:
                    print(f"  {d['doc_id']}: {d['status']} ({d.get('version', '')})")
        elif "changed" in result:
            changed = result["changed"]
            if not changed:
                print("  No changes since last publish.")
            else:
                for c in changed:
                    print(f"  {c}")
        else:
            for k, v in result.items():
                print(f"  {k}: {v}")
    elif action.status == ActionStatus.REJECTED:
        print(f"  {_c(_Colors.YELLOW, '[skipped]')} {action.name}")
    elif action.status == ActionStatus.FAILED:
        print(f"  {_c(_Colors.RED, '[failed]')} {action.error}")


def render_session_list(sessions: list[dict[str, Any]]) -> None:
    """Render a formatted list of sessions."""
    if not sessions:
        print("  No saved sessions.")
        return

    print()
    print(f"  {_c(_Colors.BOLD, 'Saved sessions:')}")
    for s in sessions:
        sid = s.get("id", "?")
        msgs = s.get("messages", 0)
        updated = s.get("updated", "")
        print(f"  {_c(_Colors.CYAN, sid)}  {msgs} messages  {_c(_Colors.DIM, updated)}")
    print()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _format_params(params: dict[str, Any]) -> str:
    """Format action parameters for display."""
    if not params:
        return "(no parameters)"
    parts = []
    for k, v in params.items():
        parts.append(f"{k}={v}")
    return "  |  ".join(parts)
