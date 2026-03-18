"""Embedding generation with automatic provider fallback.

Provider chain:
1. OpenAI API (text-embedding-3-small) — if OPENAI_API_KEY set and quota available
2. Ollama local (nomic-embed-text) — free, offline, no API key needed
3. None — caller handles fallback (e.g., keyword search)

The provider is selected automatically. If OpenAI returns a quota error
(402/429 with "exceeded your current quota"), falls through to Ollama.
"""

from __future__ import annotations

import json
import logging
import os
import time
import urllib.request
from typing import Optional

log = logging.getLogger(__name__)

_OPENAI_API_URL = "https://api.openai.com/v1/embeddings"
_OLLAMA_API_URL = "http://localhost:11434/api/embed"
_OLLAMA_EMBED_MODEL = "nomic-embed-text"

_BATCH_SIZE = 100
_MAX_RETRIES = 3
_BACKOFF_BASE = 2.0

# Track whether OpenAI is quota-blocked this session (don't retry every call)
_openai_quota_blocked = False


def embed_texts(
    texts: list[str],
    model: str = "text-embedding-3-small",
) -> Optional[list[list[float]]]:
    """Embed texts using the best available provider.

    Tries OpenAI first, falls back to Ollama if OpenAI is unavailable
    or quota-blocked. Returns None if no provider is available.
    """
    if not texts:
        return []

    # Try OpenAI first (unless we already know it's blocked)
    result = _embed_openai(texts, model)
    if result is not None:
        return result

    # Fall back to Ollama
    result = _embed_ollama(texts)
    if result is not None:
        return result

    log.warning(
        "No embedding provider available — OpenAI quota exceeded and Ollama "
        "embedding models failed to load (known issue with Ollama 0.18.x on "
        "some macOS versions). Fix your OpenAI billing at "
        "https://platform.openai.com/settings/organization/billing or wait "
        "for an Ollama update."
    )
    return None


def _embed_openai(texts: list[str], model: str) -> Optional[list[list[float]]]:
    """Embed via OpenAI API. Returns None if unavailable or quota-blocked."""
    global _openai_quota_blocked

    if _openai_quota_blocked:
        return None

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        import requests as _requests
    except ImportError:
        return None

    from neutron_os.infra.rate_limiter import get_limiter
    limiter = get_limiter("openai")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    all_embeddings: list[list[float]] = []

    for start in range(0, len(texts), _BATCH_SIZE):
        batch = texts[start: start + _BATCH_SIZE]
        payload = {"input": batch, "model": model}

        for attempt in range(_MAX_RETRIES):
            limiter.wait()
            resp = _requests.post(_OPENAI_API_URL, headers=headers, json=payload, timeout=60)
            limiter.update(resp)

            if resp.status_code == 429:
                # Check if it's a quota issue (not just rate limiting)
                body = resp.text.lower()
                if "exceeded your current quota" in body or "billing" in body:
                    log.warning("OpenAI quota exceeded — falling back to Ollama")
                    _openai_quota_blocked = True
                    return None

                wait = _BACKOFF_BASE * (2 ** attempt)
                log.warning("Rate limited by OpenAI, retrying in %.1fs", wait)
                time.sleep(wait)
                continue

            if resp.status_code >= 400:
                log.warning("OpenAI embeddings error %d — falling back", resp.status_code)
                return None

            data = resp.json()
            sorted_data = sorted(data["data"], key=lambda d: d["index"])
            all_embeddings.extend(d["embedding"] for d in sorted_data)
            break
        else:
            log.warning("OpenAI embeddings failed after %d retries", _MAX_RETRIES)
            return None

    return all_embeddings


def _embed_ollama(texts: list[str]) -> Optional[list[list[float]]]:
    """Embed via local Ollama. Returns None if Ollama is not available."""
    # Ensure Ollama is running
    try:
        from neutron_os.infra.connections import ensure_available
        ensure_available("ollama")
    except Exception:
        pass

    # Check if embedding model is available, pull if needed
    if not _ollama_has_model(_OLLAMA_EMBED_MODEL):
        log.info("Pulling Ollama embedding model: %s", _OLLAMA_EMBED_MODEL)
        try:
            import subprocess
            subprocess.run(
                ["ollama", "pull", _OLLAMA_EMBED_MODEL],
                capture_output=True, timeout=300,
            )
        except Exception as e:
            log.warning("Could not pull Ollama model %s: %s", _OLLAMA_EMBED_MODEL, e)
            return None

    all_embeddings: list[list[float]] = []

    for text in texts:
        try:
            payload = json.dumps({
                "model": _OLLAMA_EMBED_MODEL,
                "input": text,
            }).encode()
            req = urllib.request.Request(
                _OLLAMA_API_URL,
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                embeddings = data.get("embeddings", [])
                if embeddings:
                    all_embeddings.append(embeddings[0])
                else:
                    return None
        except Exception as e:
            log.warning("Ollama embedding failed: %s", e)
            return None

    return all_embeddings if all_embeddings else None


def _ollama_has_model(model: str) -> bool:
    """Check if Ollama has a model pulled."""
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags")
        with urllib.request.urlopen(req, timeout=2) as resp:
            data = json.loads(resp.read())
            models = [m.get("name", "") for m in data.get("models", [])]
            return any(model in m for m in models)
    except Exception:
        return False
