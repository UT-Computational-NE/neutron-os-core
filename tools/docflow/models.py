"""Core data models for DocFlow — provider-agnostic document state."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class Comment:
    """Reviewer comment extracted from a published artifact."""

    comment_id: str
    author: str
    timestamp: str  # ISO 8601
    text: str
    context: str | None = None  # Text range the comment is anchored to
    resolved: bool = False
    replies: list[Comment] = field(default_factory=list)
    source: str = ""  # Provider name that produced this comment

    def to_dict(self) -> dict:
        return {
            "comment_id": self.comment_id,
            "author": self.author,
            "timestamp": self.timestamp,
            "text": self.text,
            "context": self.context,
            "resolved": self.resolved,
            "replies": [r.to_dict() for r in self.replies],
            "source": self.source,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Comment:
        replies = [cls.from_dict(r) for r in data.get("replies", [])]
        return cls(
            comment_id=data.get("comment_id", ""),
            author=data.get("author", ""),
            timestamp=data.get("timestamp", ""),
            text=data.get("text", ""),
            context=data.get("context"),
            resolved=data.get("resolved", False),
            replies=replies,
            source=data.get("source", ""),
        )


@dataclass
class LinkEntry:
    """Registry entry mapping a document to its published URL."""

    doc_id: str  # e.g., "experiment-manager-prd"
    source_path: str  # e.g., "docs/prd/experiment-manager-prd.md"
    published_url: str  # From StorageProvider.get_canonical_url()
    draft_url: str | None = None
    storage_id: str = ""  # Provider-specific reference
    last_published: str = ""  # ISO 8601
    version: str = "v1"
    commit_sha: str = ""

    def to_dict(self) -> dict:
        return {
            "doc_id": self.doc_id,
            "source_path": self.source_path,
            "published_url": self.published_url,
            "draft_url": self.draft_url,
            "storage_id": self.storage_id,
            "last_published": self.last_published,
            "version": self.version,
            "commit_sha": self.commit_sha,
        }

    @classmethod
    def from_dict(cls, data: dict) -> LinkEntry:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class PublicationRecord:
    """Record of a single publication event."""

    storage_id: str
    url: str
    version: str
    published_at: str  # ISO 8601
    commit_sha: str
    generation_provider: str  # Which provider generated this artifact
    storage_provider: str  # Which provider stores this artifact

    def to_dict(self) -> dict:
        return {
            "storage_id": self.storage_id,
            "url": self.url,
            "version": self.version,
            "published_at": self.published_at,
            "commit_sha": self.commit_sha,
            "generation_provider": self.generation_provider,
            "storage_provider": self.storage_provider,
        }

    @classmethod
    def from_dict(cls, data: dict) -> PublicationRecord:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class DocumentState:
    """Full state of a tracked document in the DocFlow lifecycle."""

    doc_id: str
    source_path: str

    # Lifecycle
    status: str = "local"  # local, draft, published, archived

    # Publication records
    published: PublicationRecord | None = None
    active_draft: PublicationRecord | None = None
    draft_history: list[PublicationRecord] = field(default_factory=list)

    # Git tracking
    last_commit: str = ""
    last_branch: str = ""

    # Feedback
    pending_comments: list[Comment] = field(default_factory=list)

    # Stakeholders
    stakeholders: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "doc_id": self.doc_id,
            "source_path": self.source_path,
            "status": self.status,
            "published": self.published.to_dict() if self.published else None,
            "active_draft": self.active_draft.to_dict() if self.active_draft else None,
            "draft_history": [d.to_dict() for d in self.draft_history],
            "last_commit": self.last_commit,
            "last_branch": self.last_branch,
            "pending_comments": [c.to_dict() for c in self.pending_comments],
            "stakeholders": self.stakeholders,
        }

    @classmethod
    def from_dict(cls, data: dict) -> DocumentState:
        pub = PublicationRecord.from_dict(data["published"]) if data.get("published") else None
        draft = PublicationRecord.from_dict(data["active_draft"]) if data.get("active_draft") else None
        history = [PublicationRecord.from_dict(d) for d in data.get("draft_history", [])]
        comments = [Comment.from_dict(c) for c in data.get("pending_comments", [])]

        return cls(
            doc_id=data["doc_id"],
            source_path=data["source_path"],
            status=data.get("status", "local"),
            published=pub,
            active_draft=draft,
            draft_history=history,
            last_commit=data.get("last_commit", ""),
            last_branch=data.get("last_branch", ""),
            pending_comments=comments,
            stakeholders=data.get("stakeholders", []),
        )
