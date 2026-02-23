"""PandocDocxProvider — generates .docx from markdown.

Extracts the generation logic from docs/_tools/md_to_docx.py.
Uses that script as an external tool, or falls back to pandoc directly.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

from tools.docflow.factory import DocFlowFactory
from tools.docflow.providers.base import (
    GenerationProvider,
    GenerationOptions,
    GenerationResult,
)


class PandocDocxProvider(GenerationProvider):
    """Generate .docx files from markdown using md_to_docx.py or pandoc."""

    def __init__(self, config: dict[str, Any] | None = None):
        config = config or {}
        self.toc = config.get("toc", True)
        self.toc_depth = config.get("toc_depth", 3)
        self.reference_doc = config.get("reference_doc")
        self.mermaid_renderer = config.get("mermaid_renderer", "mermaid.ink")

        # Locate md_to_docx.py relative to repo
        self._md_to_docx = self._find_md_to_docx()

    @staticmethod
    def _find_md_to_docx() -> Path | None:
        """Find the md_to_docx.py script."""
        # Walk up to find repo root
        path = Path(__file__).resolve()
        while path != path.parent:
            candidate = path / "docs" / "_tools" / "md_to_docx.py"
            if candidate.exists():
                return candidate
            path = path.parent
        return None

    def generate(
        self, source_path: Path, output_path: Path, options: GenerationOptions
    ) -> GenerationResult:
        """Generate .docx from markdown source."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        warnings: list[str] = []

        if self._md_to_docx and self._md_to_docx.exists():
            # Use the custom md_to_docx.py converter
            result = self._generate_with_md_to_docx(source_path, output_path, options)
            if result:
                return result
            warnings.append("md_to_docx.py failed, falling back to pandoc")

        # Fall back to pandoc
        return self._generate_with_pandoc(source_path, output_path, options, warnings)

    def _generate_with_md_to_docx(
        self, source: Path, output: Path, options: GenerationOptions
    ) -> GenerationResult | None:
        """Use md_to_docx.py for generation."""
        cmd = [
            "python3",
            str(self._md_to_docx),
            str(source),
            str(output),
        ]

        if options.toc or self.toc:
            cmd.append("--toc")
        cmd.append("--bookmarks")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(source.parent),
                timeout=120,
            )

            if result.returncode == 0 and output.exists():
                return GenerationResult(
                    output_path=output,
                    format="docx",
                    size_bytes=output.stat().st_size,
                )
            return None

        except (subprocess.TimeoutExpired, FileNotFoundError):
            return None

    def _generate_with_pandoc(
        self,
        source: Path,
        output: Path,
        options: GenerationOptions,
        warnings: list[str],
    ) -> GenerationResult:
        """Use pandoc directly for generation."""
        cmd = ["pandoc", str(source), "-o", str(output)]

        if options.toc or self.toc:
            cmd.extend(["--toc", f"--toc-depth={options.toc_depth or self.toc_depth}"])

        if options.reference_doc or self.reference_doc:
            ref = options.reference_doc or self.reference_doc
            cmd.extend(["--reference-doc", ref])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(source.parent),
                timeout=60,
            )

            if result.returncode != 0:
                warnings.append(f"pandoc stderr: {result.stderr[:200]}")

            if not output.exists():
                raise RuntimeError(f"pandoc failed to generate {output}: {result.stderr}")

            return GenerationResult(
                output_path=output,
                format="docx",
                size_bytes=output.stat().st_size,
                warnings=warnings,
            )

        except FileNotFoundError:
            raise RuntimeError(
                "pandoc not found. Install with: brew install pandoc (macOS) "
                "or apt install pandoc (Linux)"
            )

    def rewrite_links(self, artifact_path: Path, link_map: dict[str, str]) -> None:
        """Rewrite internal links in a .docx file.

        Opens the docx, finds hyperlinks that reference .md files,
        and replaces them with published URLs from the link map.
        """
        if not link_map:
            return

        try:
            from docx import Document
        except ImportError:
            return  # python-docx not available

        doc = Document(str(artifact_path))
        modified = False

        # Walk all paragraphs and their hyperlink relationships
        for paragraph in doc.paragraphs:
            for run in paragraph.runs:
                for old_ref, new_url in link_map.items():
                    if old_ref in run.text:
                        run.text = run.text.replace(old_ref, new_url)
                        modified = True

        # Also check hyperlink relationships in the document part
        try:
            part = doc.part
            for rel in part.rels.values():
                if rel.is_external:
                    target = rel._target
                    for old_ref, new_url in link_map.items():
                        if old_ref in target:
                            rel._target = target.replace(old_ref, new_url)
                            modified = True
        except Exception:
            pass

        if modified:
            doc.save(str(artifact_path))

    def get_output_extension(self) -> str:
        return ".docx"

    def supports_watermark(self) -> bool:
        return True


# Self-register with factory
DocFlowFactory.register("generation", "pandoc-docx", PandocDocxProvider)
