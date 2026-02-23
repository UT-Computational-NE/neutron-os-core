"""Document state persistence — tracks lifecycle status for all documents.

Persists to .doc-state.json in repo root. Each document's state includes
its lifecycle position, publication records, and pending feedback.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from tools.docflow.models import DocumentState


class StateStore:
    """Manages document lifecycle state persistence."""

    def __init__(self, state_path: Path):
        self.path = state_path
        self.documents: dict[str, DocumentState] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            for item in data.get("documents", []):
                doc = DocumentState.from_dict(item)
                self.documents[doc.doc_id] = doc
        except (json.JSONDecodeError, KeyError):
            pass

    def save(self) -> None:
        """Persist state to disk."""
        data = {
            "documents": [d.to_dict() for d in self.documents.values()],
        }
        self.path.write_text(
            json.dumps(data, indent=2, sort_keys=True),
            encoding="utf-8",
        )

    def get(self, doc_id: str) -> Optional[DocumentState]:
        """Get document state by ID."""
        return self.documents.get(doc_id)

    def get_by_path(self, source_path: str) -> Optional[DocumentState]:
        """Get document state by source path."""
        for doc in self.documents.values():
            if doc.source_path == source_path:
                return doc
        return None

    def update(self, doc_state: DocumentState) -> None:
        """Add or update a document state."""
        self.documents[doc_state.doc_id] = doc_state
        self.save()

    def remove(self, doc_id: str) -> bool:
        """Remove a document from state tracking."""
        if doc_id in self.documents:
            del self.documents[doc_id]
            self.save()
            return True
        return False

    def list_by_status(self, status: str | None = None) -> list[DocumentState]:
        """List documents, optionally filtered by status."""
        if status:
            return [d for d in self.documents.values() if d.status == status]
        return list(self.documents.values())

    @property
    def count(self) -> int:
        return len(self.documents)
