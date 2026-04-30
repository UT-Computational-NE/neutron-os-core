# Paper Portfolio Sequencing — Educational AI Track

> *Locked 2026-04-30 by Ben + Claude (with the 2x2 framework Ben proposed:
> proof complexity × immediate usefulness). Ben works directly with
> Ondrej Chvala + Soha Khan on the lead paper drafting + pedagogy
> framing + skeptic review.*

## Continuous-learning build posture

These papers are **not single-snapshot publications**; they are
checkpoints in an ongoing evidence-accumulation program. Each ships
with an explicit **Hypothesis Ledger** (see lead paper §A) tracking
what we believed at each checkpoint and how subsequent evidence
refined or retracted earlier claims. The published version crystallizes
whichever ledger entries have accumulated sufficient evidence by
submission deadline.

This means the first paper (lead, 2026-Q3) ships *before* we have
all the evidence we'll eventually have — and it explicitly documents
what's still open. Reviewers see the trajectory, not just the
destination.

## The 2x2

```
                          │ Low immediate    │ High immediate
                          │ usefulness       │ usefulness
──────────────────────────┼──────────────────┼─────────────────────
High proof complexity     │  (avoid)         │  C — Federated Tutor
                          │                  │  B — Capability Comp.
──────────────────────────┼──────────────────┼─────────────────────
Low proof complexity      │  (trivial)       │  A — Refusal as Pedagogy
                          │                  │  D — Pedagogical-Intent Eval
                          │                  │  ↑ ship-now / merge as A+D
```

**Decision rule:** ship from the bottom-right quadrant first
(low proof, high usefulness). Reserve top-right for after we have
the empirical infrastructure to defend it. Avoid top-left and
bottom-left.

## Cadence

| Date | Paper | Status | Notes |
|---|---|---|---|
| **2026-Q3** | **Lead** — *Pedagogical-Intent RAG Evaluation: Why Refusal Quality Matters for AI Tutoring* (A+D merged) | drafting | Workshop / short-paper venue. Defensible from Day 1 + round-4 data. Establishes our terminology + battery design as cited prior work for subsequent papers. |
| **2026-Q3 (companion)** | **Tech report** — *Don't Split the Table: Structure-Aware Chunking for Scientific Retrieval* | repositioned 2026-04-30 | Supporting technical report cited from the lead paper. Documents implementation + ablation, not headline contribution. |
| **2027-Q1** | **Flagship** — *The Federated Tutor: Sovereign Cross-Institution Pedagogy Without Data Egress* (C) | sketched | Post-Prague + post-N=2 federation pilot. Cites the lead paper for methodology. The eye-opener: federation makes privacy + scale *both* easier, not a tradeoff. |
| **2027-Q3** | **Empirical** — *Per-Student Capability Composition: Outcomes from a Federated Educational AI Cohort* (B) | future | Post-Prague cohort + cohort 2 with outcome data. Cites C for architecture, lead paper for methodology. The "+15% mastery, -20% DFW" empirical claim. |

## Cross-citation graph

```
[Lead paper A+D] ────────────────────────────────────────┐
   ▲                                                     │
   │ cites for chunker implementation                    │ cites as methodology
   │                                                     ▼
[Tech report — Don't Split the Table]              [Flagship C — Federated Tutor]
                                                         │
                                                         │ cites as architecture
                                                         ▼
                                                   [Empirical B — Capability Composition]
```

## Per-paper proof gates (what we need before each ships)

### Lead (A+D, 2026-Q3)
- [x] Day 1 round 1-3 data
- [⚠] Round 4 expanded-corpus data (in flight)
- [ ] Inter-rater agreement (Ondrej + Ben + external reviewer, 5 sample questions)
- [ ] LLM-as-judge replication of human scoring

### Tech report (chunker, 2026-Q3 companion)
- [x] Round 1-3 data
- [⚠] Round 4 V2 vs V3 ablation
- [ ] BEIR public-benchmark replication (planned)
- [ ] SciFact public-benchmark replication (planned)

### Flagship (C, 2027-Q1)
- [ ] Prague cohort completed (Q3 2026)
- [ ] N=2 federation pilot (Prague + 1 peer institution; Q4 2026)
- [ ] Cross-institution comparable mastery measurement
- [ ] Federated misconception aggregation pilot data
- [ ] Trust-graph attestation prototype

### Empirical (B, 2027-Q3)
- [ ] Prague cohort outcome data (Q3 2026)
- [ ] Cohort 2 outcome data (Q1 2027)
- [ ] Per-student RAG-mode + LLM-tier override implemented (tasks #12, #14)
- [ ] Outcome correlation analysis (mastery rate vs tier composition)

## Why this ordering

1. **A+D ships first because it's defensible TODAY** and costs almost nothing extra to publish (data already in hand). Establishes our terminology and methodology as cited prior work for our own subsequent papers — that's leverage we get only by going first.

2. **C is the flagship**, but it depends on infrastructure (Prague cohort + N=2 federation) we don't yet have. Publishing C without empirical evidence would be vision-paper category, which isn't where we want our flagship to land.

3. **B comes last** because it requires both architectural infrastructure (per-student composition primitive implemented) AND outcome data (cohort 1 + cohort 2). That's a long-tail dependency.

4. **The chunker work stays valuable** as a supporting technical report — cited but not headline. This avoids the prior-art trap (structure-aware chunking is a recognized field; it's not the eye-opener).

## What we explicitly do NOT publish

- A standalone chunker paper (structure-aware chunking is established prior art; would risk desk-rejection)
- A standalone "AI in nuclear engineering education" paper (too niche without methodological contribution)
- Vision papers without empirical anchoring (top-right quadrant requires actual data; pure-vision papers don't fit our 2x2 strategy)
