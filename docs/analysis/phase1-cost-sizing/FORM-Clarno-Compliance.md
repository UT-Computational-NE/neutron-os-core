# Cost Estimation Form: Dr. Clarno — Compliance & Approval

**For:** Dr. Clarno (Director / Compliance / Budget Approval)  
**Time to Complete:** 5 minutes  
**Deadline:** Friday, Feb 20, 2026, 5 PM ⚠️ **BLOCKING GATES**  
**Submit to:** Ben  

---

## Overview

I need your help with three critical decisions that affect the cost estimate significantly:

1. **ITAR Compliance** — ±30% cost impact (Standard AWS vs. GovCloud)
2. **Data Retention Requirements** — 3x variation in storage costs
3. **TACC Allocation Status** — Affects HPC offloading strategy

Your decisions also determine budget flexibility and risk profile for Phase 1 (2026–2027).

---

## Question 1 (BLOCKING): ITAR Compliance Ruling

### Do TRIGA operations require GovCloud (ITAR-compliant) or can we use standard AWS?

**Background:** TRIGA handles nuclear reactor data which may be subject to ITAR export controls. GovCloud is an isolated AWS region designed for controlled data. It costs ~30% more than standard AWS.

**Options:**
- [ ] **Standard AWS** — Not ITAR-controlled; standard AWS fine ($1,134/mo Recommended)
- [ ] **GovCloud** — ITAR-controlled; must use AWS GovCloud (+30% cost = $1,474/mo Recommended)
- [ ] **Uncertain** — Need legal review before Feb 20

**Your answer:** _______________________________________________

**Why it matters:**
- Standard AWS: $1,134/mo baseline (Recommended)
- GovCloud: $1,474/mo baseline (Recommended) — adds ~$340/mo
- **Phase 1 impact:** ±$4,080 annually

**Next steps:** If uncertain, we can proceed with standard AWS estimate and revise if legal guidance changes.

---

## Question 2 (BLOCKING): Data Retention Compliance Requirement

### How long must operational/audit data be retained? (Years)

This includes:
- Reactor operation logs
- Safety system records
- Audit trails (access logs, configuration changes)
- Experimental datasets

**Options:**
- [ ] **1 year** — Short-term research data only ($30/mo storage)
- [ ] **2 years** — Standard research operations ($60/mo storage)
- [ ] **5 years** — Extended compliance requirement ($150/mo storage)
- [ ] **7 years** — Financial/legal audit requirement ($210/mo storage)
- [ ] **Uncertain** — varies by data type; specify below

**Your answer:** _______________________________________________

**If "varies by data type," can you clarify?**
- Operational logs: _____ years
- Safety records: _____ years
- Audit trails: _____ years
- Experimental data: _____ years

**Why it matters:**
- 1 year: Minimal storage cost
- 2 years: Standard split (30% hot S3, 70% cold Glacier)
- 5 years: Primarily cold storage, slow access
- 7 years: Maximum compliance, minimal access

---

## Question 3: TACC Allocation Status

### Is TACC HPC allocation active through 2027?

**Background:** MPACT simulations currently run on TACC (XSEDE allocation). If TACC allocation ends, we may need to shift compute to AWS, significantly increasing costs.

**Options:**
- [ ] **Yes** — TACC active through 2027+ (keep MPACT on TACC)
- [ ] **No** — TACC ending 2026 (shift MPACT to AWS)
- [ ] **Uncertain** — allocation under review

**Your answer:** _______________________________________________

**Why it matters:**
- TACC active: Estimated allocation cost remains implicit, infrastructure costs manageable
- TACC ending: Must provision GPU nodes on AWS (~$3+/hour) → increases compute cost 50–100%

**If uncertain:** When do you expect a decision? _______________________________________________

---

## Question 4 (Optional): Disaster Recovery & Multi-Region Needs

### Do Phase 1 operations require multi-region failover or backup to another facility?

**Options:**
- [ ] No — Single region (us-east-1 or us-gov-cloud-east-1) is fine
- [ ] Yes — Backup to another AWS region for DR
- [ ] Maybe — Plan for Phase 1.5 or 2, not Phase 1

**Your answer:** _______________________________________________

**Note:** Multi-region adds ~30–50% to infrastructure cost. Not required for Phase 1, but may be needed later.

---

## Question 5 (Optional): Budget Constraints or Flexibility

### Are there hard budget caps for Phase 1, or flexibility for scaling?

**Options:**
- [ ] Hard cap: Must stay under $_____ /month
- [ ] Target: Prefer $1,000–1,500/month range
- [ ] Flexible: Scale as needed, cost not primary constraint
- [ ] Budget TBD: Waiting on funding confirmation

**Your answer:** _______________________________________________

**Note:** Helps us optimize scenarios. We have Low ($612/mo), Medium ($1,134/mo), High ($2,016/mo) options.

---

## Optional: Additional Governance/Compliance Notes

If you have other compliance requirements (export controls, data residency, audit trails, institutional policies), add them here:

```
(e.g., "Data must not leave US territory", "Annual security audit required")
```

---

## Thank You!

Your decisions are foundational for Phase 1 planning. Even if some answers are "uncertain," your best judgment now helps us scope the budget correctly and escalate questions to legal/compliance as needed.

**Return to:** Ben (email or this form filled out)  
**Deadline:** **Friday, Feb 20, 5 PM** ⚠️

---

## How Your Answers Are Used

| Your Answer | Maps To | AWS Service | Impact |
|------------|---------|---|---|
| Q1: Standard AWS vs. GovCloud | Region selection | AWS Global Infrastructure | ±30% cost (+$340/mo) |
| Q2: Data retention years | Storage tiers | S3 + Glacier | 3x variation ($30–210/mo) |
| Q3: TACC allocation status | Compute location | EKS vs. on-prem | 50–100% cost variance |
| Q4: Multi-region DR | Replication strategy | Cross-region replication | +30–50% cost |
| Q5: Budget constraints | Scenario selection | Architecture optimization | Affects final recommendation |

All costs will be traceable to official AWS pricing pages.

---

## Next Steps After Your Response

1. **Feb 20, 5 PM:** Ben collects all team responses
2. **Feb 24:** Cost estimation tool generates final Recommended, High, and Low scenarios
3. **Feb 25:** Ben prepares Executive Summary + Cost Tables + Technical Justification
4. **Feb 27:** Deliver to Dr. Clarno for review + approval meeting

**Expected outcomes:** 
- Final Phase 1 budget recommendation (with contingency)
- Sensitivity analysis (if assumptions change)
- Architecture comparison (standard AWS vs. GovCloud, etc.)

---

## Recognition

Thank you for your leadership on NeutronOS Phase 1. These decisions ensure the cost estimate reflects real compliance and operational requirements, not just theoretical scenarios.
