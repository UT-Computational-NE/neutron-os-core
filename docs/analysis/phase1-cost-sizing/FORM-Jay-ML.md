# Cost Estimation Form: Jay — ML/Data Engineering

**For:** Jay (ML Engineering / Data Pipeline / Shadowcasting)  
**Time to Complete:** 4–6 minutes  
**Deadline:** Wednesday, Feb 16, 2026, 5 PM ⚠️ **BLOCKING GATE**  
**Submit to:** Ben  

---

## Precision Expectation

Order-of-magnitude estimates (±50%) are perfect. Rough ranges beat false precision. T-shirt sizing or "I don't know" is fine—we have fallbacks.

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

## Additional Context (Optional)

Anything else about ML pipelines, data, or Claude API usage that affects costs?

_______________________________________________

---

## Thank You!

**Return to:** Ben  
**Deadline:** Wednesday, Feb 16, 5 PM ⚠️
