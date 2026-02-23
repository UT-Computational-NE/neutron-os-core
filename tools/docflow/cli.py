"""CLI handler for `neut doc` / `neut docflow` — document lifecycle management.

Subcommands:
    neut doc publish <file>              Generate + publish to configured storage
    neut doc publish --draft <file>      Draft with review period
    neut doc publish --all --changed-only Batch publish changed docs
    neut doc generate <file>             Generate locally only (no upload)
    neut doc status                      Show all doc states
    neut doc status <file>               Single doc status
    neut doc check-links                 Verify cross-doc links resolve
    neut doc diff                        Show docs changed since last publish
    neut doc providers                   List available providers
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def cmd_publish(args: argparse.Namespace) -> None:
    """Publish document(s) to configured storage."""
    from tools.docflow.engine import DocFlowEngine

    engine = DocFlowEngine()

    if args.all:
        # Batch publish
        if args.changed_only:
            changed = engine.diff()
            if not changed:
                print("No documents changed since last publish.")
                return
            print(f"Found {len(changed)} changed document(s):")
            for doc in changed:
                print(f"  {doc}")
                source = engine.config.repo_root / doc
                if source.exists():
                    engine.publish(
                        source,
                        storage_override=args.storage,
                        draft=args.draft,
                    )
        else:
            print("Use --changed-only with --all to avoid publishing everything.")
            sys.exit(1)
    elif args.file:
        source = Path(args.file).resolve()
        if not source.exists():
            print(f"File not found: {args.file}")
            sys.exit(1)
        engine.publish(
            source,
            storage_override=args.storage,
            draft=args.draft,
        )
    else:
        print("Specify a file or use --all --changed-only")
        sys.exit(1)


def cmd_generate(args: argparse.Namespace) -> None:
    """Generate artifact locally without uploading."""
    from tools.docflow.engine import DocFlowEngine

    source = Path(args.file).resolve()
    if not source.exists():
        print(f"File not found: {args.file}")
        sys.exit(1)

    engine = DocFlowEngine()
    output = engine.generate(source)
    print(f"\nGenerated: {output}")


def cmd_status(args: argparse.Namespace) -> None:
    """Show document status."""
    from tools.docflow.engine import DocFlowEngine

    engine = DocFlowEngine()

    if args.file:
        source = Path(args.file).resolve()
        docs = engine.status(source)
    else:
        docs = engine.status()

    if not docs:
        print("No tracked documents.")
        return

    print(f"{'Doc ID':<35} {'Status':<12} {'Version':<8} {'Provider':<15} {'Last Published'}")
    print("-" * 100)

    for doc in docs:
        version = ""
        provider = ""
        published = ""

        if doc.published:
            version = doc.published.version
            provider = doc.published.storage_provider
            published = doc.published.published_at[:19]
        elif doc.active_draft:
            version = doc.active_draft.version
            provider = doc.active_draft.storage_provider
            published = doc.active_draft.published_at[:19]

        print(f"{doc.doc_id:<35} {doc.status:<12} {version:<8} {provider:<15} {published}")

    print(f"\nTotal: {len(docs)} document(s)")


def cmd_check_links(args: argparse.Namespace) -> None:
    """Verify cross-document links."""
    from tools.docflow.engine import DocFlowEngine

    engine = DocFlowEngine()
    results = engine.check_links()

    valid = results.get("valid", [])
    missing = results.get("missing", [])

    if valid:
        print(f"Valid links: {len(valid)}")
        for path in valid:
            print(f"  [ok] {path}")

    if missing:
        print(f"\nMissing source files: {len(missing)}")
        for path in missing:
            print(f"  [!!] {path}")

    if not valid and not missing:
        print("No documents in registry. Publish some docs first.")

    total = len(valid) + len(missing)
    if total > 0:
        print(f"\n{len(valid)}/{total} links valid")


def cmd_diff(args: argparse.Namespace) -> None:
    """Show documents changed since last publish."""
    from tools.docflow.engine import DocFlowEngine

    engine = DocFlowEngine()
    changed = engine.diff()

    if not changed:
        print("No documents changed since last publish.")
    else:
        print(f"Changed since last publish ({len(changed)} files):")
        for doc in changed:
            print(f"  {doc}")


def cmd_providers(args: argparse.Namespace) -> None:
    """List all available providers."""
    # Ensure providers are registered
    try:
        import tools.docflow.providers  # noqa: F401
    except ImportError:
        pass

    from tools.docflow.factory import DocFlowFactory
    from tools.docflow.config import load_config

    config = load_config()
    all_providers = DocFlowFactory.available()

    print("DocFlow Providers")
    print("=" * 50)

    category_labels = {
        "generation": "Generation (md -> artifact)",
        "storage": "Storage (upload & URLs)",
        "feedback": "Feedback (reviewer comments)",
        "notification": "Notifications (alerts)",
        "embedding": "Embedding (RAG indexing)",
    }

    active_map = {
        "generation": config.generation.provider,
        "storage": config.storage.provider,
        "feedback": config.feedback.provider,
        "notification": config.notification.provider,
        "embedding": config.embedding.provider if config.embedding_enabled else None,
    }

    for category, names in all_providers.items():
        label = category_labels.get(category, category)
        active = active_map.get(category, "")
        print(f"\n{label}:")
        if names:
            for name in names:
                marker = " *" if name == active else ""
                print(f"  - {name}{marker}")
        else:
            print("  (none registered)")

    print("\n* = active (from .doc-workflow.yaml)")


def main():
    parser = argparse.ArgumentParser(
        prog="neut doc",
        description="Document lifecycle management",
    )

    subparsers = parser.add_subparsers(dest="command")

    # publish
    pub_parser = subparsers.add_parser("publish", help="Generate + publish to storage")
    pub_parser.add_argument("file", nargs="?", help="Markdown file to publish")
    pub_parser.add_argument("--draft", action="store_true", help="Publish as draft")
    pub_parser.add_argument("--all", action="store_true", help="Batch publish")
    pub_parser.add_argument("--changed-only", action="store_true", help="Only changed docs")
    pub_parser.add_argument("--storage", help="Override storage provider (e.g., 'local')")

    # generate
    gen_parser = subparsers.add_parser("generate", help="Generate locally only")
    gen_parser.add_argument("file", help="Markdown file to generate")

    # status
    stat_parser = subparsers.add_parser("status", help="Show document status")
    stat_parser.add_argument("file", nargs="?", help="Specific file (optional)")

    # check-links
    subparsers.add_parser("check-links", help="Verify cross-doc links")

    # diff
    subparsers.add_parser("diff", help="Show changed docs since last publish")

    # providers
    subparsers.add_parser("providers", help="List available providers")

    args = parser.parse_args()

    if args.command == "publish":
        cmd_publish(args)
    elif args.command == "generate":
        cmd_generate(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "check-links":
        cmd_check_links(args)
    elif args.command == "diff":
        cmd_diff(args)
    elif args.command == "providers":
        cmd_providers(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
