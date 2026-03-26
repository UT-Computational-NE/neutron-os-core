"""Sense & Synthesis Pipeline for NeutronOS.

The full product development feedback loop:
  Sense → Synthesize → Create → Publish → Sense

Extracts design signals, clusters by PRD, synthesizes updates,
and tracks loop health metrics to increase velocity over time.
"""

from .clustering import PRDClusterer, SignalCluster
from .extractors import CalendarExtractor, FeedbackExtractor, NotesExtractor
from .loop import (
    ArtifactType,
    FeedbackType,
    LoopHealthMetrics,
    LoopIteration,
    LoopStage,
    LoopTracker,
    SubscriberRole,
    Subscription,
)
from .models import Changelog, ChangelogEntry, Extraction, Signal, SignalManifest
from .synthesis import BriefingGenerator, DesignBriefing, PRDUpdateDraft, PRDUpdater

__version__ = "0.1.0"

__all__ = [
    # Models
    "Signal",
    "Extraction",
    "Changelog",
    "ChangelogEntry",
    "SignalManifest",
    # Extractors
    "CalendarExtractor",
    "NotesExtractor",
    "FeedbackExtractor",
    # Clustering
    "PRDClusterer",
    "SignalCluster",
    # Synthesis
    "PRDUpdater",
    "PRDUpdateDraft",
    "BriefingGenerator",
    "DesignBriefing",
    # Loop Tracking
    "LoopStage",
    "FeedbackType",
    "SubscriberRole",
    "ArtifactType",
    "Subscription",
    "LoopIteration",
    "LoopHealthMetrics",
    "LoopTracker",
]
