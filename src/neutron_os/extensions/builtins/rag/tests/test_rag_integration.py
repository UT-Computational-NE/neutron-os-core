"""Integration tests for the RAG subsystem.

Require a live PostgreSQL instance with pgvector.
Run with:
    pytest src/neutron_os/extensions/builtins/rag/tests/test_rag_integration.py \
        -m integration -v

DATABASE_URL is read from the `rag.database_url` setting or the DATABASE_URL
environment variable.  The tests create isolated data under the `rag-internal`
corpus and clean up after themselves.
"""

from __future__ import annotations

import os
import textwrap
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_db_url() -> str | None:
    url = os.environ.get("DATABASE_URL")
    if url:
        return url
    try:
        from neutron_os.extensions.builtins.settings.store import SettingsStore
        return SettingsStore().get("rag.database_url") or None
    except Exception:
        return None


def _requires_db(fn):
    """Decorator: skip if no DATABASE_URL configured."""
    url = _get_db_url()
    return pytest.mark.skipif(
        not url,
        reason="DATABASE_URL / rag.database_url not configured",
    )(pytest.mark.integration(fn))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

TEST_CORPUS = "rag-internal"
TEST_PREFIX = "integration-test/"


@pytest.fixture(scope="module")
def store():
    """Connected RAGStore, cleaned of test data before and after the session."""
    url = _get_db_url()
    if not url:
        pytest.skip("No database configured")
    from neutron_os.rag.store import RAGStore
    s = RAGStore(url)
    s.connect()
    # Pre-clean any leftovers from a previous failed run
    with s._cur() as cur:
        cur.execute(
            "DELETE FROM chunks WHERE source_path LIKE %s AND corpus = %s",
            (TEST_PREFIX + "%", TEST_CORPUS),
        )
        cur.execute(
            "DELETE FROM documents WHERE source_path LIKE %s AND corpus = %s",
            (TEST_PREFIX + "%", TEST_CORPUS),
        )
    yield s
    # Teardown
    with s._cur() as cur:
        cur.execute(
            "DELETE FROM chunks WHERE source_path LIKE %s AND corpus = %s",
            (TEST_PREFIX + "%", TEST_CORPUS),
        )
        cur.execute(
            "DELETE FROM documents WHERE source_path LIKE %s AND corpus = %s",
            (TEST_PREFIX + "%", TEST_CORPUS),
        )
    s.close()


@pytest.fixture(scope="module")
def sample_chunks():
    """Two synthetic document chunks for testing."""
    from neutron_os.rag.chunker import Chunk

    return [
        Chunk(
            source_path=TEST_PREFIX + "xenon-guide.md",
            source_title="Xenon Poisoning Guide",
            source_type="markdown",
            text=textwrap.dedent("""\
                ## Xenon Poisoning

                Xenon-135 is a fission product with a very high neutron absorption cross-section.
                During reactor shutdown, Xe-135 builds up as I-135 decays, causing the reactor
                to become harder to restart — a phenomenon called the iodine pit.
            """),
            chunk_index=0,
            start_line=1,
        ),
        Chunk(
            source_path=TEST_PREFIX + "export-control.md",
            source_title="Export Control Overview",
            source_type="markdown",
            text=textwrap.dedent("""\
                ## Export Control (EAR / 10 CFR 810)

                MCNP, SCALE, and ORIGEN are export-controlled nuclear codes.
                Any analysis using these tools must be routed through the VPN-gated model tier.
                Queries containing these code names should never reach cloud providers.
            """),
            chunk_index=0,
            start_line=1,
        ),
    ]


# ---------------------------------------------------------------------------
# Core store tests
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_upsert_and_retrieve(store, sample_chunks):
    """Chunks can be inserted and retrieved by source_path."""
    store.upsert_chunks(
        [sample_chunks[0]],
        checksum="abc123",
        corpus=TEST_CORPUS,
    )
    doc = store.get_document(TEST_PREFIX + "xenon-guide.md", corpus=TEST_CORPUS)
    assert doc is not None
    assert doc["chunk_count"] == 1
    assert doc["checksum"] == "abc123"


@pytest.mark.integration
def test_full_text_search_returns_relevant_chunk(store, sample_chunks):
    """Full-text search finds the xenon chunk when querying 'iodine pit'."""
    store.upsert_chunks([sample_chunks[0]], checksum="abc123", corpus=TEST_CORPUS)
    results = store.search(query_text="iodine pit xenon", limit=5)
    assert len(results) > 0
    texts = [r.chunk_text for r in results]
    assert any("Xenon" in t or "xenon" in t for t in texts)


