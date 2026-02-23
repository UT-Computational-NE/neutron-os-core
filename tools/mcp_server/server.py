"""MCP server exposing neut tools to Claude Code, Cursor, and other MCP clients.

Each tool delegates to execute_tool() from the chat tool registry.
No approval gate — MCP clients handle their own confirmation UX.

Usage:
    python -m tools.mcp_server.server
"""

from __future__ import annotations

import asyncio
import json
import sys
import os

# Ensure repo root is on sys.path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _check_mcp_available() -> bool:
    """Check if the mcp package is installed."""
    try:
        import mcp  # noqa: F401
        return True
    except ImportError:
        return False


def create_server():
    """Create and configure the MCP server with all neut tools."""
    from mcp.server import Server
    from mcp.types import TextContent, Tool

    server = Server("neutron-os")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """Dynamically list all available tools from the registry."""
        from tools.agents.chat.tools import get_all_tools

        result = []
        for tool_def in get_all_tools().values():
            result.append(Tool(
                name=tool_def.name,
                description=tool_def.description,
                inputSchema=tool_def.parameters or {"type": "object", "properties": {}},
            ))
        return result

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        """Execute a tool by name and return the result as JSON."""
        from tools.agents.chat.tools import execute_tool, get_all_tools

        all_tools = get_all_tools()
        if name not in all_tools:
            return [TextContent(
                type="text",
                text=json.dumps({"error": f"Unknown tool: {name}"}, indent=2),
            )]

        try:
            result = execute_tool(name, arguments or {})
        except Exception as e:
            result = {"error": str(e)}

        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2),
        )]

    return server


async def run_stdio():
    """Run the MCP server over stdio transport."""
    from mcp.server.stdio import stdio_server

    server = create_server()

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    """Entry point for the MCP server."""
    if not _check_mcp_available():
        print(
            "MCP server requires the 'mcp' package.\n"
            "Install it with: pip install 'neutron-os[mcp]'",
            file=sys.stderr,
        )
        sys.exit(1)

    asyncio.run(run_stdio())


if __name__ == "__main__":
    main()
