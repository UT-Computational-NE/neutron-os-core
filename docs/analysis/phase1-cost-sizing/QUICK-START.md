# Quick Start: Cost Estimation Package

**For stakeholders:** Read this first. Takes 3 minutes.

---

## What You Need To Do (Feb 12–18)

### By Friday, Feb 16 at 5 PM
Fill out your section of: **aws-cost-estimate-data-collection.md**

- **Cole** → Section A (MPACT frequency & physics)
- **Nick** → Section B (Operations & production volume)
- **Max** → Section C (PiXie hardware specs) ← **CRITICAL: Phase 1 yes/no?**
- **Jay** → Section D (ML/RAG/training details)
- **Dr. Clarno** → Section E (Compliance & approval) ← **CRITICAL: ITAR ruling?**

Return your section via email to Ben.

### By Monday, Feb 18 at 5 PM
Ben will submit to Dr. Clarno with budget numbers.

---

## Why We're Asking These Questions

**Every question maps directly to a cost component:**

| Your Input | What It Affects | Dollar Impact |
|-----------|---|---|
| Operating hours/week (Nick) | EKS node count | ±$50–100/mo |
| Data volume (Jay) | S3 storage | ±$20–50/mo |
| PiXie Phase 1 yes/no (Max) | Redpanda Cloud | ±$150–300/mo |
| External access (Nick) | Data egress | ±$20–100/mo |
| ITAR compliance (Dr. Clarno) | AWS region | ±30% total cost |

**See:** COST-ESTIMATION-SOURCES.md for details on each cost.

---

## Three Cost Scenarios

**Based on the questions above, we'll calculate three scenarios:**

| Scenario | PiXie | External Access | Cost |
|----------|-------|---|---|
| **Minimal** | No | No | **$612/mo** |
| **Recommended** ⭐ | Yes | Minimal | **$1,134/mo** |
| **Full Cloud** | Yes | Heavy | **$2,016/mo** |

**Meaning:**
- Minimal: Conservative; PiXie deferred to Phase 2
- Recommended: Balanced; PiXie Phase 1 included
- Full Cloud: Premium; multi-AZ + multi-region + heavy external services

---

## All Costs Are Traceable

Every dollar in the estimate:
1. ✅ Comes from official AWS pricing page (or Redpanda/Anthropic)
2. ✅ Is based on a specific assumption (e.g., "150 GB/year data volume")
3. ✅ Can be verified using AWS Pricing Calculator
4. ✅ Will be tracked monthly against actual spend

**See:** COST-ESTIMATION-SOURCES.md (page 2) for source map showing where every cost comes from.

---

## Five Documents (In Reading Order)

### 1. QUICK-START.md ← You are here (3 min read)

### 2. COST-ESTIMATION-SOURCES.md (5 min read)
**TL;DR:** Where all the numbers come from.
- Five standard tools we use
- Cost source map (every cost traces back to AWS pricing page)
- Confidence levels (which costs are certain? which are uncertain?)

### 3. aws-cost-estimate-data-collection.md (30 min to fill out)
**Your worksheet:** Questions organized by stakeholder.
- Section A: Cole → MPACT & physics
- Section B: Nick → Operations & production
- Section C: Max → PiXie hardware ← **CRITICAL**
- Section D: Jay → ML/RAG/training
- Section E: Dr. Clarno → Compliance & approval ← **CRITICAL**

### 4. aws-cost-estimation-methodology.md (20 min skim, 1 hr deep)
**For the rigorous:** Complete methodology documentation.
- How each question maps to AWS calculator inputs
- Every assumption documented with source
- How costs are verified (using AWS Pricing Calculator + Cost Explorer)

### 5. Other Documents (Reference Only)
- aws-comprehensive-utility-usage.md — Detailed 9-service breakdown
- USING-THE-COST-TOOL.md — How to run the Python calculator (for Ben on Feb 17)
- README-COST-ESTIMATE.md — Master orientation

---

## The Three Blocking Gates

You MUST answer these or the estimate can't be finalized:

### Gate 1: ITAR Compliance (Dr. Clarno) ❌ TBD
**Question:** "Does ITAR require AWS GovCloud?"
- **If Yes:** Costs increase by ~30% (e.g., $1,134 → $1,474/mo)
- **If No:** Use standard AWS pricing (current estimate)

**Impact:** $5K–$7.5K difference over 2 years

### Gate 2: PiXie Phase 1 Inclusion (Max) ❌ TBD
**Question:** "Proceed with PiXie sensor integration now, or defer to Phase 2?"
- **If Yes:** Add $150–300/mo (Redpanda streaming, additional storage)
- **If No:** Save $150–300/mo; implement in Phase 2

**Impact:** $1.8K–$3.6K difference per year

### Gate 3: TACC Allocation Status (Cole + Dr. Clarno) ❌ TBD
**Question:** "Is TACC allocation active through end of 2027?"
- **If Yes:** Keep MPACT on TACC (cheaper); AWS costs lower
- **If No:** Move MPACT to AWS; add GPU compute costs

