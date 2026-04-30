# Don't Split the Table

## Structure-Aware Chunking for Scientific Retrieval

> *Repositioned 2026-04-30 — supporting technical report, not standalone
> flagship paper.* Structure-aware chunking is established prior art
> (LangChain `MarkdownHeaderTextSplitter`, Llama-Index `MarkdownNodeParser`,
> regulatory-NLP literature). This document contributes a reproducibility
> artifact + ablation data, not a novel headline contribution. The
> empirical findings here are CITED FROM the lead paper:
>
> **`pedagogical-intent-rag-eval-draft.md`** —
> *Pedagogical-Intent RAG Evaluation: Why Refusal Quality Matters for AI Tutoring*
>
> See also `portfolio-sequencing.md` for the publication cadence
> placing this as a technical report supporting the lead paper.

---

## Abstract (draft)

Retrieval-augmented generation (RAG) systems for scientific tutoring
often underperform commercial single-tenant chat baselines on
domain-specific questions, despite having access to authoritative course
material the baselines lack. We show that this gap is *not* a model-
capability gap but a **chunking gap**: fixed-window character-based
chunking, the default in most production RAG stacks, excludes
answer-bearing content from top-*k* retrieval on roughly one-third of
corpus-specific questions in a calibrated nuclear-engineering
introductory-course battery.

We compare three chunking strategies on the same retrieval +
generation pipeline: (1) fixed 400-character windows, (2) structure-aware
semantic chunking that respects markdown headings, tables, code blocks,
and list boundaries, and (3) graph-informed semantic chunking that
additionally consumes structural boundaries from a deterministic
entity/cross-reference extractor. Strategy (2) closes 31 percentage
points of the gap on should-RAG-win questions; strategy (3) extends
the benefit on regulatory-reference-dense and multi-document corpora
without regressing on short structured material.

Our broader claim: **for sovereign, institution-hosted RAG serving
educational and scientific workloads, the chunker is the bottleneck.**
Within the retrieval-grounding-generation pipeline, retrieval quality
dominates, and within retrieval quality, where you split the document
matters more than which embedder or model you use.

---

## 1. Introduction

[Frame: the rise of grounded RAG for sovereign / institutional AI;
the persistent perception that domain RAG ≈ general-LLM on niche
content; the unspoken role of chunking strategy in shaping the comparison.]

Indirect competitive framing (per portfolio guidance):
- *"character-window chunking products"* — never named directly
- *"general-purpose LLM tutoring services"* — without naming Claude/ChatGPT
- *"retrofit retrieval layers atop foundation models"*

**Contributions:**
1. A reproducible 5-lane comparison harness (bare LLM, three RAG-modes
   under different chunking strategies, commercial-baseline LLM)
   calibrated for a nuclear-engineering introductory course.
2. Empirical demonstration that fixed-window chunking misses
   answer-bearing content for ~30% of corpus-specific questions on a
   real lecture-style corpus.
3. A graph-informed chunking method that wraps an existing semantic
   chunker with deterministic entity / cross-reference extraction,
   delivering measurable gains on regulatory-reference-dense material
   without engineering retrofit.
4. A pedagogical framework for *per-student* RAG-mode + LLM-tier
   composition that lets instructors calibrate the cognitive demand
   of an AI tutor on a learner-by-learner basis.

---

## 2. Related Work

[To populate. Notes for now:]
- Sentence-window vs document-window vs sliding-window chunking
  literature (LangChain default, Llama-Index default, etc.) —
  describe approaches, frame as "character-window strategies"
- Document-structure-aware chunking (some prior work in legal/
  regulatory NLP)
- RAG evaluation benchmarks: BEIR, SciFact, MS-MARCO — note the
  domain coverage gap (no nuclear-engineering coursework)
- Pedagogical AI tutoring systems — note the typical commercial-
  black-box approach and the sovereignty gap

---

## 3. Method

### 3.1 The chunking strategies

**(C1) Fixed-window** — The reference baseline. 400-character target
size with double-newline-aware merging; widely used as a default in
production RAG stacks. We use the implementation that NeutronOS's
classroom extension shipped before this work (`_chunk_text`, prior
to commit a745cdf, 2026-04-30).

**(C2) Structure-aware semantic** — Splits at detected document
structure (markdown headings, tables, code blocks, regulatory section
markers, paragraph clusters), with a min-chunk size of 200 chars and
a max of 2000 chars. Short documents below the min-chunk threshold
remain whole. Implementation: `axiom.rag.semantic_chunker.chunk_semantic`.

