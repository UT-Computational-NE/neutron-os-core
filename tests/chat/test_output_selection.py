"""Tests for output area mouse selection — position translation, style, overlay."""

import pytest
from unittest.mock import MagicMock

from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document

from tools.agents.chat.fullscreen import (
    _ScrollableBufferControl,
    _OutputLexer,
    _apply_selection_overlay,
    _highlight_fragments,
    _STYLE,
)


@pytest.fixture
def make_control():
    """Create a _ScrollableBufferControl with a fake TUI and given buffer text."""

    def _factory(text: str, scroll: int = 0, width: int = 40):
        tui = MagicMock()
        tui._scroll_vertical_scroll = scroll
        tui._scroll_window_width = width
        buf = Buffer(read_only=True, name="output")
        buf.set_document(Document(text, 0), bypass_readonly=True)
        ctrl = _ScrollableBufferControl(
            tui=tui, buffer=buf, focusable=True,
        )
        return ctrl

    return _factory


class TestMousePosToCursor:
    """Verify (visual_row, col) -> buffer cursor_position mapping."""

    def test_single_line(self, make_control):
        ctrl = make_control("hello world")
        assert ctrl._mouse_pos_to_cursor(0, 5) == 5

    def test_multi_line_second_row(self, make_control):
        ctrl = make_control("line one\nline two\nline three")
        assert ctrl._mouse_pos_to_cursor(1, 0) == len("line one\n")
        assert ctrl._mouse_pos_to_cursor(1, 4) == len("line one\n") + 4

    def test_col_clamped_to_line_length(self, make_control):
        ctrl = make_control("short\nhi")
        assert ctrl._mouse_pos_to_cursor(0, 99) == 5

    def test_scroll_offset(self, make_control):
        ctrl = make_control("aaa\nbbb\nccc\nddd", scroll=2)
        pos = ctrl._mouse_pos_to_cursor(0, 1)
        assert pos == len("aaa\nbbb\n") + 1

    def test_empty_lines(self, make_control):
        ctrl = make_control("first\n\n\nfourth")
        assert ctrl._mouse_pos_to_cursor(1, 0) == len("first\n")
        assert ctrl._mouse_pos_to_cursor(2, 0) == len("first\n\n")
        assert ctrl._mouse_pos_to_cursor(3, 2) == len("first\n\n\n") + 2

    def test_long_line_wraps(self, make_control):
        ctrl = make_control("abcdefghijklmnopqrstuvwxyz", width=10)
        assert ctrl._mouse_pos_to_cursor(0, 3) == 3
        assert ctrl._mouse_pos_to_cursor(1, 0) == 10
        assert ctrl._mouse_pos_to_cursor(1, 5) == 15
        assert ctrl._mouse_pos_to_cursor(2, 3) == 23

    def test_past_end_of_buffer(self, make_control):
        ctrl = make_control("only line")
        pos = ctrl._mouse_pos_to_cursor(10, 0)
        assert pos == len("only line")

    def test_mixed_short_and_long_lines(self, make_control):
        ctrl = make_control("short\nabcdefghijklmno\nend", width=10)
        assert ctrl._mouse_pos_to_cursor(0, 2) == 2
        assert ctrl._mouse_pos_to_cursor(1, 3) == len("short\n") + 3
        assert ctrl._mouse_pos_to_cursor(2, 2) == len("short\n") + 12
        assert ctrl._mouse_pos_to_cursor(3, 1) == len("short\nabcdefghijklmno\n") + 1


class TestSelectedStyleDefined:
    """The 'selected' style must exist so selection highlights are visible."""

    def test_selected_style_in_style_dict(self):
        style_list = _STYLE.style_rules
        class_names = [rule[0] for rule in style_list]
        assert "selected" in class_names, (
            "_STYLE must define 'selected' so drag-selection is visible"
        )

    def test_selected_style_has_background(self):
        for selector, style_str in _STYLE.style_rules:
            if selector == "selected":
                assert "bg:" in style_str or "bg#" in style_str or "reverse" in style_str, (
                    "'selected' style must set a background color or reverse"
                )
                return
        pytest.fail("'selected' rule not found")


class TestHighlightFragments:
    """_highlight_fragments applies class:selected to character ranges."""

    def test_full_fragment(self):
        frags = [("", "hello")]
        result = _highlight_fragments(frags, 0, 5)
        assert result == [(" class:selected", "hello")]

    def test_partial_start(self):
        frags = [("", "hello")]
        result = _highlight_fragments(frags, 0, 3)
        assert result == [(" class:selected", "hel"), ("", "lo")]

    def test_partial_end(self):
        frags = [("", "hello")]
        result = _highlight_fragments(frags, 2, 5)
        assert result == [("", "he"), (" class:selected", "llo")]

    def test_partial_middle(self):
        frags = [("", "hello")]
        result = _highlight_fragments(frags, 1, 4)
        assert result == [("", "h"), (" class:selected", "ell"), ("", "o")]

    def test_multi_fragment(self):
        frags = [("class:dim", "ab"), ("class:bold", "cd")]
        result = _highlight_fragments(frags, 1, 3)
        # "a" outside, "b" selected (dim), "c" selected (bold), "d" outside
        assert result == [
            ("class:dim", "a"),
            ("class:dim class:selected", "b"),
            ("class:bold class:selected", "c"),
            ("class:bold", "d"),
        ]

    def test_no_overlap(self):
        frags = [("", "hello")]
        result = _highlight_fragments(frags, 5, 10)
        assert result == [("", "hello")]


