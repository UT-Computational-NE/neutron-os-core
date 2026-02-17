# Phase 1 AWS Cost Sizing Exercise

**Period:** February 13–27, 2026  
**Objective:** Estimate infrastructure costs for NeutronOS Phase 1 (TRIGA digital twin, 2026–2027)  
**Approach:** Simplified 6-critical-question methodology + intelligent estimates  
**Deadline:** February 27, 2026, 5 PM (submit to Dr. Clarno)

---

## Quick Navigation

### For Team Distribution (Feb 13)
- **[COST-ESTIMATION-SIMPLIFIED-COVER.md](COST-ESTIMATION-SIMPLIFIED-COVER.md)** — Email to send to all stakeholders

### For Understanding the Approach
- **[SIMPLIFIED-COST-DRIVERS.md](SIMPLIFIED-COST-DRIVERS.md)** — Why 6 questions? What gets estimated?

### Personalized Forms (Each 3–6 minutes)
- **[FORM-Cole-Physics.md](FORM-Cole-Physics.md)** — Physics/MPACT data (deadline: Feb 20)
- **[FORM-Nick-Operations.md](FORM-Nick-Operations.md)** — TRIGA operations (deadline: Feb 20)
- **[FORM-Max-PiXie.md](FORM-Max-PiXie.md)** — PiXie hardware (deadline: **Feb 16** ⚠️)
- **[FORM-Jay-ML.md](FORM-Jay-ML.md)** — ML/data engineering (deadline: **Feb 16** ⚠️)
- **[FORM-Clarno-Compliance.md](FORM-Clarno-Compliance.md)** — Compliance/approval (deadline: Feb 20)

### Quick Reference (Optional Deep Dive)
- **[COST-ESTIMATION-SOURCES.md](COST-ESTIMATION-SOURCES.md)** — Where costs come from (TL;DR)
- **[USING-THE-COST-TOOL.md](USING-THE-COST-TOOL.md)** — How to run Python calculator
- **[INDEX.md](INDEX.md)** — Complete document index & navigation

### Detailed Reference (For Complete Understanding)
- **[aws-cost-estimation-methodology.md](aws-cost-estimation-methodology.md)** — Full methodology + tool mappings
- **[aws-comprehensive-utility-usage.md](aws-comprehensive-utility-usage.md)** — All 9 AWS service categories explained
- **[aws-cost-estimate-to-approval.md](aws-cost-estimate-to-approval.md)** — Workflow templates + deliverable guides
- **[aws-cost-estimate-data-collection.md](aws-cost-estimate-data-collection.md)** — Original full questionnaire (reference)

### Project Summary
- **[DELIVERY-SUMMARY.md](DELIVERY-SUMMARY.md)** — What was created + how it connects
- **[QUICK-START.md](QUICK-START.md)** — 3-minute stakeholder orientation

---

## Timeline at a Glance

| Date | Action | Who | Status |
|------|--------|-----|--------|
| **Feb 13** | Send personalized forms | Ben | 📤 Ready |
| **Feb 16, 5 PM** | Receive Max + Jay responses ⚠️ | Max, Jay | 📍 Blocking gates |
| **Feb 20, 5 PM** | Receive Cole + Nick + Dr. Clarno ⚠️ | Cole, Nick, Dr. Clarno | 📍 Hard deadline |
| **Feb 24** | Load responses → generate costs | Ben | 🔧 Mechanical |
| **Feb 25–26** | Draft deliverables | Ben | ✍️ Analysis |
| **Feb 27, 5 PM** | Submit to Dr. Clarno | Ben | 🎯 Final deadline |

---

## What Gets Asked (The 6 Critical Questions)

