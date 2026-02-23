"""Data models for the neut sense signal ingestion pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Signal:
    """A structured signal extracted from any source.

    Every extractor produces a list of Signal objects. These flow through
    the correlator (name/initiative resolution) and synthesizer (changelog
    generation).
    """

    source: str  # "gitlab_diff", "voice", "transcript", "freetext"
    timestamp: str  # ISO 8601
    raw_text: str  # Original content (or excerpt)
    people: list[str] = field(default_factory=list)
    initiatives: list[str] = field(default_factory=list)
    signal_type: str = "raw"  # progress, blocker, decision, action_item, status_change, raw
    detail: str = ""  # Human-readable summary
    confidence: float = 0.5  # 0.0-1.0 (1.0 for gitlab_diff, lower for LLM)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "timestamp": self.timestamp,
            "raw_text": self.raw_text,
            "people": self.people,
            "initiatives": self.initiatives,
            "signal_type": self.signal_type,
            "detail": self.detail,
            "confidence": self.confidence,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Signal:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class Extraction:
    """Result of running an extractor on a source file."""

    extractor: str  # Name of the extractor that produced this
    source_file: str  # Path to input file
    signals: list[Signal] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    extracted_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return {
            "extractor": self.extractor,
            "source_file": self.source_file,
            "signals": [s.to_dict() for s in self.signals],
            "errors": self.errors,
            "extracted_at": self.extracted_at,
        }


@dataclass
class ChangelogEntry:
    """A single entry in a generated changelog."""

    initiative: str
    signal_type: str
    detail: str
    people: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    confidence: float = 1.0


@dataclass
class Changelog:
    """A synthesized changelog draft, ready for human review."""

    date: str
    entries: list[ChangelogEntry] = field(default_factory=list)
    summary: str = ""
    generated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