**Impact:** $100–500/mo depending on MPACT volume

---

## Example Responses (What We're Looking For)

### Cole (Section A):
```
A1a: States per nightly run?
     "Usually 10–20 stable states per day"
     
A1b: Wall-clock time per MPACT?
     "Typically 2–5 minutes per simulation"
     
A2c: Total archive size?
     "About 500 GB of HDF5 files (3 years of history)"
```

### Nick (Section B):
```
B1a: Operating hours per week?
     "Typically 80 hours/week (10 hrs/day, 8 days)"
     
B4a-c: Data volume breakdown of 150GB/year?
       "ZOC logs: 50 GB, MPACT results: 80 GB, misc: 20 GB"
```

### Max (Section C) ← CRITICAL
```
C3a: Phase 1 inclusion (yes/no)?
     "YES, we want PiXie operational in Phase 1"
     
C2a: Current daily data volume?
     "About 0.5 GB/day currently, could increase with more sensors"
```

### Jay (Section D):
```
D1a: RAG document count?
     "About 2,000 documents in corpus (PDFs, protocols, etc.)"
     
D2e: Model retraining frequency?
     "Monthly for physics models, quarterly for AI models"
```

### Dr. Clarno (Section E) ← CRITICAL
```
E1b: ITAR requirement?
     "Yes, export control requires all data on US soil"
     → Standard AWS or GovCloud?
     → [NEEDS DECISION]
     
E1d: TACC allocation status?
     "Active through 2027, with ~50% utilization"
     → Can we keep MPACT on TACC?
     → [CLARIFICATION NEEDED]
```

---

## Questions to Ask Before Answering Your Section

- **Cole:** Any recent MPACT performance benchmarks? Archive growth rate?
- **Nick:** How many researchers? External collaborators accessing Superset?
- **Max:** PiXie ready for Phase 1, or wait for Phase 2? What data rate/format?
- **Jay:** Will researchers actively use RAG, or just background processing?
- **Dr. Clarno:** Can you settle ITAR ruling + TACC status by Feb 16?

---

## The Timeline

```
Today (Feb 12):        ✅ You received this package
Tomorrow (Feb 13):     📧 Stakeholders get email + worksheet
Feb 13–16:             📝 You fill out your section
Friday, Feb 16, 5 PM:  📥 All responses due to Ben
Feb 17 Morning:        🔧 Ben loads data into cost calculator
Feb 17–18:             📊 Ben generates final cost estimates
Monday, Feb 18, 5 PM:  📤 Submit to Dr. Clarno for approval
```

---

## After You Submit Your Section

Ben will:
1. Collect all responses (Feb 16)
2. Resolve the three blocking gates (Feb 16–17)
3. Run the cost calculator (Feb 17)
4. Draft approval documents (Feb 17–18)
5. Submit to Dr. Clarno (Feb 18)

**You don't need to do anything else unless we come back with clarifying questions.**

---

## Key Assumptions (Already Built In)

We've already made these assumptions; you don't need to confirm them:

- ✅ **Data volume:** 150 GB/year baseline (from Jay's estimate)
- ✅ **Hot retention:** 2 years (S3 Standard)
- ✅ **Cold retention:** 5 years (S3 Glacier, for compliance)
- ✅ **AWS region:** US East 1 (unless Dr. Clarno says GovCloud)
- ✅ **Compute:** On-demand EC2 (no reserved instances yet)
- ✅ **Support:** Developer tier (not Business/Enterprise)

**These can be adjusted if you have better data.**

---

## What NOT to Worry About

- 🚫 **Detailed pricing research** — We've already done that
- 🚫 **AWS calculator** — Ben will use that on Feb 17
- 🚫 **Complex formulas** — We've automated it
- 🚫 **Spreadsheets** — No manual calculation needed

**Just answer the questions as accurately as you can.**

---

## Still Have Questions?

**Quick answers:**
- "Why are we collecting this data?" → See COST-ESTIMATION-SOURCES.md (page 3)
- "How confident are these estimates?" → See COST-ESTIMATION-SOURCES.md (page 6)
- "Will prices change?" → See aws-cost-estimation-methodology.md (Section 4)

**Deep questions:**
- Read aws-cost-estimation-methodology.md (complete methodology)
- Or ask Ben directly

---

## TL;DR

1. **You:** Fill out your section of the worksheet by Friday, Feb 16
2. **Ben:** Runs calculator on Feb 17, submits to Dr. Clarno on Feb 18
3. **All costs:** Traceable to official AWS pricing pages
4. **Three scenarios:** Minimal ($612/mo), Recommended ($1,134/mo), Full Cloud ($2,016/mo)
5. **Three critical gates:** ITAR ruling, PiXie Phase 1 yes/no, TACC allocation status

**Next:** Read [COST-ESTIMATION-SOURCES.md](COST-ESTIMATION-SOURCES.md) (5 min) to understand where costs come from.

Then fill out [aws-cost-estimate-data-collection.md](aws-cost-estimate-data-collection.md) with your section.

That's it! 🎯