| # | Question | Who | Impact | Estimate If Missing |
|---|----------|-----|--------|---|
| 1 | Data egress/month? | Cole + Nick | Network costs (10x variation) | 100 GB/mo = $9/mo |
| 2 | PiXie Phase 1 yes/no? | Max | Architecture scope (binary) | No PiXie (baseline) |
| 3 | EKS hours/week? | Nick | Compute costs (4x variation) | 40 hrs/wk = $346/mo |
| 4 | Data retention policy? | Dr. Clarno | Storage costs (3x variation) | 2 years = $60/mo |
| 5 | Claude API calls/day? | Jay | External service costs (10x) | 10 calls/day = $48/mo |
| 6 | ITAR (GovCloud)? | Dr. Clarno | Regional costs (±30%) | Standard AWS |

---

## Three Blocking Decisions

**These MUST be answered by their deadlines:**

1. **Max (Feb 16):** PiXie Phase 1 → Yes or No? (blocks Redpanda sizing)
2. **Jay (Feb 16):** Claude API usage → light/moderate/heavy? (blocks external service budget)
3. **Dr. Clarno (Feb 20):** ITAR ruling → GovCloud or standard AWS? (blocks region selection)

Without these, we cannot finalize the estimate.

---

## Three Cost Scenarios

All traceable to AWS pricing pages:

| Scenario | PiXie | Hours/week | External | Monthly | 2026 (9mo) | Phase 1 Total |
|----------|-------|-----------|----------|---------|-----------|---------------|
| **Minimal** | No | 40 | No RAG | $612 | $5,508 | $12,852 |
| **Recommended** ⭐ | Yes | 40 | Moderate | $1,134 | $10,206 | $23,814 |
| **Full Cloud** | Yes | 168 | Heavy | $2,016 | $18,144 | $42,336 |

**Final recommendation likely:** Recommended ($1,134/mo), unless blocking gates shift assumptions.

---

## Document Organization

### In This Folder (phase1-cost-sizing/)
This is the master index. All cost sizing documents are organized here:
- Personalized forms (FORM-*.md)
- Simplified approach guide (SIMPLIFIED-COST-DRIVERS.md)
- Team distribution email (COST-ESTIMATION-SIMPLIFIED-COVER.md)
- Quick reference guides (COST-ESTIMATION-SOURCES.md, USING-THE-COST-TOOL.md, INDEX.md)
- Detailed methodology (aws-cost-estimation-methodology.md, aws-comprehensive-utility-usage.md)
- Workflow templates (aws-cost-estimate-to-approval.md)
- Project summary (DELIVERY-SUMMARY.md, QUICK-START.md)

### In Parent Folder (docs/analysis/)
- README-COST-ESTIMATE.md (master orientation, points to this folder)
- COST-SIZING-ORGANIZATION.md (navigation guide)
- cost_estimation_tool/ (Python calculator, sibling to analysis folder)

### Code
- **Python tool:** `../../cost_estimation_tool/` (8 modules, 1500+ lines, located in Neutron_OS root)

---

## How to Use This Folder

**If you're:**

### 👤 A Stakeholder (Cole, Nick, Max, Jay, Dr. Clarno)
1. Find your personalized form above
2. Complete it (3–6 minutes)
3. Email response to Ben by your deadline
4. Done!

### 📊 Ben (Coordinator)
1. **Feb 13:** Send `COST-ESTIMATION-SIMPLIFIED-COVER.md` to team with form links
2. **Feb 16:** Collect Max + Jay responses
3. **Feb 20:** Collect Cole + Nick + Dr. Clarno responses
4. **Feb 24:** Load all into `../../cost_estimation_tool/`
5. **Feb 25–26:** Generate final deliverables
6. **Feb 27:** Submit to Dr. Clarno

### 👨‍💼 Dr. Clarno (Reviewer)
1. Read: `COST-ESTIMATION-SIMPLIFIED-COVER.md` (overview)
2. Decide on three blocking gates (ITAR, PiXie, TACC)
3. Complete: `FORM-Clarno-Compliance.md` by Feb 20
4. Review final deliverables (Feb 27)
5. Approve budget

### 🔍 Future Auditor/Reviewer
1. Start with this README
2. Read: `DELIVERY-SUMMARY.md` (what was created)
3. Dive into: `aws-cost-estimation-methodology.md` (full methodology)
4. Reference: All formulas in `cost_calculator.py`

