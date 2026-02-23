# Cost Estimation Form: Dr. Clarno — Compliance & Approval

**For:** Dr. Clarno (Director / Compliance / Budget Approval)  
**Time to Complete:** 5 minutes  
**Deadline:** Friday, Feb 20, 2026, 5 PM ⚠️ **BLOCKING GATES**  
**Submit to:** Ben  

---

## Precision Expectation

Order-of-magnitude estimates (±50%) are perfect. Rough ranges beat false precision. T-shirt sizing or "I don't know" is fine—we have fallbacks.

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

## Additional Context (Optional)

Any other compliance, budget, or policy constraints that affect Phase 1 scoping?

_______________________________________________

---

## Thank You!

**Return to:** Ben  
**Deadline:** Friday, Feb 20, 5 PM ⚠️
