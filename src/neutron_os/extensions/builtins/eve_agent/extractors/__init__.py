"""Signal extractors for neut signal.

Extracts signals from various sources to feed the design loop:
- calendar: Meeting events, deadlines
- notes: Personal notes, meeting minutes
- voice: Voice memos, transcriptions
- feedback: User feedback (surveys, support, analytics)
- docflow_review: External document changes (MS 365 Word, Google Docs)
"""

from .calendar import CalendarExtractor
from .docflow_review import DocFlowReviewExtractor, DocFormat, register_prd
from .feedback import FeedbackExtractor
from .notes import NotesExtractor

__all__ = [
    "CalendarExtractor",
    "NotesExtractor",
    "FeedbackExtractor",
    "DocFlowReviewExtractor",
    "DocFormat",
    "register_prd",
]
