"""DocFlow core workflow engine — provider-agnostic orchestration.

This module NEVER imports any specific provider. It works exclusively
through the Provider ABCs, creating instances via DocFlowFactory.

Workflow: load config -> create providers via factory -> generate artifact
-> rewrite links via registry -> upload via storage -> update state -> notify
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from tools.docflow.config import DocFlowConfig, _state_dir, load_config
from tools.docflow.factory import DocFlowFactory
from tools.docflow.git_integration import get_git_context, check_branch_policy
from tools.docflow.models import DocumentState, LinkEntry, PublicationRecord
from tools.docflow.providers.base import (
    GenerationOptions,
    GenerationProvider,
    NotificationProvider,
    StorageProvider,
)
from tools.docflow.registry import LinkRegistry
from tools.docflow.state import StateStore


class DocFlowEngine:
    """Core workflow engine — orchestrates providers through ABCs only."""

    def __init__(self, config: DocFlowConfig | None = None):
        if config is None:
            config = load_config()
        self.config = config

        # Ensure provider registration by importing providers package
        try:
            import tools.docflow.providers  # noqa: F401
        except ImportError:
            pass

        # State and registry paths — use .neut/ subdir when outside a git repo
        state_root = _state_dir(config.repo_root)
        self.registry = LinkRegistry(state_root / ".doc-registry.json")
        self.state_store = StateStore(state_root / ".doc-state.json")

    def _create_generation_provider(self) -> GenerationProvider:
        """Create the configured generation provider."""
        return DocFlowFactory.create(
            "generation",
            self.config.generation.provider,
            self.config.generation.settings,
        )

    def _create_storage_provider(
        self, override: str | None = None
    ) -> StorageProvider:
        """Create the configured (or overridden) storage provider."""
        name = override or self.config.storage.provider
        # Preserve configured settings when override matches configured provider
        if override and override != self.config.storage.provider:
            settings = {}
        else:
            settings = self.config.storage.settings
        return DocFlowFactory.create("storage", name, settings)

    def _create_notification_provider(self) -> NotificationProvider:
        """Create the configured notification provider."""
        return DocFlowFactory.create(
            "notification",
            self.config.notification.provider,
            self.config.notification.settings,
        )

    def generate(
        self,
        source_path: Path,
        output_dir: Path | None = None,
        options: GenerationOptions | None = None,
    ) -> Path:
        """Generate an artifact from a markdown source file.

        This is a local operation — no upload, no state change.
        """
        gen = self._create_generation_provider()
        ext = gen.get_output_extension()

        if output_dir is None:
            output_dir = self.config.repo_root / "docs" / "_tools" / "generated"

        # Preserve directory structure relative to docs/
        try:
            rel = source_path.relative_to(self.config.repo_root / "docs")
            output_path = output_dir / rel.with_suffix(ext)
        except ValueError:
            output_path = output_dir / source_path.with_suffix(ext).name

        if options is None:
            options = GenerationOptions(
                toc=True,
                toc_depth=3,
            )

        print(f"Generating {output_path.name}...", flush=True)
        result = gen.generate(source_path, output_path, options)

        if result.warnings:
            for w in result.warnings:
                print(f"  Warning: {w}", file=sys.stderr)

        # Rewrite links if we have a registry
        link_map = self.registry.build_link_map()
        if link_map:
            print(f"  Rewriting {len(link_map)} cross-document links...", flush=True)
            gen.rewrite_links(result.output_path, link_map)

        print(
            f"  Generated: {result.output_path} "
            f"({result.size_bytes / 1024:.1f} KB)",
            flush=True,
        )
        return result.output_path

    def publish(
        self,
        source_path: Path,
        storage_override: str | None = None,
        draft: bool = False,
    ) -> PublicationRecord | None:
        """Full publish workflow: generate + upload + update state.

        Args:
            source_path: Path to .md file.
            storage_override: Override the configured storage provider.
            draft: If True, publish as draft (any branch allowed).
        """
        # Git context
        git_ctx = get_git_context(self.config.repo_root)

        # When git is unavailable, skip all branch policy and dirty-tree checks
        if git_ctx.git_available:
            policy = check_branch_policy(
                git_ctx.current_branch,
                self.config.git.publish_branches,
                self.config.git.draft_branches,
            )

            if not draft and policy == "local":
                print(
                    f"Branch '{git_ctx.current_branch}' only allows local generation. "
                    f"Use --draft or switch to a publish branch.",
                    file=sys.stderr,
                )
                return None

            if not draft and policy == "draft":
                print(
                    f"Branch '{git_ctx.current_branch}' only allows draft publishing.",
                    file=sys.stderr,
                )
                draft = True

            # Check for dirty state
            if self.config.git.require_clean and git_ctx.is_dirty:
                print(
                    "Working tree has uncommitted changes. "
                    "Commit or stash before publishing.",
                    file=sys.stderr,
                )
                return None

        # Generate artifact
        artifact_path = self.generate(source_path)

        # Upload
        storage = self._create_storage_provider(storage_override)
        gen_provider = self._create_generation_provider()

        # Determine doc_id and destination
        doc_id = source_path.stem
        try:
            rel = source_path.relative_to(self.config.repo_root)
            source_rel = str(rel)
        except ValueError:
            source_rel = source_path.name

        # Check existing state for versioning (consider both published and draft versions)
        existing = self.state_store.get(doc_id)
        if existing:
            latest_version = "v0"
            if existing.published:
                latest_version = existing.published.version
            if existing.active_draft:
                draft_num = int(existing.active_draft.version.lstrip("v"))
                pub_num = int(latest_version.lstrip("v"))
                if draft_num > pub_num:
                    latest_version = existing.active_draft.version
            version_num = int(latest_version.lstrip("v")) + 1
            version = f"v{version_num}"
        else:
            version = "v1"

        destination = f"{doc_id}{gen_provider.get_output_extension()}"

        metadata = {
            "version": version,
            "commit_sha": git_ctx.commit_sha,
            "branch": git_ctx.current_branch,
            "source": source_rel,
            "draft": draft,
        }

        print(f"Uploading to {self.config.storage.provider}...", flush=True)
        upload_result = storage.upload(artifact_path, destination, metadata)
        print(f"  Published: {upload_result.canonical_url}", flush=True)

        # Create publication record
        now = datetime.now(timezone.utc).isoformat()
        record = PublicationRecord(
            storage_id=upload_result.storage_id,
            url=upload_result.canonical_url,
            version=version,
            published_at=now,
            commit_sha=git_ctx.commit_sha,
            generation_provider=self.config.generation.provider,
            storage_provider=storage_override or self.config.storage.provider,
        )

        # Update state
        if existing:
            doc_state = existing
        else:
            doc_state = DocumentState(doc_id=doc_id, source_path=source_rel)

        if draft:
            doc_state.status = "draft"
            doc_state.active_draft = record
            doc_state.draft_history.append(record)
        else:
            doc_state.status = "published"
            doc_state.published = record

        doc_state.last_commit = git_ctx.commit_sha
        doc_state.last_branch = git_ctx.current_branch

        self.state_store.update(doc_state)

        # Update link registry
        link_entry = LinkEntry(
            doc_id=doc_id,
            source_path=source_rel,
            published_url=upload_result.canonical_url if not draft else "",
            draft_url=upload_result.canonical_url if draft else None,
            storage_id=upload_result.storage_id,
            last_published=now,
            version=version,
            commit_sha=git_ctx.commit_sha,
        )
        self.registry.update(link_entry)

        # Notify
        try:
            notifier = self._create_notification_provider()
            action = "Draft published" if draft else "Published"
            notifier.send(
                recipients=[],
                subject=f"{action}: {doc_id} ({version})",
                body=f"URL: {upload_result.canonical_url}\nSource: {source_rel}",
            )
        except Exception:
            pass  # Non-fatal

        return record

    def status(self, source_path: Path | None = None) -> list[DocumentState]:
        """Get status of tracked documents."""
        if source_path:
            doc_id = source_path.stem
            doc = self.state_store.get(doc_id)
            return [doc] if doc else []
        return self.state_store.list_by_status()

    def check_links(self) -> dict[str, list[str]]:
        """Verify all cross-document links resolve."""
        return self.registry.check_links(self.config.repo_root / "docs")

    def diff(self) -> list[str]:
        """Show docs changed since last publish."""
        from tools.docflow.git_integration import get_changed_docs

        # Find the earliest commit SHA from published docs
        earliest_sha = None
        for doc in self.state_store.list_by_status():
            if doc.last_commit and (earliest_sha is None):
                earliest_sha = doc.last_commit

        if earliest_sha is None:
            earliest_sha = "HEAD~10"  # Default fallback

        return get_changed_docs(self.config.repo_root, earliest_sha)

    def list_providers(self) -> dict[str, list[str]]:
        """List all registered providers."""
        return DocFlowFactory.available()