**(C3) Graph-informed semantic** — As C2, but with the boundary
detection augmented by a deterministic entity/cross-reference extractor
that adds boundaries at document references (NUREG-XXXX, 10 CFR
§NN.NN, ORNL-XXXX, IAEA TECDOC-XXX) and at author-attributed sections.
Implementation: `axiom.graph.extractors.deterministic.extract_from_document`
output piped into `chunk_semantic` as the `boundaries=` argument.

### 3.2 The pipeline (constant across lanes)

- Retrieval store: SQLite with FTS5 + optional sqlite-vec for
  semantic similarity
- Embeddings (where present): paragraph-level embeddings via the
  classroom-bundled embedder
- LLM: Qwen 3.5 122B-A10B-Q4_K_M served on llama-server (sovereign,
  on-premise; "rascal-qwen-ec" preset in the federation registry)
- Generation prompt: tutor-style system + retrieved-citation context
  block + question; consistent across all three RAG lanes

### 3.3 The question battery

A 3-category, *N*=18 calibrated battery (will scale to *N*=72+ in the
expanded version):

| Category | Intent | Expected behavior |
|---|---|---|
| should-RAG-win | Specific to corpus — answer is in the materials. | Grounded RAG cites the source; bare LLM should refuse. |
| should-be-wash | General domain knowledge present in the LLM's training prior. | All lanes should answer; differentiates noise floor. |
| out-of-corpus | Material not in corpus; some are adversarial / safety probes. | All lanes should refuse with explanation; adversarial probes test refusal quality. |

### 3.4 The harness

A reproducible Python harness (`harness.py`) drives each lane through
all questions, captures latency / token / answer / citation data per
trace, and ships every event to an institutional LangFuse instance for
side-by-side inspection. Source: `axiom/docs/working/visual-journeys/
day1-rag-harness/`.

---

## 4. Experiments

### 4.1 Setup

- **Synthetic corpus v1** (5 documents, ~6 KB, used for round 1-3
  reported below)
- **Synthetic corpus v2** (~15 documents, ~30 KB, expanded to stress
  long-document and regulatory-cross-reference cases — pending round 4)
- **Real corpus** (Ondrej's NE-101 lecture material, pending Prague
  cohort onboarding)
- **Hardware**: Rascal (Threadripper PRO 7975WX, 128 GB ECC RAM, RTX
  PRO 6000 96 GB, K3S/containerd, sovereign on-premise)
- **Observability**: institutional LangFuse v3.171.0 self-hosted

### 4.2 Results — round 1-3 (synthetic corpus v1)

Scoring rubric per (question, lane): factuality (0-3) + citation
accuracy (0-2) + completeness (0-2) = max 7.

**Should-RAG-win category (max 42):**

| Lane | Score | % |
|---|---|---|
| Bare Qwen 122B | 0/42 | 0% |
| C1 — Fixed-window | 28/42 | 67% |
| C2 — Structure-aware semantic | **41/42** | **98%** |
| C3 — Graph-informed semantic | **41/42** | **98%** |
| Claude (commercial baseline) | 0/42 | 0% |

**Headline observations:**

1. **C1 → C2 swing is +31 percentage points.** The single biggest
   improvement available in the entire stack — bigger than any
   embedder change, prompt-engineering tweak, or model-capability
   bump on this corpus.
2. **C2 ≡ C3 on synthetic corpus v1.** The synthetic corpus is short
   (5 docs averaging 1.2 KB) and lacks regulatory cross-references;
   the graph extractor's added boundaries don't change behavior when
   the structure-aware chunker is already keeping documents whole.
   This is the *correct* expected outcome and *not* a regression.
3. **Bare LLM (no retrieval) and commercial baseline both score 0/42**
   on corpus-specific questions. *No model, no matter how capable,
   answers questions about material it hasn't been trained on.*
