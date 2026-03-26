"""Synthesis module - transforms signal clusters into actionable outputs."""

from .briefing_generator import BriefingGenerator, DesignBriefing
from .prd_updater import PRDUpdateDraft, PRDUpdater

__all__ = [
    "PRDUpdater",
    "PRDUpdateDraft",
    "BriefingGenerator",
    "DesignBriefing",
]
