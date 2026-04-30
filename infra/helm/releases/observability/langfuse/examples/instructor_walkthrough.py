# Copyright (c) 2026 B-Tree Ventures, LLC
# SPDX-License-Identifier: Apache-2.0

"""LangFuse instructor walkthrough.

A guided demo that fires real prompts at Rascal's Axiom-managed Qwen endpoint
(:41883, EC-safe) and sends rich traces to the institutional LangFuse on
Rascal. Run this once as an instructor to see exactly what classroom traffic
will look like in LangFuse — then open the UI and use the included reading
guide.

Required env (sourced via direnv from workspace .envrc + Neutron_OS .env):
  LANGFUSE_PUBLIC_KEY
  LANGFUSE_SECRET_KEY
  LANGFUSE_HOST
  QWEN_API_KEY

Run:
  cd /path/to/UT_Computational_NE
  python Neutron_OS/infra/helm/releases/observability/langfuse/examples/instructor_walkthrough.py
"""

from __future__ import annotations

import base64
import json
import os
import time
import urllib.request
import uuid
from datetime import datetime, timezone
from typing import Any

# Reuse the real provider so we exercise the same code path the classroom
# extension will hit.
from axiom.infra.tracing.langfuse_provider import LangfuseTraceProvider


# ─── Configuration ─────────────────────────────────────────────────────────

LF_HOST = os.environ["LANGFUSE_HOST"]
LF_PK = os.environ["LANGFUSE_PUBLIC_KEY"]
LF_SK = os.environ["LANGFUSE_SECRET_KEY"]
QWEN_KEY = os.environ["QWEN_API_KEY"]

# The Axiom-managed Qwen endpoint on Rascal — bare Qwen, EC-safe, no RAG.
# Same target the `rascal-qwen-ec` axi connect preset routes to.
QWEN_URL = "https://10.159.142.118:41883/v1/chat/completions"
QWEN_MODEL = "unsloth/Qwen3.5-122B-A10B-GGUF:Q4_K_M"

# Realistic classroom metadata — use values you'd attach in production.
COURSE = "NE-101"
COHORT = "prague-summer-2026"
INSTRUCTOR = "@ondrej:utexas"
WEEK = 1


# ─── HTTP helpers ──────────────────────────────────────────────────────────


