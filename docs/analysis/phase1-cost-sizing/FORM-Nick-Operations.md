# Cost Estimation Form: Nick — TRIGA Operations

**For:** Nick (TRIGA Operations / Facility Management)  
**Time to Complete:** 3–5 minutes  
**Deadline:** Friday, Feb 20, 2026, 5 PM  
**Submit to:** Ben  

---

## Precision Expectation

Order-of-magnitude estimates (±50%) are perfect. Rough ranges beat false precision. T-shirt sizing or "I don't know" is fine—we have fallbacks.

---

## Overview

I need your help with:
- How many hours/week TRIGA actually operates
- Data volumes from daily operations
- Operational requirements and constraints

Your answers drive **compute costs** (EKS uptime) and **storage costs** (operational data retention).

---

## Question 1: TRIGA Operating Hours (Compute Costs)

### How many hours per week does TRIGA operate?

This determines how long the Kubernetes cluster needs to run.

**Options:**
- [ ] Research/part-time: 20–40 hrs/week (nights + weekends off)
- [ ] Standard business: 40 hrs/week (8 AM–5 PM weekdays)
- [ ] Extended hours: 60–80 hrs/week (early mornings + some weekends)
- [ ] Continuous: 24/7/365 (rarely shuts down)
- [ ] Variable: specify below

**Your answer:** _______________________________________________

**Typical schedule example:** "Monday–Friday 8 AM–5 PM, plus Saturday operations" = 48 hrs/week

**Impact:**
- 40 hrs/week = $346/mo compute
- 60 hrs/week = $519/mo compute
- 168 hrs/week (24/7) = $1,452/mo compute

---

## Question 2: Operational Data Volume (Storage Costs)

### How much new operational data is generated per year?

This includes:
- Sensor logs (temperature, power, neutron flux, etc.)
- Control system logs
- Experiment logs
- Safety system records

**Options:**
- [ ] Less than 100 GB/year (minimal instrumentation)
- [ ] 100–500 GB/year (typical research reactor)
- [ ] 500 GB–2 TB/year (comprehensive logging)
- [ ] More than 2 TB/year (extensive monitoring; specify below)

**Your answer:** _______________________________________________

**Note:** This is typically much smaller than MPACT outputs. If unsure, estimate 150 GB/year.

**Impact:**
- 100 GB/year = $4/mo storage
- 500 GB/year = $20/mo storage
- 2 TB/year = $80/mo storage

---

## Question 3: Data Access Requirements (Optional Detail)

### How often do operators/researchers access historical data?

This affects whether we keep data "hot" (fast, $0.023/GB/mo) vs. "cold" (slow, $0.004/GB/mo).

**Options:**
- [ ] Daily access (keep hot, faster response)
- [ ] Weekly access (split hot/cold)
- [ ] Monthly access (mostly cold, occasional hot)
- [ ] Archive only (all cold, slow access okay)

**Your answer:** _______________________________________________

**Note:** We'll use "split hot/cold" if you don't have a preference.

---

## Optional: Additional Context

If you have other operational considerations (maintenance windows, seasonal variation, planned upgrades), add them here:

```
(e.g., "TRIGA shuts down for 2 weeks every summer for maintenance")
```

---

## Additional Context (Optional)

Anything else about facility operations, scheduling, or data that affects AWS costs?

_______________________________________________

---

## Thank You!

**Return to:** Ben  
**Deadline:** Friday, Feb 20, 5 PM

---

## How Your Answers Are Used

| Your Answer | Maps To | AWS Service | Impact |
|------------|---------|---|---|
| Q1: Operating hours/week | Cluster uptime | EKS + EC2 | $346–1,452/mo |
| Q2: Operational data volume | Storage needs | S3 | $4–80/mo |
| Q3: Data access frequency | Hot vs. cold storage | S3 tiers | Affects retrieval speed + cost |

All costs will be traceable to official AWS pricing with specific assumptions noted.