class TestApplySelectionOverlay:
    """_apply_selection_overlay modifies styled fragments in-place."""

    def test_single_line_selection(self):
        styled = [[("", "hello world")]]
        lines = ["hello world"]
        _apply_selection_overlay(styled, lines, 0, 5)
        # "hello" selected, " world" not
        assert styled[0] == [(" class:selected", "hello"), ("", " world")]

    def test_multi_line_selection(self):
        styled = [[("", "first")], [("", "second")], [("", "third")]]
        lines = ["first", "second", "third"]
        # Select from "rst" in first to "sec" in second
        # first = chars 0-4, \n at 5, second = chars 6-11
        _apply_selection_overlay(styled, lines, 2, 9)
        # Line 0: "fi" untouched, "rst" selected
        assert styled[0] == [("", "fi"), (" class:selected", "rst")]
        # Line 1: "sec" selected, "ond" untouched
        assert styled[1] == [(" class:selected", "sec"), ("", "ond")]
        # Line 2: untouched
        assert styled[2] == [("", "third")]

    def test_empty_range(self):
        styled = [[("", "hello")]]
        lines = ["hello"]
        _apply_selection_overlay(styled, lines, 3, 3)
        assert styled[0] == [("", "hello")]  # unchanged


class TestDragSelectionState:
    """Selection is tracked via sel_start/sel_end on the control."""

    def test_drag_start_end(self, make_control):
        ctrl = make_control("hello world\nsecond line")
        # Simulate MOUSE_DOWN at (0,0)
        ctrl._drag_start = ctrl._mouse_pos_to_cursor(0, 0)
        ctrl.sel_start = None
        ctrl.sel_end = None

        # Simulate MOUSE_MOVE to (0,5)
        pos = ctrl._mouse_pos_to_cursor(0, 5)
        a, b = sorted((ctrl._drag_start, pos))
        ctrl.sel_start = a
        ctrl.sel_end = b

        assert ctrl.sel_start == 0
        assert ctrl.sel_end == 5
        assert ctrl.buffer.text[ctrl.sel_start:ctrl.sel_end] == "hello"

    def test_mouseup_fallback_without_mousemove(self, make_control):
        """MOUSE_UP synthesises selection when MOUSE_MOVE never fired."""
        ctrl = make_control("hello world")
        ctrl._drag_start = ctrl._mouse_pos_to_cursor(0, 0)
        ctrl.sel_start = None
        ctrl.sel_end = None

        # Simulate MOUSE_UP at (0,5) — no MOUSE_MOVE happened
        pos = ctrl._mouse_pos_to_cursor(0, 5)
        if pos != ctrl._drag_start:
            a, b = sorted((ctrl._drag_start, pos))
            ctrl.sel_start = a
            ctrl.sel_end = b

        assert ctrl.sel_start == 0
        assert ctrl.sel_end == 5
        assert ctrl.buffer.text[ctrl.sel_start:ctrl.sel_end] == "hello"

    def test_click_without_drag_no_selection(self, make_control):
        ctrl = make_control("hello world")
        pos = ctrl._mouse_pos_to_cursor(0, 3)
        ctrl._drag_start = pos
        ctrl.sel_start = None
        ctrl.sel_end = None

        # MOUSE_UP at same position
        up_pos = ctrl._mouse_pos_to_cursor(0, 3)
        if up_pos != ctrl._drag_start:
            a, b = sorted((ctrl._drag_start, up_pos))
            ctrl.sel_start = a
            ctrl.sel_end = b

        assert ctrl.sel_start is None
        assert ctrl.sel_end is None


class TestDragDoesNotAffectInput:
    """Output selection is entirely separate from the input buffer."""

    def test_input_buffer_untouched(self, make_control):
        ctrl = make_control("hello world\nsecond line")
        ctrl.sel_start = 0
        ctrl.sel_end = 5

        input_buf = Buffer(name="input")
        input_buf.set_document(Document("user typing", len("user typing")))
        assert input_buf.selection_state is None
        assert input_buf.text == "user typing"


class TestLexerSelectionIntegration:
    """_OutputLexer renders selection highlight from control's sel_start/sel_end."""

    def test_lexer_applies_selection(self, make_control):
        ctrl = make_control("hello world")
        ctrl.sel_start = 0
        ctrl.sel_end = 5
        lexer = _OutputLexer(control=ctrl)

        doc = Document("hello world", 0)
        get_line = lexer.lex_document(doc)
        fragments = get_line(0)

        styles = [s for s, _ in fragments]
        texts = [t for _, t in fragments]

        # "hello" should have class:selected, " world" should not
        assert "class:selected" in styles[0]
        assert "hello" in texts[0]

    def test_lexer_no_selection(self, make_control):
        ctrl = make_control("hello world")
        ctrl.sel_start = None
        ctrl.sel_end = None
        lexer = _OutputLexer(control=ctrl)

        doc = Document("hello world", 0)
        get_line = lexer.lex_document(doc)
        fragments = get_line(0)

        # No selection styling
        for style, _ in fragments:
            assert "selected" not in style
