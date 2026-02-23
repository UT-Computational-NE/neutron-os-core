"""Voice memo extractor — transcription via Whisper + optional diarization.

Processes .m4a files in inbox/raw/voice/:
1. Transcribe with openai-whisper (base model for speed)
2. Optionally run pyannote.audio for speaker diarization
3. Save transcript to inbox/processed/
4. Extract signals via LLM if available

Gracefully degrades if whisper is not installed.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from tools.agents.sense.extractors.base import BaseExtractor
from tools.agents.sense.models import Extraction, Signal


class VoiceExtractor(BaseExtractor):
    """Extract signals from voice memo recordings."""

    SUPPORTED_EXTENSIONS = {".m4a", ".mp3", ".wav", ".webm", ".mp4", ".ogg"}

    @property
    def name(self) -> str:
        return "voice"

    def can_handle(self, path: Path) -> bool:
        return path.exists() and path.suffix.lower() in self.SUPPORTED_EXTENSIONS

    def extract(self, source: Path, **kwargs) -> Extraction:
        """Transcribe a voice memo and extract signals.

        Args:
            source: Path to audio file.
            model_size: Whisper model size (default "base").
            gateway: LLM gateway for signal extraction.
            correlator: Entity correlator.
        """
        model_size = kwargs.get("model_size", "base")
        gateway = kwargs.get("gateway")
        correlator = kwargs.get("correlator")

        # Check if whisper is available
        try:
            import whisper  # type: ignore
        except ImportError:
            return Extraction(
                extractor=self.name,
                source_file=str(source),
                signals=[],
                errors=[
                    "openai-whisper not installed. Install with: pip install openai-whisper. "
                    "Skipping voice transcription."
                ],
            )

        now = datetime.now(timezone.utc).isoformat()
        signals: list[Signal] = []
        errors: list[str] = []

        # Transcribe
        try:
            print(f"  Transcribing {source.name} (model={model_size})...", flush=True)
            model = whisper.load_model(model_size)
            result = model.transcribe(str(source))
            transcript = result.get("text", "")

            if not transcript.strip():
                return Extraction(
                    extractor=self.name,
                    source_file=str(source),
                    errors=["Transcription produced empty text."],
                )

            print(f"  Transcribed: {len(transcript)} chars", flush=True)

        except Exception as e:
            return Extraction(
                extractor=self.name,
                source_file=str(source),
                errors=[f"Transcription failed: {e}"],
            )

        # Optional diarization
        speakers: dict[str, list[str]] = {}
        try:
            from pyannote.audio import Pipeline  # type: ignore

            hf_token = __import__("os").environ.get("HF_TOKEN")
            if hf_token:
                print("  Running speaker diarization...", flush=True)
                pipeline = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization-3.1",
                    use_auth_token=hf_token,
                )
                diarization = pipeline(str(source))
                for turn, _, speaker in diarization.itertracks(yield_label=True):
                    speakers.setdefault(speaker, []).append(
                        f"[{turn.start:.1f}s-{turn.end:.1f}s]"
                    )
                print(f"  Found {len(speakers)} speaker(s)", flush=True)
        except ImportError:
            pass  # pyannote not available, skip diarization
        except Exception as e:
            errors.append(f"Diarization failed (non-fatal): {e}")

        # Save transcript to processed/
        processed_dir = self._get_processed_dir(source)
        processed_dir.mkdir(parents=True, exist_ok=True)
        transcript_path = processed_dir / f"{source.stem}_transcript.md"

        transcript_content = f"# Transcript: {source.name}\n\n"
        transcript_content += f"**Transcribed:** {now}\n"
        transcript_content += f"**Model:** whisper-{model_size}\n\n"
        if speakers:
            transcript_content += "## Speakers\n\n"
            for speaker, segments in speakers.items():
                transcript_content += f"- {speaker}: {len(segments)} segments\n"
            transcript_content += "\n"
        transcript_content += "## Full Transcript\n\n"
        transcript_content += transcript

        transcript_path.write_text(transcript_content, encoding="utf-8")

        # Create base signal
        signal = Signal(
            source=self.name,
            timestamp=now,
            raw_text=transcript[:2000],
            signal_type="raw",
            detail=f"Voice memo transcribed: {source.name} ({len(transcript)} chars)",
            confidence=0.6,
            metadata={
                "filename": source.name,
                "model": f"whisper-{model_size}",
                "transcript_path": str(transcript_path),
                "speaker_count": len(speakers),
            },
        )

        # Try LLM extraction (import here to avoid circular import at module level)
        from tools.agents.sense.extractors.freetext import FreetextExtractor

        if gateway and gateway.available:
            ft = FreetextExtractor()
            llm_signals = ft._extract_with_llm(
                transcript, source, gateway, correlator, now
            )
            for s in llm_signals:
                s.source = self.name
                s.metadata["original_file"] = source.name
            signals.extend(llm_signals)
        else:
            # No LLM — use correlator for basic matching
            if correlator:
                signal.people = FreetextExtractor._find_people_mentions(
                    transcript, correlator
                )
                signal.initiatives = FreetextExtractor._find_initiative_mentions(
                    transcript, correlator
                )
            signals.append(signal)

        return Extraction(
            extractor=self.name,
            source_file=str(source),
            signals=signals,
            errors=errors,
        )

    @staticmethod
    def _get_processed_dir(source: Path) -> Path:
        """Get the processed directory for saving transcripts."""
        # Navigate up from the source to find inbox/raw, then go to inbox/processed
        # source is like: tools/agents/inbox/raw/voice/memo.m4a
        parts = source.parts
        try:
            raw_idx = parts.index("raw")
            base = Path(*parts[:raw_idx])
            return base / "processed"
        except ValueError:
            return source.parent / "processed"
