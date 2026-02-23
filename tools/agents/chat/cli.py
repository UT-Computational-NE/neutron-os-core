"""CLI handler for `neut chat` — interactive agent with streaming.

Usage:
    neut chat                         Start a new chat session
    neut chat --resume <id>           Resume an existing session
    neut chat --context <file>        Load additional context from file
    neut chat --no-stream             Disable streaming output
    neut chat --model <name>          Override LLM model
    neut chat --provider <name>       Override LLM provider

The REPL reads user input, passes it through the ChatAgent
(which handles native tool calling and approval gates), and streams responses.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from tools.agents.chat.agent import ChatAgent
from tools.agents.chat.renderer import (
    render_message,
    render_welcome,
    stream_text,
    render_thinking_spinner,
)
from tools.agents.chat.commands import (
    cmd_help,
    cmd_status,
    cmd_sense,
    cmd_doc,
    cmd_sessions,
    cmd_resume,
    cmd_new,
)
from tools.agents.orchestrator.bus import EventBus
from tools.agents.orchestrator.session import Session, SessionStore
from tools.agents.sense.gateway import Gateway
from tools.agents.setup.renderer import _c, _Colors, _use_color


def run_repl(agent: ChatAgent, store: SessionStore, stream: bool = True) -> None:
    """Run the interactive REPL loop."""
    render_welcome(gateway=agent.gateway)

    # Set up streaming renderer
    if stream:
        agent.set_renderer(stream_text)

    multiline_mode = False
    multiline_buffer: list[str] = []

    while True:
        try:
            if multiline_mode:
                prompt = "...> " if not _use_color() else _c(_Colors.DIM, "...> ")
            else:
                prompt = "you> " if not _use_color() else _c(_Colors.BRIGHT_BLUE, "you> ")

            user_input = input(prompt)
        except KeyboardInterrupt:
            if multiline_mode:
                multiline_mode = False
                multiline_buffer.clear()
                print()
                continue
            print()  # New prompt on Ctrl+C
            continue
        except EOFError:
            print(f"\n  {_c(_Colors.DIM, 'Goodbye.')}")
            break

        # Multi-line mode toggle
        if user_input.strip() == '"""':
            if multiline_mode:
                # End multi-line mode
                multiline_mode = False
                user_input = "\n".join(multiline_buffer)
                multiline_buffer.clear()
            else:
                # Start multi-line mode
                multiline_mode = True
                multiline_buffer.clear()
                print(f"  {_c(_Colors.DIM, 'Multi-line mode. Type')}"
                      f" {_c(_Colors.CYAN, '\"\"\"')}"
                      f" {_c(_Colors.DIM, 'to send.')}")
                continue

        if multiline_mode:
            multiline_buffer.append(user_input)
            continue

        user_input = user_input.strip()
        if not user_input:
            continue

        # --- Slash commands ---
        if user_input.startswith("/"):
            handled = _handle_slash_command(user_input, agent, store)
            if handled == "exit":
                break
            if handled:
                print(handled)
            continue

        # Legacy exit commands
        if user_input.lower() in ("exit", "quit"):
            print(f"  {_c(_Colors.DIM, 'Goodbye.')}")
            break

        # --- Agent turn ---
        try:
            if stream and agent.gateway.available:
                print()  # Blank line before response
                response = agent.turn(user_input, stream=True)
                print()  # Blank line after response
            else:
                with render_thinking_spinner("Thinking"):
                    response = agent.turn(user_input, stream=False)
                render_message("assistant", response)
        except KeyboardInterrupt:
            print(f"\n  {_c(_Colors.DIM, '[interrupted]')}")
            continue

        # Auto-save after each turn
        store.save(agent.session)


def _handle_slash_command(
    command: str, agent: ChatAgent, store: SessionStore,
) -> Optional[str]:
    """Dispatch a slash command. Returns output text or 'exit'."""
    parts = command.split(maxsplit=1)
    cmd = parts[0].lower()
    arg = parts[1].strip() if len(parts) > 1 else ""

    if cmd in ("/exit", "/quit"):
        print(f"  {_c(_Colors.DIM, 'Goodbye.')}")
        return "exit"

    if cmd == "/help":
        return cmd_help()

    if cmd == "/status":
        return cmd_status(agent)

    if cmd == "/sense":
        return cmd_sense()

    if cmd == "/doc":
        return cmd_doc()

    if cmd == "/sessions":
        return cmd_sessions(store)

    if cmd == "/resume":
        if not arg:
            return f"\n  Usage: /resume <session_id>\n"
        return cmd_resume(arg, store, agent)

    if cmd == "/new":
        return cmd_new(store, agent)

    return f"\n  Unknown command: {cmd}. Type /help for available commands.\n"


def main():
    parser = argparse.ArgumentParser(
        prog="neut chat",
        description="Interactive agent with tool calling",
    )
    parser.add_argument(
        "--resume", metavar="SESSION_ID",
        help="Resume an existing chat session",
    )
    parser.add_argument(
        "--context", metavar="FILE",
        help="Load additional context from a file",
    )
    parser.add_argument(
        "--no-stream", action="store_true",
        help="Disable streaming output",
    )
    parser.add_argument(
        "--model", metavar="NAME",
        help="Override LLM model for this session",
    )
    parser.add_argument(
        "--provider", metavar="NAME",
        help="Override LLM provider for this session",
    )

    args = parser.parse_args()

    store = SessionStore()
    gateway = Gateway()
    bus = EventBus()

    # Resume or create session
    session: Optional[Session] = None
    if args.resume:
        session = store.load(args.resume)
        if session is None:
            print(f"Session '{args.resume}' not found.")
            sys.exit(1)
        print(f"  Resuming session {args.resume} ({len(session.messages)} messages)")
    else:
        context = {}
        if args.context:
            ctx_path = Path(args.context)
            if ctx_path.exists():
                context["loaded_file"] = str(ctx_path)
                context["file_content"] = ctx_path.read_text(encoding="utf-8")[:4000]
            else:
                print(f"Context file not found: {args.context}")
                sys.exit(1)
        session = store.create(context=context)

    agent = ChatAgent(gateway=gateway, bus=bus, session=session)
    stream = not args.no_stream

    try:
        run_repl(agent, store, stream=stream)
    finally:
        store.save(agent.session)


if __name__ == "__main__":
    main()
