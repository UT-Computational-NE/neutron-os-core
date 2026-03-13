"""Document ingestion orchestrator.

Scans the repository for markdown/text files, chunks them, generates
embeddings, and upserts into the RAG store.  Uses MD5 checksums to
skip unchanged files.
"""

from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .chunker import chunk_markdown
from .embeddings import embed_texts
from .extract import extract_text, SUPPORTED_EXTENSIONS
from .store import CORPUS_INTERNAL, RAGStore

log = logging.getLogger(__name__)

_TEXT_EXTENSIONS = {".md", ".txt"}
_BINARY_EXTENSIONS = {".pdf", ".docx", ".pptx", ".odt"}


@dataclass
class IngestStats:
    files_indexed: int = 0
    chunks_created: int = 0
    files_skipped: int = 0


def _md5(path: Path) -> str:
    h = hashlib.md5()
    h.update(path.read_bytes())
    return h.hexdigest()


def ingest_file(
    path: Path,
    store: RAGStore,
    repo_root: Optional[Path] = None,
    corpus: str = CORPUS_INTERNAL,
    owner: Optional[str] = None,
) -> IngestStats:
    """Ingest a single file into the RAG store.

    Returns stats for this file (1 indexed or 1 skipped).
    """
    stats = IngestStats()

    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        log.debug("Skipping unsupported file: %s", path)
        stats.files_skipped += 1
        return stats

    rel_path = str(path.relative_to(repo_root)) if repo_root else str(path)
    checksum = _md5(path)

    # Check if already indexed with same checksum
    existing = store.get_document(rel_path)
    if existing and existing.get("checksum") == checksum:
        log.debug("Unchanged, skipping: %s", rel_path)
        stats.files_skipped += 1
        return stats

    # Extract text — plain read for md/txt, extraction for binary formats
    if suffix in _TEXT_EXTENSIONS:
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            log.warning("Cannot read %s: %s", path, exc)
            stats.files_skipped += 1
            return stats
    else:
        content = extract_text(path)
        if not content:
            log.warning("No text extracted from %s", rel_path)
            stats.files_skipped += 1
            return stats

    chunks = chunk_markdown(content, rel_path)
    if not chunks:
        stats.files_skipped += 1
        return stats

    # Generate embeddings (optional — works without OPENAI_API_KEY)
    texts = [c.text for c in chunks]
    embeddings = embed_texts(texts)

    if embeddings is None:
        log.info("Indexing %s (%d chunks, text-only — no embedding API key)", rel_path, len(chunks))
    else:
        log.info("Indexing %s (%d chunks, with embeddings)", rel_path, len(chunks))

    store.upsert_chunks(chunks, embeddings, checksum=checksum, corpus=corpus, owner=owner)

    stats.files_indexed = 1
    stats.chunks_created = len(chunks)
    return stats


def ingest_repo(
    repo_root: Path,
    store: RAGStore,
    corpus: str = CORPUS_INTERNAL,
) -> IngestStats:
    """Scan and ingest all supported documents under *repo_root*.

    Looks in ``docs/``, ``runtime/config/``, and ``CLAUDE.md``.
    """
    stats = IngestStats()

    search_dirs = [
        repo_root / "docs",
        repo_root / "runtime" / "config",
        repo_root / "runtime" / "knowledge",  # Box, SharePoint, external docs
    ]
    extra_files = [repo_root / "CLAUDE.md"]

    files: list[Path] = []
    for d in search_dirs:
        if d.is_dir():
            for ext in SUPPORTED_EXTENSIONS:
                files.extend(d.rglob(f"*{ext}"))
    for f in extra_files:
        if f.is_file():
            files.append(f)

    # Filter out __MACOSX and hidden files
    files = [f for f in files if "__MACOSX" not in str(f) and not f.name.startswith(".")]

    log.info("Found %d files to consider for ingestion", len(files))

    for fpath in sorted(files):
        file_stats = ingest_file(fpath, store, repo_root=repo_root, corpus=corpus)
        stats.files_indexed += file_stats.files_indexed
        stats.chunks_created += file_stats.chunks_created
        stats.files_skipped += file_stats.files_skipped

    log.info(
        "Ingestion complete: %d indexed, %d chunks, %d skipped",
        stats.files_indexed,
        stats.chunks_created,
        stats.files_skipped,
    )
    return stats