def call_qwen(messages: list[dict[str, str]]) -> tuple[str, str, dict[str, Any], float]:
    """Send a chat-completion request to Rascal Qwen.
    Returns (answer, reasoning, usage, latency_s).

    Qwen 3.5 is a reasoning model: it produces a hidden `reasoning_content`
    chain-of-thought followed by a `content` answer. We capture both so the
    instructor can see what the model was thinking — useful when answers
    look surprising.
    """
    import ssl

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE  # Rascal uses self-signed; matches verify_ssl=false

    payload = json.dumps(
        {
            "model": QWEN_MODEL,
            "messages": messages,
            # Generous budget — Qwen 3.5 burns ~500-1000 tokens on reasoning
            # before producing the answer. Truncating mid-think yields an
            # empty `content`.
            "max_tokens": 2000,
            "temperature": 0.3,
        }
    ).encode()
    req = urllib.request.Request(
        QWEN_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {QWEN_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
        body = json.loads(resp.read())
    elapsed = time.perf_counter() - t0

    msg = body["choices"][0]["message"]
    answer = msg.get("content", "") or ""
    reasoning = msg.get("reasoning_content", "") or ""
    usage = body.get("usage", {})
    return answer, reasoning, usage, elapsed


def post_event(event: dict[str, Any]) -> None:
    """Direct LangFuse ingest — used for the manual `score` and `tags` demos
    that aren't yet first-class on the provider. Production code will use
    the provider; this is a teaching escape hatch."""
    auth = base64.b64encode(f"{LF_PK}:{LF_SK}".encode()).decode()
    req = urllib.request.Request(
        f"{LF_HOST}/api/public/ingestion",
        data=json.dumps({"batch": [event]}).encode(),
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10):
        pass


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ─── A trace-with-context helper ───────────────────────────────────────────


def attach_user_session_tags(
    trace_id: str,
    *,
    user_id: str,
    session_id: str,
    tags: list[str],
) -> None:
    """LangFuse's UI has dedicated User and Session views that filter on
    top-level fields. The provider currently puts everything in metadata, so
    this helper updates the trace afterward to hoist them.

    TODO: extend LangfuseTraceProvider so callers can pass these as kwargs
    to start_trace() and the provider hoists them automatically. Filed under
    the deeper observability dive.
    """
    post_event(
        {
            "id": str(uuid.uuid4()),
            "timestamp": now_iso(),
            "type": "trace-create",
            "body": {
                "id": trace_id,
                "userId": user_id,
                "sessionId": session_id,
                "tags": tags,
            },
        }
    )


# ─── Demo scenarios ────────────────────────────────────────────────────────


def demo_session_alice_three_questions(provider: LangfuseTraceProvider) -> None:
    """One student, one chat session, three turns. Demonstrates:
    - userId + sessionId grouping
    - Multiple traces under one session
    - Tags for course/cohort/week
    - Generation timing + token usage from the model
    """
    print("\n[DEMO 1] alice asks 3 questions in one session")
    user_id = "@alice:prague"
    session_id = f"chat-alice-week{WEEK}-{datetime.now().strftime('%Y%m%d')}"
    tags = [f"course:{COURSE}", f"cohort:{COHORT}", f"week:{WEEK}", "role:student"]

    questions = [
        "In two sentences, what's the difference between fission and fusion?",
        "Could you explain k-effective in plain English for a non-physicist?",
        "Why does U-235 fission more easily than U-238?",
    ]
    history: list[dict[str, str]] = [
        {"role": "system", "content": "You are a nuclear-engineering tutor. Be concise."}
    ]

    for i, q in enumerate(questions, 1):
        history.append({"role": "user", "content": q})
        tid = provider.start_trace(
            f"chat.message.{i}",
            course=COURSE,
            cohort=COHORT,
            week=WEEK,
            instructor=INSTRUCTOR,
            student=user_id,
            turn=i,
        )
        attach_user_session_tags(tid, user_id=user_id, session_id=session_id, tags=tags)

        answer, reasoning, usage, elapsed = call_qwen(history)
        history.append({"role": "assistant", "content": answer})

        provider.log_generation(
            tid,
            model=QWEN_MODEL,
            prompt=q,
            output=answer,
            latency_ms=int(elapsed * 1000),
            tokens_in=usage.get("prompt_tokens"),
            tokens_out=usage.get("completion_tokens"),
            tokens_total=usage.get("total_tokens"),
            endpoint="rascal-qwen-ec",
            reasoning_chars=len(reasoning),
            reasoning_preview=reasoning[:400],
        )
        print(f"  q{i}: {q[:50]}... → answer={len(answer)} reasoning={len(reasoning)} chars in {elapsed:.1f}s")

    provider.flush()


def demo_session_bob_low_confidence(provider: LangfuseTraceProvider) -> None:
    """A question outside the model's training distribution — bare Qwen has
    no NETL TRIGA corpus, so it'll either hallucinate or hedge. Demonstrates:
    - The pattern that triggers RAG-grounding (vs bare-LLM)
    - Why instructors need to watch for low-confidence answers
    - Manual instructor scoring as a feedback signal CHALK-E will eventually consume
    """
    print("\n[DEMO 2] bob asks an out-of-corpus question (bare Qwen, no RAG)")
    user_id = "@bob:prague"
    session_id = f"chat-bob-week{WEEK}-{datetime.now().strftime('%Y%m%d')}"
    tags = [
        f"course:{COURSE}",
        f"cohort:{COHORT}",
        f"week:{WEEK}",
        "role:student",
        "review:flagged",
    ]

    q = "What is the operating power level of the NETL TRIGA reactor in kW?"
    history = [
        {"role": "system", "content": "You are a nuclear-engineering tutor. Be honest about uncertainty."},
        {"role": "user", "content": q},
    ]
    tid = provider.start_trace(
        "chat.message.1",
        course=COURSE,
        cohort=COHORT,
        week=WEEK,
        instructor=INSTRUCTOR,
        student=user_id,
        turn=1,
        rag_used=False,  # important context for instructor review
    )
    attach_user_session_tags(tid, user_id=user_id, session_id=session_id, tags=tags)

    answer, reasoning, usage, elapsed = call_qwen(history)

    # Empty retrieval span demonstrates "no RAG used" case in the trace tree.
    provider.log_retrieval(tid, query=q, results=[], retrieval_skipped=True)
    provider.log_generation(
        tid,
        model=QWEN_MODEL,
        prompt=q,
        output=answer,
        latency_ms=int(elapsed * 1000),
        tokens_in=usage.get("prompt_tokens"),
        tokens_out=usage.get("completion_tokens"),
        tokens_total=usage.get("total_tokens"),
        endpoint="rascal-qwen-ec",
        reasoning_chars=len(reasoning),
        reasoning_preview=reasoning[:400],
    )
    # Instructor manual score — what CHALK-E will eventually do automatically.
    provider.score(
        tid,
        name="factuality",
        value=0.0,  # placeholder; we'll discuss in the walkthrough
        reviewer=INSTRUCTOR,
        reason="bare Qwen has no NETL TRIGA corpus — answer is unreliable; needs RAG",
    )
    provider.flush()
    print(f"  q: {q[:60]}... → answer={len(answer)} reasoning={len(reasoning)} chars in {elapsed:.1f}s (instructor flagged)")


def demo_evals_dataset_seed() -> None:
    """LangFuse Datasets — ground-truth Q&A you collect over the term. Each
    dataset item ties an input to an expected output; running an eval over
    the dataset is how you'll know whether a prompt change improved or
    regressed quality. Demonstrates the SHAPE; CHALK-E will populate this
    automatically as the cohort runs.
    """
    print("\n[DEMO 3] seeding 2 example dataset items for evals")
    dataset_name = f"{COURSE}-week{WEEK}-canonical-qs"

    items = [
        {
            "input": "What is k-effective in a nuclear reactor?",
            "expectedOutput": (
                "k-effective (k_eff) is the ratio of neutrons in one generation "
                "to neutrons in the previous generation in a reactor system. "
                "k_eff = 1 means critical (steady), >1 supercritical, <1 subcritical."
            ),
        },
        {
            "input": "Explain the difference between thermal and fast neutrons.",
            "expectedOutput": (
                "Thermal neutrons (~0.025 eV) are slowed by a moderator and have "
                "high fission cross-sections in U-235; fast neutrons (~1 MeV+) "
                "are produced by fission and drive fast-spectrum reactor designs."
            ),
        },
    ]
    auth = base64.b64encode(f"{LF_PK}:{LF_SK}".encode()).decode()
    for item in items:
        # POST /api/public/datasets to create-or-get; then POST items
        # (LangFuse exposes a public datasets API; for the walkthrough we
        # just show the call shape — actual seeding tomorrow.)
        print(f"  would seed → {dataset_name}: {item['input'][:50]}...")
    print("  (skipping live dataset POST in this walkthrough — UI is faster for first run)")


# ─── Main ──────────────────────────────────────────────────────────────────


def main() -> None:
    print("=" * 72)
    print("LangFuse instructor walkthrough — sending real traces to:")
    print(f"  {LF_HOST}")
    print("=" * 72)

    provider = LangfuseTraceProvider(
        public_key=LF_PK, secret_key=LF_SK, host=LF_HOST
    )

    demo_session_alice_three_questions(provider)
    demo_session_bob_low_confidence(provider)
    demo_evals_dataset_seed()

    print("\n" + "=" * 72)
    print("DONE. Open the LangFuse UI now:")
    print(f"  {LF_HOST}")
    print("\nReading guide → see ../README.md §Walkthrough")
    print("=" * 72)


if __name__ == "__main__":
    main()