@pytest.mark.integration
def test_search_returns_corpus_field(store, sample_chunks):
    """Search results include the corpus field."""
    store.upsert_chunks([sample_chunks[0]], checksum="abc123", corpus=TEST_CORPUS)
    results = store.search(query_text="xenon", limit=5)
    assert all(r.corpus == TEST_CORPUS for r in results)


@pytest.mark.integration
def test_upsert_replaces_existing_chunks(store, sample_chunks):
    """Upserting the same source_path+corpus replaces old chunks."""
    chunk = sample_chunks[0]
    store.upsert_chunks([chunk], checksum="v1", corpus=TEST_CORPUS)
    store.upsert_chunks([chunk], checksum="v2", corpus=TEST_CORPUS)
    doc = store.get_document(chunk.source_path, corpus=TEST_CORPUS)
    assert doc["checksum"] == "v2"
    with store._cur() as cur:
        cur.execute(
            "SELECT count(*) AS n FROM chunks WHERE source_path = %s AND corpus = %s",
            (chunk.source_path, TEST_CORPUS),
        )
        assert cur.fetchone()["n"] == 1


@pytest.mark.integration
def test_per_corpus_stats(store, sample_chunks):
    """stats() returns per-corpus breakdown."""
    store.upsert_chunks([sample_chunks[0]], checksum="s1", corpus=TEST_CORPUS)
    store.upsert_chunks([sample_chunks[1]], checksum="s2", corpus=TEST_CORPUS)
    s = store.stats()
    assert s["total_chunks"] >= 2
    assert "rag-internal" in s["chunks_by_corpus"]
    assert s["chunks_by_corpus"]["rag-internal"] >= 2


@pytest.mark.integration
def test_delete_document(store, sample_chunks):
    """delete_document removes only the targeted doc from the corpus."""
    chunk = sample_chunks[1]
    store.upsert_chunks([chunk], checksum="del1", corpus=TEST_CORPUS)
    store.delete_document(chunk.source_path, corpus=TEST_CORPUS)
    assert store.get_document(chunk.source_path, corpus=TEST_CORPUS) is None


# ---------------------------------------------------------------------------
# Ingest integration tests
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_ingest_file_roundtrip(store, tmp_path):
    """ingest_file indexes a real markdown file and it becomes searchable."""
    from neutron_os.rag.ingest import ingest_file

    md = tmp_path / "test-doc.md"
    md.write_text(
        "# TRIGA Reactor Safety\n\n"
        "The TRIGA reactor has a negative temperature coefficient of reactivity. "
        "This self-limiting safety feature prevents runaway power excursions.\n"
    )
    # Use a unique path prefix to avoid collisions
    stats = ingest_file(md, store, repo_root=tmp_path, corpus=TEST_CORPUS)
    assert stats.files_indexed == 1
    assert stats.chunks_created >= 1

    results = store.search(query_text="negative temperature coefficient TRIGA", limit=5)
    assert any("TRIGA" in r.chunk_text for r in results)


@pytest.mark.integration
def test_ingest_skips_unchanged_checksum(store, tmp_path):
    """ingest_file skips files whose checksum hasn't changed."""
    from neutron_os.rag.ingest import ingest_file

    md = tmp_path / "stable-doc.md"
    md.write_text("# Stable\n\nNo changes here.\n")

    stats1 = ingest_file(md, store, repo_root=tmp_path, corpus=TEST_CORPUS)
    assert stats1.files_indexed == 1

    stats2 = ingest_file(md, store, repo_root=tmp_path, corpus=TEST_CORPUS)
    assert stats2.files_skipped == 1
    assert stats2.files_indexed == 0


# ---------------------------------------------------------------------------
# CLI integration tests
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_cli_status_shows_counts(capsys):
    """neut rag status shows the per-corpus table."""
    from neutron_os.rag.cli import main

    main(["status"])
    out = capsys.readouterr().out
    assert "RAG Index Status" in out
    assert "community" in out
    assert "internal" in out


@pytest.mark.integration
def test_cli_index_with_explicit_path(tmp_path):
    """neut rag index <path> traverses the directory and indexes docs."""
    from neutron_os.rag.cli import main

    doc = tmp_path / "reactor-ops.md"
    doc.write_text(
        "# Reactor Operations\n\nMaintain criticality with control rod withdrawal.\n"
    )
    main(["index", str(tmp_path), "--corpus", "rag-internal"])

    # Verify it's searchable
    url = _get_db_url()
    from neutron_os.rag.store import RAGStore
    s = RAGStore(url)
    s.connect()
    results = s.search(query_text="criticality control rod", limit=5)
    s.close()
    assert any("criticality" in r.chunk_text.lower() for r in results)
