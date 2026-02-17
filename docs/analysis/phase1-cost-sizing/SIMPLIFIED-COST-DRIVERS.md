# Simplified Cost Estimation: Order of Magnitude Approach

**Document Purpose:** Identify 5-6 biggest cost drivers (~80% of total cost). Everything else estimated intelligently.  
**Timeline:** Feb 13–27, 2026  
**Status:** Ready for team distribution  
**Deadline:** Friday, Feb 27, 5 PM (responses)

---

## 🎯 The 80/20 Rule Applied

Instead of asking 50+ questions, focus on **6 critical inputs** that drive most of the cost variation. Fill everything else with reasonable estimates.

| Rank | Cost Driver | Range | Impact | Source | Question For |
|------|-------------|-------|--------|--------|--------------|
| **1** | **Data egress patterns** | $0–$500/mo | 10x variation | Network bandwidth | Nick + Cole |
| **2** | **PiXie Phase 1 yes/no** | $0 or +$150–300/mo | Binary decision | Hardware scope | Max |
| **3** | **EKS operating hours/week** | 40–168 hrs | 4x variation | Compute | Nick |
| **4** | **Data retention policy** | 1yr–5yr | 3x variation | Storage | Dr. Clarno |
| **5** | **Claude API query volume** | 0–100 queries/day | 10x variation | External services | Jay |
| **6** | **ITAR compliance** | Standard AWS or GovCloud | +30% cost | Region + compliance | Dr. Clarno |

---

## Why These Six?

### 1. Data Egress ($0–500/mo, **10x variation**)
- **What it is:** Internet data leaving AWS (e.g., reports, external access)
- **Why it varies:** TRIGA operations might push 1–10 TB/month out of AWS
- **Cost:** $0.09/GB egress
- **Our estimate if not provided:** 100 GB/month = $9/mo (conservative)
- **Ask:** Cole + Nick: "How much data moves out of AWS monthly?" (reports, external collaborators, backups)

### 2. PiXie Phase 1 (Binary, **+$150–300/mo**)
- **What it is:** High-speed data acquisition hardware connected to cluster
- **Why it matters:** Drives Redpanda Cloud costs, storage costs, network costs
- **Our estimate if "No":** $0 for PiXie (use standard TRIGA data sources)
- **Our estimate if "Yes":** $250/mo base Redpanda + 20 GB/day storage
- **Ask:** Max: "Is PiXie Phase 1 happening in 2026, yes or no?"

### 3. EKS Operating Hours ($167–350/mo, **4x variation**)
- **What it is:** How many hours/week is the cluster actually running?
- **Cost:** $0.10/hour per on-demand node (2 nodes recommended)
- **Our estimate if not provided:** 40 hrs/week = $80/week = $346/mo (standard business hours)
- **Ask:** Nick: "How many hours/week does TRIGA operate?"

### 4. Data Retention Policy ($24–150/mo, **3x variation**)
- **What it is:** How long do you keep historical data warm/cold?
- **Cost:** S3 Standard (hot): $0.023/GB/mo; Glacier (cold): $0.004/GB/mo
- **Our estimate if not provided:** 2 years history = split 30% hot + 70% cold
- **Ask:** Dr. Clarno: "What's the compliance requirement for data retention?" (audit logs, operational logs)

### 5. Claude API Query Volume ($100–400/mo, **10x variation**)
- **What it is:** How many times/day does the RAG system query Claude?
- **Cost:** $0.80 per 1M input tokens (~4,000 queries/mo at ~200 tokens each)
- **Our estimate if not provided:** 10 queries/day = $24/mo (minimal RAG usage)
- **Ask:** Jay: "How many Claude API calls/day in Phase 1?" (shadowcasting, meeting intake)

### 6. ITAR Compliance (Binary, **+30% cost if GovCloud**)
- **What it is:** Standard AWS ($) vs. GovCloud AWS (+30% premium)
- **Why:** TRIGA may handle ITAR-controlled reactor data
- **Our estimate if not provided:** Standard AWS (conservative)
- **Ask:** Dr. Clarno: "Do we need GovCloud for ITAR compliance, or standard AWS sufficient?"

---

## Data Collection: The Short Form

### For Cole (Physics/MPACT)
- **Q1:** How much data leaves AWS monthly? (reports, external collaborators, validation data)  
  *Estimate: 100 GB/mo if not provided*
- **Q2:** How much historical MPACT simulation data should migrate to AWS?  
  *Estimate: 100 GB archive if not provided*

### For Nick (TRIGA Operations)
- **Q1:** How many hours/week does TRIGA operate?  
  *Estimate: 40 hrs/week if not provided*
- **Q2:** How much data moves out of AWS monthly?  
  *Estimate: 100 GB/mo if not provided*

### For Max (PiXie Hardware)
- **Q1 (BLOCKING):** Is PiXie Phase 1 happening in 2026, yes or no?  
  *No estimate—must ask*
