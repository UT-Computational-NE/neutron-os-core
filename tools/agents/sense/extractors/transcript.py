"""Transcript extractor — parses already-transcribed meeting notes.

Handles meeting transcripts that have already been converted to text
(e.g., from the meeting-intake pipeline). Extracts signals using
the LLM gateway if available, falls back to keyword matching.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from tools.agents.sense.extractors.base import BaseExtractor
from tools.agents.sense.extractors.freetext import FreetextExtractor
from tools.agents.sense.models import Extraction, Signal
from tools.agents.sense.gateway import Gateway
from tools.agents.sense.correlator import Correlator


class TranscriptExtractor(BaseExtractor):
    """Extract signals from pre-existing meeting transcripts."""

    @property
    def name(self) -> str:
        return "transcript"

    def can_handle(self, path: Path) -> bool:
        if not path.exists():
            return False
        # Accept .md or .txt files in a teams/ directory or with transcript-related names
        name_lower = path.name.lower()
        return (
            path.suffix in (".md", ".txt")
            and (
                "transcript" in name_lower
                or "meeting" in name_lower
                or "teams" in str(path).lower()
            )
        )

    def extract(self, source: Path, **kwargs) -> Extraction:
        """Extract signals from a meeting transcript.

        Delegates to FreetextExtractor with a meeting-specific system prompt
        when LLM is available.
        """
        gateway: Gateway | None = kwargs.get("gateway")
        correlator: Correlator | None = kwargs.get("correlator")

        try:
            text = source.read_text(encoding="utf-8")
        except Exception as e:
            return Extraction(
                extractor=self.name,
                source_file=str(source),
                errors=[f"Failed to read transcript: {e}"],
            )

        now = datetime.now(timezone.utc).isoformat()
        signals: list[Signal] = []

        if gateway and gateway.available:
            signals = self._extract_with_meeting_prompt(
                text, source, gateway, correlator, now
            )
        else:
            # Fall back to basic keyword matching
            ft = FreetextExtractor()
            signal = Signal(
                source=self.name,
                timestamp=now,
                raw_text=text[:2000],
                signal_type="raw",
                detail=f"Meeting transcript: {source.name} ({len(text)} chars)",
                confidence=0.3,
                metadata={"filename": source.name, "full_length": len(text)},
            )
            if correlator:
                signal.people = ft._find_people_mentions(text, correlator)
                signal.initiatives = ft._find_initiative_mentions(text, correlator)
            signals.append(signal)

        return Extraction(
            extractor=self.name,
            source_file=str(source),
            signals=signals,
        )

    def _extract_with_meeting_prompt(
        self,
        text: str,
        source: Path,
        gateway: Gateway,
        correlator: Correlator | None,
        timestamp: str,
    ) -> list[Signal]:
        """Use LLM with meeting-specific prompt."""
        import json as json_mod

        system = (
            "You are analyzing a meeting transcript for a nuclear engineering program. "
            "Extract structured signals. Focus on: decisions made, action items assigned, "
            "blockers raised, progress updates, and status changes. "
            "Return a JSON array of objects, each with: "
            '"signal_type" (one of: progress, blocker, decision, action_item, status_change), '
            '"detail" (one-sentence summary), '
            '"people" (list of names mentioned or responsible), '
            '"initiatives" (list of project/initiative names discussed). '
            "Be thorough — meetings often contain multiple signals. Return only the JSON array."
        )

        response = gateway.complete(
            prompt=text[:6000],
            system=system,
            task="extraction",
        )

        if not response.success:
            return [Signal(
                source=self.name,
                timestamp=timestamp,
                raw_text=text[:2000],
                signal_type="raw",
                detail=f"Meeting LLM extraction failed. Raw text preserved.",
                confidence=0.3,
                metadata={"filename": source.name},
            )]

        signals = []
        try:
            response_text = response.text.strip()
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                response_text = "\n".join(lines[1:-1])

            extracted = json_mod.loads(response_text)
            if not isinstance(extracted, list):
                extracted = [extracted]

            for item in extracted:
                people = item.get("people", [])
                initiatives = item.get("initiatives", [])

                if correlator:
                    people = correlator.resolve_people(people)
                    initiatives = correlator.resolve_initiatives(initiatives)

                signals.append(Signal(
                    source=self.name,
                    timestamp=timestamp,
                    raw_text=text[:500],
                    people=people,
                    initiatives=initiatives,
                    signal_type=item.get("signal_type", "raw"),
                    detail=item.get("detail", ""),
                    confidence=0.7,
                    metadata={
                        "filename": source.name,
                        "llm_provider": response.provider,
                    },
                ))

        except (json_mod.JSONDecodeError, KeyError, TypeError):
            signals.append(Signal(
                source=self.name,
                timestamp=timestamp,
                raw_text=text[:2000],
                signal_type="raw",
                detail=response.text[:500],
                confidence=0.5,
                metadata={"filename": source.name, "llm_provider": response.provider},
            ))

        return signals
