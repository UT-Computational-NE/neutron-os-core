#!/usr/bin/env python3
"""
neut — Neutron OS CLI dispatcher (Python prototype)

Routes subcommands to their respective handlers:
  neut sense ...     → tools/agents/sense/cli.py
  neut doc ...       → tools/docflow/cli.py
  neut docflow ...   → tools/docflow/cli.py  (alias)

The production neut CLI will be Rust (see docs/specs/neut-cli-spec.md).
This Python entry point serves developer tooling during early development.

Usage:
    python tools/neut_cli.py <subcommand> [args...]
    python -m tools.neut_cli <subcommand> [args...]

Installation:
    alias neut="python /path/to/tools/neut_cli.py"
"""

import sys
import os

# Ensure repo root is on sys.path so imports resolve
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _load_dotenv():
    """Load .env file from repo root if it exists (no external deps)."""
    env_path = os.path.join(REPO_ROOT, ".env")
    if not os.path.isfile(env_path):
        return
    try:
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip()
                # Don't overwrite explicitly set env vars
                if key and key not in os.environ:
                    os.environ[key] = value
    except OSError:
        pass


_load_dotenv()


SUBCOMMANDS = {
    "setup": "tools.agents.setup.cli",
    "sense": "tools.agents.sense.cli",
    "doc": "tools.docflow.cli",
    "docflow": "tools.docflow.cli",
    "chat": "tools.agents.chat.cli",
    "serve-mcp": "tools.mcp_server.server",
}


def print_usage():
    print("neut — Neutron OS CLI (Python prototype)")
    print()
    print("Usage: neut <subcommand> [args...]")
    print()
    print("Subcommands:")
    print("  setup     Interactive onboarding wizard")
    print("  sense     Agentic signal ingestion pipeline")
    print("  doc       Document lifecycle management (alias: docflow)")
    print("  chat      Interactive agent with tool calling")
    print("  serve-mcp Start the MCP server for IDE integration")
    print()
    print("Examples:")
    print("  neut sense status")
    print("  neut sense ingest --source gitlab")
    print("  neut doc publish docs/prd/foo.md")
    print("  neut doc providers")


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    subcommand = sys.argv[1]

    if subcommand in ("-h", "--help", "help"):
        print_usage()
        sys.exit(0)

    module_path = SUBCOMMANDS.get(subcommand)
    if not module_path:
        print(f"neut: unknown subcommand '{subcommand}'")
        print(f"Run 'neut --help' for usage.")
        sys.exit(1)

    # Remove the subcommand from argv so the handler sees only its own args
    sys.argv = [f"neut {subcommand}"] + sys.argv[2:]

    try:
        import importlib
        module = importlib.import_module(module_path)
        module.main()
    except ImportError as e:
        print(f"neut: failed to load {subcommand} handler: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        sys.exit(130)


if __name__ == "__main__":
    main()
