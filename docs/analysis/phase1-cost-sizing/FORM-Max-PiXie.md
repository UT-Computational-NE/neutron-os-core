# Cost Estimation Form: Max — PiXie Hardware

**For:** Max (PiXie DAQ / Hardware Integration)  
**Time to Complete:** 3 minutes  
**Deadline:** Wednesday, Feb 16, 2026, 5 PM ⚠️ **BLOCKING GATE**  
**Submit to:** Ben  

---

## Overview

I need your help with:
- Whether PiXie Phase 1 is happening in 2026
- Data volume and format from the DAQ system
- Hardware integration timeline

Your answer to **Question 1** determines ~$150–300/mo of the cost estimate. This is a blocking gate—we cannot estimate further without it.

---

## Question 1 (BLOCKING): PiXie Phase 1 in 2026? ⚠️

### Is PiXie Phase 1 hardware connected to the cluster in 2026?

**Options:**
- [ ] **YES** — PiXie is operational in 2026 (proceed to Q2 + Q3)
- [ ] **NO** — PiXie deferred to 2027 or later (cost estimate excludes PiXie)
- [ ] **UNCERTAIN** — needs decision before Feb 20

**Your answer:** _______________________________________________

**Why this matters:**
- **YES:** Adds Redpanda Cloud ($150–300/mo) + extra storage + network capacity
- **NO:** Simpler architecture, lower baseline cost ($612/mo Minimal scenario)
- **Cost difference:** ~$200/mo annually (impacts budget by ~$2,400 in Phase 1)

---

## Question 2 (IF "YES"): Data Volume from PiXie

### How much data per day from the PiXie DAQ system?

**Options:**
- [ ] Light: 1–5 GB/day (sparse sampling, limited sensors)
- [ ] Moderate: 5–20 GB/day (typical high-speed acquistion)
- [ ] Heavy: 20–50 GB/day (continuous, multi-detector)
- [ ] Extreme: 50+ GB/day (streaming all channels; specify below)

**Your answer:** _______________________________________________

**Note:** If unsure, estimate "Moderate: 5–20 GB/day" for high-speed physics DAQ.

**Impact:**
- 5 GB/day = $20/mo storage + $50/mo Redpanda
- 20 GB/day = $80/mo storage + $150/mo Redpanda
- 50 GB/day = $200/mo storage + $300/mo Redpanda

---

## Question 3 (IF "YES"): Data Format & Retention

### How long should PiXie data stay "hot" (immediately accessible)?

**Options:**
- [ ] Short-term: 1–2 weeks (quick analysis, then archive)
- [ ] Medium-term: 1–3 months (active research window)
- [ ] Long-term: 6–12 months (comprehensive historical analysis)
- [ ] Depends on use case; specify below

**Your answer:** _______________________________________________

**Note:** We'll use "Medium-term: 1–3 months" if you don't specify.

---

## Optional: Additional Context

If you have other PiXie considerations (upgrades planned, detector changes, sampling rate constraints), add them here:

```
(e.g., "PiXie sampling rate increases 10x in Phase 1.5")
```

---

## Thank You!

Your response is **critical** for budget planning. Even if uncertain, your best estimate helps.

**Return to:** Ben (email or this form filled out)  
**Deadline:** **Wednesday, Feb 16, 5 PM** ⚠️ (earlier than others—blocking gate)

---

## How Your Answers Are Used

| Your Answer | Maps To | AWS Service | Impact |
|------------|---------|---|---|
| Q1: PiXie yes/no | Architecture scope | EKS + Redpanda | $0 or +$200–300/mo |
| Q2: Data volume/day | Throughput tiers | S3 + Redpanda | Scales costs linearly |
| Q3: Retention window | Storage class mix | S3 Standard vs. Glacier | Affects retrieval speed |

All costs will be traceable to official AWS + Redpanda pricing pages.

---

## Why Feb 16 Deadline?

This blocks several downstream decisions:
- Storage architecture (S3 Standard vs. Glacier mix)
- Redpanda cluster sizing
- Network egress budget
- Compute resource allocation

**Answer by Feb 16 EOD → Ben can consolidate all Phase 1 scope by Feb 20.**
