# Cost Estimation Form: Jay — ML/Data Engineering

**For:** Jay (ML Engineering / Data Pipeline / Shadowcasting)  
**Time to Complete:** 4–6 minutes  
**Deadline:** Wednesday, Feb 16, 2026, 5 PM ⚠️ **BLOCKING GATE**  
**Submit to:** Ben  

---

## Overview

I need your help with the AI/RAG architecture for NeutronOS:
- **RAG systems** (document indexing, retrieval, Claude API integration)
- **Embeddings & semantic search** (knowledge base indexing)
- **Claude API integration** (querying LLMs for analysis & assistance)
- **Shadowcasting** (MPACT prediction comparison using AI)

Your answers drive **external service costs** (Claude API, embeddings) and **compute costs** (inference, semantic search).

---

## Question 1 (BLOCKING): Claude API Usage

### How many Claude API calls per day in Phase 1 operations?

This includes:
- **Meeting intake** (extracting requirements from meeting recordings/notes)
- **Shadowcasting** (generating MPACT-like predictions for comparison)
- **RAG queries** (semantic search over documentation)
- **Anomaly analysis** (interpreting unexpected reactor behavior)

**Estimation help:**
- Meeting intake: ~2 calls/week if 1 meeting/week
- Shadowcasting: ~5–10 calls/day (depends on batch frequency)
- RAG: ~1–5 calls/day (depends on user queries)
- Anomaly analysis: ~2–3 calls/week

**Options:**
- [ ] Light: 0–5 calls/day (~$24/mo)
- [ ] Moderate: 5–20 calls/day (~$100/mo)
- [ ] Heavy: 20–50 calls/day (~$250/mo)
- [ ] Very heavy: 50+ calls/day (specify below)

**Your answer:** _______________________________________________

**If "Very heavy," how many?** _____ calls/day

**Note:** Can be refined later if usage patterns change. Phase 1 baseline assumption: ~10 calls/day = $48/mo.

---

## Question 2 (BLOCKING): Training Data Requirements

### How much historical training data (GB) needed for bias correction + other ML models?

This affects storage costs and one-time migration volume.

**Options:**
- [ ] Minimal: 1–5 GB (sparse training, curated datasets)
- [ ] Typical: 5–20 GB (standard research ML setup)
- [ ] Comprehensive: 20–100 GB (extensive historical comparison)
- [ ] Extensive: 100+ GB (specify below)

**Your answer:** _______________________________________________

**If "Extensive," how much?** _____ GB

**Note:** If unsure, assume "Typical: 5–20 GB". Includes MPACT runs, measured data, external datasets.

**Impact:**
- 5 GB = $1/mo storage
- 20 GB = $4/mo storage
- 100 GB = $20/mo storage

---

## Question 3: Model Retraining Frequency

### How often should bias correction + prediction models retrain?

**Options:**
- [ ] Annual: Once per year (cost: ~$200/year compute)
- [ ] Quarterly: Every 3 months (cost: ~$75/quarter)
- [ ] Monthly: Every month (cost: ~$50/month)
- [ ] Continuous: Online learning as new data arrives (cost: ~$100/month)
- [ ] As-needed: Only when performance degrades (cost: $0 baseline)

**Your answer:** _______________________________________________

**Note:** Monthly is typical for production ML systems with stable data.

---

## Question 4: Shadowcasting Approach (Optional Detail)

### How will shadowcasting run in Phase 1?

This affects compute + storage:

**Options:**
- [ ] Nightly batch (run once/day like today on TACC) — minimal cost
- [ ] Continuous background (streaming predictions) — moderate cost
- [ ] On-demand (only when reactor state changes) — minimal cost
- [ ] Multiple per day (3–4x/day for different scenarios) — higher cost

**Your answer:** _______________________________________________

**Note:** We'll assume "Nightly batch" if you don't specify. Can scale up in Phase 2.

---

## Optional: Additional Context

If you have other ML/data engineering considerations (new models planned, external datasets, collaborators), add them here:

```
(e.g., "Planning to integrate external datasets for flux prediction in Phase 1.5")
```

---

## Thank You!

Your detailed knowledge of the data pipeline is essential for accurate cost estimation. Your work on shadowcasting, meeting intake, and RAG systems is driving a lot of the platform value—this form ensures the infrastructure costs reflect that.

**Return to:** Ben (email or this form filled out)  
**Deadline:** **Wednesday, Feb 16, 5 PM** ⚠️ (blocking gate)

---

## How Your Answers Are Used

| Your Answer | Maps To | AWS Service | Impact |
|------------|---------|---|---|
| Q1: Claude API calls/day | API costs | Anthropic Claude | $24–$400+/mo |
| Q2: Training data volume | Storage needs | S3 | $1–20/mo |
| Q3: Retraining frequency | Compute hours | EC2 | $0–100+/mo |
| Q4: Shadowcasting frequency | Batch compute | EKS + EC2 | $50–300/mo |

All costs will be traceable to official AWS + Anthropic pricing pages.

---

## Recognition

Thank you for the extensive work on shadowcasting, meeting intake, and RAG systems. Your innovations are driving much of NeutronOS Phase 1's value. This cost estimate ensures the infrastructure budget reflects that contribution.

---

## Why Feb 16 Deadline?

Q1 and Q2 block downstream architecture decisions:
- External service budget (Claude API is ~10% of total in Recommended scenario)
- Storage architecture (training data affects S3 sizing)
- Compute allocation (retraining frequency affects node sizing)

**Answer by Feb 16 EOD → Ben can finalize infrastructure scope by Feb 20.**