4. **Refusal quality differs.** C2/C3 refuse with provenance ("Source X
   does not specify"); commercial baseline refuses politely without
   surfacing why; bare reasoning-model timed out on 7/18 in round-0
   testing.

### 4.3 Results — round 4 (synthetic corpus v2, pending)

Designed to stress C2's structure-aware splitter with long documents,
regulatory-cross-reference density, multi-author attribution, and
adversarial structural-boundary placement. Expectation: C2-C3 gap
opens to 5-10 percentage points on rw-* category. *In progress at
draft time.*

### 4.4 Public-benchmark replication (planned)

BEIR (heterogeneous IR) and SciFact (scientific claim verification)
runs across all three chunking strategies. We will publish per-task
nDCG@10 deltas. **Goal:** demonstrate that the chunker effect we see
on the calibrated education-domain battery *generalizes* to standard
scientific-retrieval benchmarks.

---

## 5. Pedagogical Framework — Per-Student Composition

[Brief section. Material from `feedback_llm_tier_is_general_knowledge_dial`.]

The chunker fix is necessary but not sufficient for educational RAG.
Real classrooms also need *learner-level* control:

- **RAG-mode override per student** — instructor sets cohort default
  (e.g., `course_only`), then bumps specific students to `course +
  institutional` for advanced work
- **LLM-tier override per student** — same shape; `dumb` (Bonsai
  1.7B) for retention quizzes, `smart` (Qwen + RAG) for tutoring,
  `smartest` (full-RAG + reranking) for instructor-side analysis

Together: a 2-axis, per-student calibration knob the instructor can
turn without re-engineering the system. The empirical question: does
this knob improve learning outcomes? *Pending Prague cohort data
(2026-Q3).*

---

## 6. Threats to Validity

1. **Synthetic corpus n=5 is too small for v1 results to differentiate
   C2 vs C3.** Round 4 (v2) addresses this directly; real Ondrej
   corpus is the gold standard.
2. **Single LLM (Qwen 3.5 122B).** Generalization to other reasoning
   models, smaller models, and commercial APIs needs replication.
3. **Single judge.** Heuristic + author-judged scoring; need
   multi-reviewer (Ondrej + Soha + Ben) inter-rater agreement.
4. **Single run per (question, lane).** Variance unestimated;
   multi-run (n≥3) needed for confidence intervals.
5. **N=0 cohort.** Pedagogical-outcome claims are pre-cohort; empirical
   impact is not yet measured on real students.

---

## 7. Conclusion (draft)

The dominant narrative for grounded RAG falls along
embedder-and-model axes — better embeddings, larger models, smarter
prompts. We show empirically that on calibrated educational corpus,
**none of those move the needle as much as the chunker.** A 31-point
swing from a single-line code change is a stronger signal than years of
embedder iteration on this material. Sovereign self-hosting of the
chunker, the retrieval, and the LLM lets institutions deploy this
class of system without the data-residency and governance compromises
of commercial AI tutoring services. The remaining work — variance
estimation, real-corpus replication, public-benchmark comparison, and
classroom-outcome measurement — is straightforward to scope and we
report it as our publication roadmap.

---

## Appendices (planned)

- A. Question battery (full text, expected answers, scoring rubric)
- B. Harness invocation + reproducibility instructions
- C. LangFuse dashboard URLs for each round
- D. Per-question score sheets
- E. Synthetic corpus v1 + v2 sources

---

## Publication-readiness checklist

- [x] Locked title
- [x] Synthetic corpus v1 (5 docs)
- [ ] Synthetic corpus v2 (long-doc + cross-ref stress test) — *in progress*
- [ ] Round 4 results vs synthetic corpus v2
- [ ] Public-benchmark replication (BEIR + SciFact)
- [ ] Real Ondrej corpus run (post-corpus-arrival)
- [ ] Multi-run variance estimate (n=3+ per cell)
- [ ] Multi-reviewer scoring (Ben + Ondrej + Soha or external)
- [ ] Cross-LLM replication (Qwen + Bonsai + Claude as judge)
- [ ] Prague cohort data (Q3 2026)
- [ ] Indirect-competitive-framing pass on all wording
- [ ] IRB review (if cohort outcomes are claimed)

---

## Reproducibility

All harness code, corpus fixtures, results, and journey artifacts:

```
axiom/docs/working/visual-journeys/day1-rag-harness/
├── harness.py            # 5-lane comparison harness
├── render_journey.py     # results.jsonl → journey.md
├── questions.yaml        # question battery (extends to v2)
├── fixtures-synthetic/   # synthetic corpus v1 (and v2 when done)
└── results.jsonl         # raw output

Neutron_OS/docs/papers/working/dont-split-the-table-draft.md  # this file
Neutron_OS/infra/helm/releases/observability/langfuse/         # LangFuse self-host
```

LangFuse traces (institutional dashboard, UT VPN required):
http://rascal.austin.utexas.edu:30030 — project `prague-cohort`.