- **Q2 (if yes):** How much data per day from PiXie?  
  *Estimate: 20 GB/day if not provided*

### For Jay (ML/Data Engineering)
- **Q1:** How many Claude API calls/day in Phase 1? (shadowcasting, meeting intake, RAG queries)  
  *Estimate: 10 queries/day if not provided*
- **Q2:** How much training data (GB) for bias correction models?  
  *Estimate: 5 GB if not provided*

### For Dr. Clarno (Compliance/Approval)
- **Q1 (BLOCKING):** Do we need GovCloud for ITAR compliance, or standard AWS?  
  *No estimate—must ask*
- **Q2 (BLOCKING):** What's the compliance requirement for data retention? (1yr? 5yr? 7yr audit logs?)  
  *Estimate: 2 years if not provided*
- **Q3:** Is TACC allocation active through 2027?  
  *Estimate: Yes, active if not provided*

---

## How We Fill in the Rest

**For any question not answered by the team, we use:**

1. **Conservative estimate** (lower bound, safe for budgeting)
2. **Stated rationale** (e.g., "Assumed 40 hrs/week business operations")
3. **Sensitivity range** (e.g., "Cost ranges $X–Y if hours/week varies 20–80")

**Example:** If Nick doesn't respond about egress:
```
Q: "How much data moves out of AWS monthly?"
Assumption: 100 GB/month (conservative, typical research operations)
Source: AWS documentation on egress patterns
Cost: 100 GB × $0.09/GB = $9/month
Sensitivity: If 1 TB/mo → $90/mo; if 10 TB/mo → $900/mo
```

This way, the estimate is **defensible and traceable**, even with missing data.

---

## Timeline: Feb 13–27

| Date | Action | Deadline |
|------|--------|----------|
| **Feb 13** | Email personalized forms to Cole, Nick, Max, Jay, Dr. Clarno | EOD |
| **Feb 16, 5 PM** | Receive responses from Max, Jay (blocking gates) | Hard deadline |
| **Feb 20, 5 PM** | Receive responses from Cole, Nick, Dr. Clarno | Hard deadline |
| **Feb 24** | Load all responses into cost_estimation_tool | EOD |
| **Feb 25–26** | Generate final estimates + sensitivity analysis | EOD |
| **Feb 27, 5 PM** | Deliver to Dr. Clarno: Executive Summary + Cost Tables + Justification | Final deadline |

---

## Blocking Gates (Must Ask)

These questions **cannot be estimated**. We must have answers:

1. **Max:** "Is PiXie Phase 1 happening in 2026?"
2. **Dr. Clarno:** "GovCloud or standard AWS?"
3. **Dr. Clarno:** "Data retention compliance requirement?"

Without these, cost estimate is incomplete.

---

## Confidence Levels

| Scenario | Estimated Cost | Confidence | Driver |
|----------|---|---|---|
| Minimal (no PiXie) | $612/mo | High | Few variables, most controllable |
| Recommended (PiXie yes, 40 hrs/week) | $1,134/mo | Medium | Depends on egress + RAG usage |
| Full Cloud (heavy usage, GovCloud) | $2,016/mo | Low | Many assumptions about scale |

**Key uncertainty:** Egress patterns (can vary 10x). Everything else is well-understood.

---

## What NOT to Ask

❌ Don't ask for exact counts of every data point  
✅ Do ask for order of magnitude (tens of GB? hundreds? thousands?)

❌ Don't ask for granular weekly breakdowns  
✅ Do ask for ranges ("20–50 hours/week?" or "high/medium/low usage?")

❌ Don't ask about implementation details we can look up  
✅ Do ask about constraints that change cost (ITAR, data retention, compliance)

---

## Document Organization

This doc establishes the **simplified approach**. Each stakeholder gets a personalized questionnaire:

- [FORM-Cole-Physics.md](FORM-Cole-Physics.md) — 2 key questions + 3 estimates
- [FORM-Nick-Operations.md](FORM-Nick-Operations.md) — 2 key questions + 3 estimates
- [FORM-Max-PiXie.md](FORM-Max-PiXie.md) — 1 blocking question + 2 estimates
- [FORM-Jay-ML.md](FORM-Jay-ML.md) — 2 key questions + 3 estimates
- [FORM-Clarno-Compliance.md](FORM-Clarno-Compliance.md) — 3 blocking questions + 2 estimates

**All forms:** ~5 min to fill out, immediate high-value response.

---

## Bottom Line

✅ **6 critical questions** → 80% of cost variation identified  
✅ **5 intelligent estimates** → fills remaining 20%  
✅ **3 blocking gates** → ensure completeness  
✅ **Traceable assumptions** → every estimate documented  
✅ **2-week timeline** → enough time for quality responses  

**Result:** Defensible cost estimate ready by Feb 27 for Dr. Clarno approval.
