"""Slash command implementations for neut chat.

Each command is a standalone function for testability.
Commands return a string to display, or None for no output.
"""

from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

from tools.agents.setup.renderer import _c, _Colors, _use_color

if TYPE_CHECKING:
    from tools.agents.chat.agent import ChatAgent
    from tools.agents.orchestrator.session import SessionStore


def cmd_help() -> str:
    """Return the help text."""
    lines = [
        "",
        f"  {_c(_Colors.BOLD, 'Commands:')}",
        f"  {_c(_Colors.CYAN, '/help')}       Show this help",
        f"  {_c(_Colors.CYAN, '/status')}     Session info, gateway, message count",
        f"  {_c(_Colors.CYAN, '/sense')}      Sense pipeline status",
        f"  {_c(_Colors.CYAN, '/doc')}        Document status",
        f"  {_c(_Colors.CYAN, '/sessions')}   List saved sessions",
        f"  {_c(_Colors.CYAN, '/resume')} <id> Load a different session",
        f"  {_c(_Colors.CYAN, '/new')}        Start a fresh session",
        f"  {_c(_Colors.CYAN, '/exit')}       Save and exit",
        "",
        f"  {_c(_Colors.DIM, 'Tip: Use triple quotes')} {_c(_Colors.CYAN, '\"\"\"')} "
        f"{_c(_Colors.DIM, 'for multi-line input.')}",
        "",
    ]
    return "\n".join(lines)


def cmd_status(agent: ChatAgent) -> str:
    """Return session status info."""
    session = agent.session
    provider = agent.gateway.active_provider
    if provider:
        gw_status = f"{provider.name} ({provider.model})"
    else:
        gw_status = "stub mode (no LLM configured)"

    lines = [
        "",
        f"  {_c(_Colors.BOLD, 'Session:')}  {session.session_id}",
        f"  {_c(_Colors.BOLD, 'Messages:')} {len(session.messages)}",
        f"  {_c(_Colors.BOLD, 'Gateway:')}  {gw_status}",
    ]
    if session.context:
        ctx_keys = list(session.context.keys())
        lines.append(f"  {_c(_Colors.BOLD, 'Context:')}  {ctx_keys}")
    lines.append("")
    return "\n".join(lines)


def cmd_sense() -> str:
    """Return sense pipeline status."""
    from tools.agents.chat.tools import execute_tool
    result = execute_tool("sense_status", {})
    lines = [""]
    lines.append(f"  {_c(_Colors.BOLD, 'Sense Pipeline Status')}")
    inbox = result.get("inbox_raw", {})
    if inbox:
        for source, count in inbox.items():
            lines.append(f"  inbox/{source}: {count} files")
    else:
        lines.append("  inbox: empty")
    lines.append(f"  processed: {result.get('processed', 0)}")
    lines.append(f"  drafts: {result.get('drafts', 0)}")
    lines.append("")
    return "\n".join(lines)


def cmd_doc() -> str:
    """Return document status."""
    from tools.agents.chat.tools import execute_tool
    result = execute_tool("query_docs", {})
    lines = [""]
    lines.append(f"  {_c(_Colors.BOLD, 'Document Status')}")
    docs = result.get("documents", [])
    if not docs:
        lines.append("  No tracked documents.")
    else:
        for d in docs:
            status = d.get("status", "unknown")
            version = d.get("version", "")
            lines.append(f"  {d['doc_id']}: {status} ({version})")
    lines.append("")
    return "\n".join(lines)


def cmd_sessions(store: SessionStore) -> str:
    """Return formatted list of sessions."""
    session_ids = store.list_sessions()
    if not session_ids:
        return "\n  No saved sessions.\n"

    lines = ["", f"  {_c(_Colors.BOLD, 'Saved sessions:')}"]
    for sid in session_ids[:10]:
        session = store.load(sid)
        if session:
            msg_count = len(session.messages)
            updated = session.updated_at[:10] if session.updated_at else ""
            lines.append(
                f"  {_c(_Colors.CYAN, sid)}  "
                f"{msg_count} messages  "
                f"{_c(_Colors.DIM, updated)}"
            )
        else:
            lines.append(f"  {_c(_Colors.CYAN, sid)}")
    lines.append("")
    return "\n".join(lines)


def cmd_resume(
    session_id: str,
    store: SessionStore,
    agent: ChatAgent,
) -> str:
    """Resume a session by ID. Returns status message."""
    session = store.load(session_id)
    if session is None:
        return f"\n  {_c(_Colors.RED, 'Session not found:')} {session_id}\n"

    agent.session = session
    return (
        f"\n  Resumed session {_c(_Colors.CYAN, session_id)} "
        f"({len(session.messages)} messages)\n"
    )


def cmd_new(store: SessionStore, agent: ChatAgent) -> str:
    """Start a fresh session. Returns status message."""
    # Save current session first
    store.save(agent.session)
    old_id = agent.session.session_id

    # Create new session
    new_session = store.create()
    agent.session = new_session

    return (
        f"\n  Saved {_c(_Colors.DIM, old_id)}, "
        f"started {_c(_Colors.CYAN, new_session.session_id)}\n"
    )


# ---------------------------------------------------------------------------
# Dispatch table
# ---------------------------------------------------------------------------

SLASH_COMMANDS = {
    "/help": "Show available commands",
    "/status": "Session info, gateway, message count",
    "/sense": "Sense pipeline status",
    "/doc": "Document status",
    "/sessions": "List saved sessions",
    "/resume": "Load a different session (/resume <id>)",
    "/new": "Start a fresh session",
    "/exit": "Save and exit",
}
