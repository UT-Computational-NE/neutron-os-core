"""CLI handler for `neut sense` — agentic signal ingestion.

Subcommands:
    neut sense ingest --source gitlab    Run gitlab diff extractor
    neut sense ingest --source voice     Process voice memos
    neut sense ingest --source freetext  Process text files in inbox
    neut sense ingest --source all       All extractors
    neut sense draft                     Synthesize → generate changelog
    neut sense status                    Show inbox/processed/draft status
    neut sense serve [--port] [--host]   HTTP inbox ingestion server
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Resolve paths relative to tools/agents/
_AGENTS_DIR = Path(__file__).resolve().parent.parent
INBOX_RAW = _AGENTS_DIR / "inbox" / "raw"
INBOX_PROCESSED = _AGENTS_DIR / "inbox" / "processed"
DRAFTS_DIR = _AGENTS_DIR / "drafts"
EXPORTS_DIR = _AGENTS_DIR.parent / "exports"


def cmd_status(args: argparse.Namespace) -> None:
    """Show what's in inbox, what's processed, what drafts exist."""
    print("neut sense — status")
    print()

    # Inbox raw
    raw_counts: dict[str, int] = {}
    if INBOX_RAW.exists():
        for child in INBOX_RAW.iterdir():
            if child.is_dir():
                files = list(child.rglob("*"))
                file_count = sum(1 for f in files if f.is_file() and f.name != ".gitkeep")
                if file_count:
                    raw_counts[child.name] = file_count
            elif child.is_file() and child.name != ".gitkeep":
                raw_counts.setdefault("root", 0)
                raw_counts["root"] += 1

    if raw_counts:
        print("Inbox (raw):")
        for folder, count in sorted(raw_counts.items()):
            print(f"  {folder}/: {count} file(s)")
    else:
        print("Inbox (raw): empty")

    # Processed
    processed_count = 0
    if INBOX_PROCESSED.exists():
        processed_count = sum(
            1 for f in INBOX_PROCESSED.rglob("*")
            if f.is_file() and f.name != ".gitkeep"
        )
    print(f"Processed: {processed_count} file(s)")

    # Drafts
    draft_count = 0
    latest_draft = None
    if DRAFTS_DIR.exists():
        drafts = sorted(DRAFTS_DIR.glob("changelog_*.md"), reverse=True)
        draft_count = len(drafts)
        if drafts:
            latest_draft = drafts[0].name

    print(f"Drafts: {draft_count} changelog(s)")
    if latest_draft:
        print(f"  Latest: {latest_draft}")

    # GitLab exports
    export_count = 0
    latest_export = None
    if EXPORTS_DIR.exists():
        exports = sorted(EXPORTS_DIR.glob("gitlab_export_*.json"), reverse=True)
        export_count = len(exports)
        if exports:
            latest_export = exports[0].name

    print(f"GitLab exports: {export_count} file(s)")
    if latest_export:
        print(f"  Latest: {latest_export}")

    # Config
    from tools.agents.sense.correlator import CONFIG_DIR, CONFIG_EXAMPLE_DIR

    config_dir = CONFIG_DIR if CONFIG_DIR.exists() else CONFIG_EXAMPLE_DIR
    people_path = config_dir / "people.md"
    init_path = config_dir / "initiatives.md"
    print(f"\nConfig: {config_dir}")
    print(f"  people.md: {'found' if people_path.exists() else 'missing'}")
    print(f"  initiatives.md: {'found' if init_path.exists() else 'missing'}")

    # Gateway
    from tools.agents.sense.gateway import Gateway

    gw = Gateway()
    print(f"  LLM gateway: {'available' if gw.available else 'no providers configured'}")


def cmd_ingest(args: argparse.Namespace) -> None:
    """Run extractors on inbox data."""
    from tools.agents.sense.correlator import Correlator
    from tools.agents.sense.gateway import Gateway
    from tools.agents.sense.models import Signal

    correlator = Correlator()
    gateway = Gateway()

    source = args.source
    all_signals: list[Signal] = []

    if source in ("gitlab", "all"):
        signals = _ingest_gitlab(correlator)
        all_signals.extend(signals)

    if source in ("voice", "all"):
        signals = _ingest_voice(gateway, correlator)
        all_signals.extend(signals)

    if source in ("freetext", "all"):
        signals = _ingest_freetext(gateway, correlator)
        all_signals.extend(signals)

    if source in ("transcript", "all"):
        signals = _ingest_transcripts(gateway, correlator)
        all_signals.extend(signals)

    # Save extracted signals
    if all_signals:
        INBOX_PROCESSED.mkdir(parents=True, exist_ok=True)
        from datetime import datetime, timezone

        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
        output = INBOX_PROCESSED / f"signals_{ts}.json"
        data = [s.to_dict() for s in all_signals]
        output.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"\nSaved {len(all_signals)} signal(s) to {output.name}")
    else:
        print("\nNo signals extracted.")


def _ingest_gitlab(correlator) -> list:
    """Run GitLab diff extractor."""
    from tools.agents.sense.extractors.gitlab_diff import GitLabDiffExtractor

    print("GitLab diff extractor")
    print("-" * 40)

    extractor = GitLabDiffExtractor()

    # Find the two most recent exports
    exports = sorted(EXPORTS_DIR.glob("gitlab_export_*.json"), reverse=True)

    if not exports:
        print("  No gitlab export files found in tools/exports/")
        print(f"  Run: python tools/gitlab_tracker_export.py --output-dir {EXPORTS_DIR}")
        return []

    current = exports[0]
    previous = exports[1] if len(exports) > 1 else None

    print(f"  Current: {current.name}")
    if previous:
        print(f"  Previous: {previous.name}")
        extraction = extractor.extract(current, previous=previous)
    else:
        print("  No previous export for diff — summarizing current only")
        extraction = extractor.extract(current)

    if extraction.errors:
        for err in extraction.errors:
            print(f"  Error: {err}")

    # Resolve people via correlator
    for signal in extraction.signals:
        signal.people = correlator.resolve_people(signal.people)
        signal.initiatives = correlator.resolve_initiatives(signal.initiatives)

    print(f"  Extracted {len(extraction.signals)} signal(s)")
    for s in extraction.signals[:5]:
        print(f"    [{s.signal_type}] {s.detail[:80]}")
    if len(extraction.signals) > 5:
        print(f"    ... and {len(extraction.signals) - 5} more")

    return extraction.signals


def _ingest_voice(gateway, correlator) -> list:
    """Process voice memos from inbox/raw/voice/."""
    from tools.agents.sense.extractors.voice import VoiceExtractor

    print("\nVoice extractor")
    print("-" * 40)

    voice_dir = INBOX_RAW / "voice"
    if not voice_dir.exists():
        print("  No voice directory found (inbox/raw/voice/)")
        return []

    extractor = VoiceExtractor()
    all_signals = []

    for audio_file in sorted(voice_dir.iterdir()):
        if extractor.can_handle(audio_file):
            print(f"  Processing: {audio_file.name}")
            extraction = extractor.extract(
                audio_file, gateway=gateway, correlator=correlator
            )
            if extraction.errors:
                for err in extraction.errors:
                    print(f"    Warning: {err}")
            all_signals.extend(extraction.signals)
            print(f"    Extracted {len(extraction.signals)} signal(s)")

    if not all_signals:
        print("  No voice memos found")

    return all_signals


def _ingest_freetext(gateway, correlator) -> list:
    """Process freetext files from inbox/raw/."""
    from tools.agents.sense.extractors.freetext import FreetextExtractor

    print("\nFreetext extractor")
    print("-" * 40)

    extractor = FreetextExtractor()
    all_signals = []

    # Process .md and .txt files directly in inbox/raw/
    for path in sorted(INBOX_RAW.iterdir()):
        if extractor.can_handle(path):
            print(f"  Processing: {path.name}")
            extraction = extractor.extract(
                path, gateway=gateway, correlator=correlator
            )
            if extraction.errors:
                for err in extraction.errors:
                    print(f"    Warning: {err}")
            all_signals.extend(extraction.signals)
            print(f"    Extracted {len(extraction.signals)} signal(s)")

    if not all_signals:
        print("  No freetext files found in inbox/raw/")

    return all_signals


def _ingest_transcripts(gateway, correlator) -> list:
    """Process meeting transcripts from inbox/raw/teams/."""
    from tools.agents.sense.extractors.transcript import TranscriptExtractor

    print("\nTranscript extractor")
    print("-" * 40)

    teams_dir = INBOX_RAW / "teams"
    if not teams_dir.exists():
        print("  No teams directory found (inbox/raw/teams/)")
        return []

    extractor = TranscriptExtractor()
    all_signals = []

    for path in sorted(teams_dir.iterdir()):
        if extractor.can_handle(path):
            print(f"  Processing: {path.name}")
            extraction = extractor.extract(
                path, gateway=gateway, correlator=correlator
            )
            if extraction.errors:
                for err in extraction.errors:
                    print(f"    Warning: {err}")
            all_signals.extend(extraction.signals)
            print(f"    Extracted {len(extraction.signals)} signal(s)")

    if not all_signals:
        print("  No transcripts found in inbox/raw/teams/")

    return all_signals


def cmd_serve(args: argparse.Namespace) -> None:
    """Start the HTTP inbox ingestion server."""
    from tools.agents.sense.serve import run_server

    run_server(host=args.host, port=args.port)


def cmd_draft(args: argparse.Namespace) -> None:
    """Synthesize all processed signals into a changelog draft."""
    from tools.agents.sense.models import Signal
    from tools.agents.sense.synthesizer import Synthesizer

    print("neut sense — draft synthesis")
    print("-" * 40)

    # Load all processed signals
    all_signals = []
    if INBOX_PROCESSED.exists():
        for signal_file in sorted(INBOX_PROCESSED.glob("signals_*.json")):
            try:
                data = json.loads(signal_file.read_text())
                for item in data:
                    all_signals.append(Signal.from_dict(item))
            except Exception as e:
                print(f"  Warning: Failed to load {signal_file.name}: {e}")

    if not all_signals:
        print("  No processed signals found. Run 'neut sense ingest' first.")
        return

    print(f"  Loaded {len(all_signals)} signal(s) from processed files")

    synthesizer = Synthesizer()
    changelog = synthesizer.synthesize(all_signals)

    changelog_path = synthesizer.write_changelog(changelog)
    summary_path = synthesizer.write_weekly_summary(changelog)

    print(f"\n  Changelog: {changelog_path}")
    print(f"  Summary:   {summary_path}")
    print(f"\n  {changelog.summary}")
    print(f"\n  Review the drafts, then move approved files to agents/approved/")


def main():
    parser = argparse.ArgumentParser(
        prog="neut sense",
        description="Agentic signal ingestion pipeline",
    )

    subparsers = parser.add_subparsers(dest="command")

    # ingest
    ingest_parser = subparsers.add_parser("ingest", help="Run extractors on inbox data")
    ingest_parser.add_argument(
        "--source",
        choices=["gitlab", "voice", "freetext", "transcript", "all"],
        default="all",
        help="Which source(s) to ingest (default: all)",
    )

    # draft
    subparsers.add_parser("draft", help="Synthesize signals into changelog draft")

    # status
    subparsers.add_parser("status", help="Show inbox/processed/draft status")

    # serve
    serve_parser = subparsers.add_parser("serve", help="HTTP inbox ingestion server")
    serve_parser.add_argument(
        "--port", type=int, default=8765, help="Port to listen on (default: 8765)"
    )
    serve_parser.add_argument(
        "--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)"
    )

    args = parser.parse_args()

    if args.command == "status":
        cmd_status(args)
    elif args.command == "ingest":
        cmd_ingest(args)
    elif args.command == "draft":
        cmd_draft(args)
    elif args.command == "serve":
        cmd_serve(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