---

## Key Files by Purpose

### Distribution
- COST-ESTIMATION-SIMPLIFIED-COVER.md (email template + overview)
- SIMPLIFIED-COST-DRIVERS.md (methodology + blocking gates)

### Data Collection
- FORM-Cole-Physics.md (2 questions, deadline Feb 20)
- FORM-Nick-Operations.md (2 questions, deadline Feb 20)
- FORM-Max-PiXie.md (3 questions, deadline **Feb 16** ⚠️)
- FORM-Jay-ML.md (4 questions, deadline **Feb 16** ⚠️)
- FORM-Clarno-Compliance.md (5 questions, deadline Feb 20)

### Reference & Understanding
- QUICK-START.md (3-minute orientation for stakeholders)
- COST-ESTIMATION-SOURCES.md (where costs come from—TL;DR)
- USING-THE-COST-TOOL.md (how to run Python calculator)
- INDEX.md (complete navigation guide)

### Deep Dive (Optional)
- aws-cost-estimation-methodology.md (1000+ lines, complete methodology)
- aws-comprehensive-utility-usage.md (900 lines, all 9 services)
- aws-cost-estimate-to-approval.md (workflow + templates)
- DELIVERY-SUMMARY.md (what was created + inventory)

---

## Blocking Gates & Timeline

**These decisions block downstream work:**

### Gate 1: PiXie Phase 1 (Max, due Feb 16 EOD) ⚠️
- **Question:** Is PiXie hardware connected in 2026, yes or no?
- **Impact:** Determines Redpanda + streaming architecture
- **Cost variance:** $0 or +$200–300/mo
- **What depends on this:** Architecture scope, Redpanda sizing, storage tiers

### Gate 2: Claude API Usage (Jay, due Feb 16 EOD) ⚠️
- **Question:** How many Claude API calls/day in Phase 1?
- **Impact:** Determines external service budget
- **Cost variance:** $24–400+/mo (10x variation)
- **What depends on this:** RAG complexity, meeting intake frequency, shadowcasting approach

### Gate 3: ITAR Compliance (Dr. Clarno, due Feb 20 EOD) ⚠️
- **Question:** Do we need AWS GovCloud, or standard AWS?
- **Impact:** Determines region + compliance rules
- **Cost variance:** +30% if GovCloud required
- **What depends on this:** Vendor selection, data residency, security architecture

**Without these answers by Feb 20, we cannot finalize the estimate.**

---

## Success Criteria

- [ ] All 5 stakeholders respond to their forms by deadline
- [ ] 3 blocking gates resolved (PiXie, Claude, ITAR)
- [ ] Responses loaded into cost_estimation_tool
- [ ] 3 final deliverables generated (Executive Summary, Cost Tables, Justification)
- [ ] All costs traceable to AWS pricing pages
- [ ] Dr. Clarno approves budget by end of Feb
- [ ] AWS account creation begins ~Mar 1

---

## Questions?

Refer to the appropriate document:
- **"Why are we asking this?"** → SIMPLIFIED-COST-DRIVERS.md
- **"Where does this cost come from?"** → COST-ESTIMATION-SOURCES.md
- **"How do I fill out my form?"** → Your personalized FORM-*.md
- **"How does the Python tool work?"** → USING-THE-COST-TOOL.md
- **"What's the complete methodology?"** → aws-cost-estimation-methodology.md

---

## Status

✅ **Documents created:** 15+ files, ~5,500 lines  
✅ **Python tool ready:** 8 modules, all scenarios validated  
✅ **Timeline finalized:** Feb 13–27, 2026  
✅ **Blocking gates identified:** 3 critical decisions  
⏳ **Next:** Distribute forms Feb 13 morning

**All documents are in this folder (phase1-cost-sizing/)** — just pick the link above.

---

**Last Updated:** February 12, 2026  
**Coordinator:** Ben  
**Submission Deadline:** February 27, 2026, 5 PM
