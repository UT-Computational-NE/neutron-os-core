# AWS Cost Estimate: Complete Package README

**Purpose:** Budget approval submission to Dr. Clarno by Feb 27, 2026  
**Status:** Simplified approach ready; all docs organized in subfolder  
**Owner:** Ben  
**Stakeholders:** Cole (physics), Nick (ops), Max (hardware), Jay (ML), Dr. Clarno (approval)  
**Timeline:** Feb 13–27, 2026 (extended for quality responses + 80/20 simplified approach)  
**📁 All Cost Sizing Documents:** [→ phase1-cost-sizing/README.md](phase1-cost-sizing/README.md)

**📋 Document Hierarchy (in this folder):**
1. **This README** ← Start here for orientation
2. **COST-ESTIMATION-SIMPLIFIED-COVER.md** ← TL;DR for Feb 13 email to team
3. **SIMPLIFIED-COST-DRIVERS.md** ← Explains 6-critical-question approach
4. **Individual Forms:**
   - FORM-Cole-Physics.md
   - FORM-Nick-Operations.md
   - FORM-Max-PiXie.md
   - FORM-Jay-ML.md
   - FORM-Clarno-Compliance.md
5. **Deep Reference:**
   - aws-cost-estimation-methodology.md ← Sources & tool integration
   - aws-cost-estimate-data-collection.md ← Original full questionnaire (optional)
   - aws-comprehensive-utility-usage.md ← Detailed service breakdown
6. **cost_estimation_tool/** ← Python calculator (run Feb 24 after data collection)

**📊 Also in workspace:**
- `Neutron_OS/cost_estimation_tool/` — Python library for automated cost calculations

---

## What You're Building

A **simplified AWS infrastructure cost estimate** for NeutronOS Phase 1 (TRIGA only, 2026-2027) using a **6-critical-question approach**:

1. **Data egress patterns** — drives network costs 10x variation
2. **PiXie Phase 1 yes/no** — binary decision, blocks architecture
3. **EKS operating hours/week** — drives compute costs 4x variation
4. **Data retention policy** — drives storage costs 3x variation
5. **Claude API query volume** — drives external service costs 10x variation
6. **ITAR compliance (GovCloud?)** — drives regional costs +30% if yes

Everything else is estimated intelligently. **Three scenarios:** Minimal ($612/mo), Recommended ($1,134/mo), Full Cloud ($2,016/mo).

**Key insight:** Don't ask what we can estimate. Ask only what changes the answer.

**Timeline:** Feb 13 → 27 (extended from Feb 18 for quality + 2-week response window)

---

## Complete Document Hierarchy (Updated)

```
AWS Cost Estimation Package (Feb 13–27, 2026)
│
├── DISTRIBUTION (Feb 13)
│   ├─ THIS FILE: README-COST-ESTIMATE.md
│   ├─ COST-ESTIMATION-SIMPLIFIED-COVER.md ← Email to team
│   └─ SIMPLIFIED-COST-DRIVERS.md ← Methodology
│
├── PERSONALIZED FORMS (Feb 13–20)
│   ├─ FORM-Cole-Physics.md (deadline Feb 20)
│   ├─ FORM-Nick-Operations.md (deadline Feb 20)
│   ├─ FORM-Max-PiXie.md (deadline Feb 16 ⚠️ blocking)
│   ├─ FORM-Jay-ML.md (deadline Feb 16 ⚠️ blocking)
│   └─ FORM-Clarno-Compliance.md (deadline Feb 20 ⚠️ blocking)
│
├── TIER 1: For Quick Reference
│   ├─ COST-ESTIMATION-SOURCES.md
│   │  └─ TL;DR: Where all the numbers come from
│   ├─ USING-THE-COST-TOOL.md
│   │  └─ How to run Python calculator (Feb 24 use)
│   └─ INDEX.md
│      └─ Complete navigation guide
│
├── TIER 2: For Detail & Rigor
│   ├─ aws-cost-estimation-methodology.md
│   │  └─ Deep dive: tool integration, assumptions, citations
│   ├─ aws-comprehensive-utility-usage.md
│   │  └─ All 9 AWS service categories + external services
│   └─ aws-cost-estimate-data-collection.md (original full questionnaire)
│      └─ Stakeholder questionnaire (Sections A–E) - for reference
│
├── TIER 3: For Workflow & Approval
│   └─ aws-cost-estimate-to-approval.md
│      └─ Timeline, templates, delivery checklist
│
└── TIER 4: Code (Python)
    └─ ../cost_estimation_tool/
       ├─ data_models.py (cost data structures)
       ├─ cost_calculator.py (implements formulas)
       ├─ scenarios.py (pre-defined scenarios)
       ├─ reporter.py (markdown/JSON/CSV output)
       ├─ main.py (CLI interface)
       ├─ test_scenarios.py (validation tests)
       └─ README.md (tool documentation)
```

---

## NEW: Simplified Approach (Feb 13, 2026)

Instead of a long 50+ question worksheet, we're using a **6-critical-question approach**:

### Distribution (Feb 13)
**File:** `COST-ESTIMATION-SIMPLIFIED-COVER.md`  
**Purpose:** Team email with overview + form links  
**Status:** ✅ Ready to send

### Methodology Guide
**File:** `SIMPLIFIED-COST-DRIVERS.md`  
**Purpose:** Explains the 80/20 approach + blocking gates  
**Status:** ✅ Ready to reference  
**Key insight:** 6 questions drive 80% of cost variation. Fill rest with intelligent estimates.

### Personalized Questionnaires (3-6 min each)
**Files:** `FORM-Cole-Physics.md`, `FORM-Nick-Operations.md`, `FORM-Max-PiXie.md`, `FORM-Jay-ML.md`, `FORM-Clarno-Compliance.md`  
**Purpose:** Focused questions only for what each person knows/controls  
**Status:** ✅ Ready to distribute  

**Timeline:**
- **Feb 13:** Send personalized forms to each stakeholder
- **Feb 16, 5 PM:** Hard deadline for Max (PiXie) + Jay (Claude usage) — blocking gates
- **Feb 20, 5 PM:** Hard deadline for Cole, Nick, Dr. Clarno
- **Feb 24:** Load responses into cost_estimation_tool
- **Feb 25–26:** Generate final estimates + sensitivity
- **Feb 27:** Submit to Dr. Clarno

### Original Full Questionnaire (Available for Reference)
**File:** `aws-cost-estimate-data-collection.md`  
**Purpose:** Complete detailed questionnaire (optional for deeper context)  
**Status:** Available but not the primary distribution  
**Use case:** If someone wants to provide more detail than their personalized form requires

---

### 1.5. Cost Estimation Methodology (NEW)
**File:** `aws-cost-estimation-methodology.md` (this folder)  
**Purpose:** Explain data collection questions → AWS pricing tools → cost calculations  
**Status:** ✅ Ready to reference

**Sections:**
- **Standard Tools & Frameworks** — AWS Pricing Calculator, Cost Explorer, Terraform, CloudFormation
- **Questions Designed for Tools** — How each data collection question maps to AWS calculator inputs
- **Tool Assumptions Table** — Formula + assumption + source for each cost component
- **Citation & Sourcing Standards** — How to cite AWS pricing in final docs
- **Pricing Currency & Update Schedule** — When estimates become invalid
- **Tool Integration Workflow** — Monthly review loop, quarterly pricing checks
- **Traceability Matrix** — Questions → Tools → Costs (complete audit trail)
- **Validation Spot-Checks** — How to verify estimates against real AWS data
- **Known Limitations & Risk Factors** — What can go wrong

**Key reference:**
```
Section 2.1: Questions → Tool Inputs
Maps each stakeholder question to AWS Pricing Calculator entry
(e.g., "Operating hours/week" → EKS node auto-scaling)

Section 2.2: Tool Assumptions Table
Every cost formula has citation to AWS pricing page + assumption documented
```

**How to use:**
1. Stakeholders can read Section 2.1 to understand "why we're asking this question"
2. During Feb 17–18 population phase, reference Section 2.2 for cost formulas
3. When writing final deliverables, use Section 3 (Citation Standards) for citations
4. Include this doc as technical appendix to budget submission

---

### 2. Workflow & Deliverables Guide
**File:** `aws-cost-estimate-to-approval.md` (this folder)  
**Purpose:** Show path from data collection → budget approval  
**Status:** ✅ Ready to reference

**Sections:**
- **Workflow Overview** — Feb 12-18 timeline with checkpoints
- **Deliverable 1: Executive Summary** — 1-page request, 3 scenarios, approval gates
- **Deliverable 2: Detailed Cost Tables** — Monthly breakdown, one-time costs, sensitivity analysis
- **Deliverable 3: Technical Justification** — Why each service, references to PRDs/ADRs
- **Distribution Template** — Email to send to stakeholders
- **Success Criteria** — Approval readiness checklist

**How to use:**
1. Reference workflow timeline during data collection week
2. Use Executive Summary template to draft final doc (Feb 17)
3. Populate cost tables with collected data (Feb 16-17)
4. Write justification using PRD/ADR references provided (Feb 17-18)
5. Submit all three to Dr. Clarno by Feb 18

---

### 3. This README
**File:** `README-COST-ESTIMATE.md` (this folder)  
**Purpose:** Orientation guide for entire cost estimation effort  
**Status:** ✅ You're reading it

---

## Documents to Create (Feb 16-18)

After collecting data, you will create three final deliverables:

### Final Deliverable 1: Executive Summary
**File:** `aws-cost-estimate-executive-summary.md` (to create)  
**Purpose:** 1-page approval request to Dr. Clarno  
**Who needs it:** Dr. Clarno (decision-maker)  
**Timeline:** Draft Feb 17, finalize Feb 18  
**Template:** See `aws-cost-estimate-to-approval.md` Section "Deliverable 1"

**Contents:**
- Opening: "Request approval for $X/month AWS infrastructure"
- Three scenarios (A/B/C) with monthly & annual costs
- Three critical approval gates (ITAR, PiXie, TACC)
- Recommended action + budget line item
- Link to detailed analysis below

---

### Final Deliverable 2: Detailed Cost Tables
**File:** `aws-cost-estimate-tables.md` (to create)  
**Purpose:** 5-page spreadsheet + analysis for budget justification  
**Who needs it:** Finance, Dr. Clarno, internal planning  
**Timeline:** Draft Feb 16-17, finalize Feb 18  
**Template:** See `aws-cost-estimate-to-approval.md` Section "Deliverable 2"

**Contents:**
- Table 1: Monthly recurring costs (Jan 2026–Dec 2027)
- Table 2: One-time costs (Spring 2026)
- Table 3: Annual forecast (2026 & 2027)
- Table 4: Sensitivity analysis (what drives cost up/down?)
- Table 5: Architecture comparison (AWS vs. TACC vs. hybrid)

**Data feeds:** From Sections A-E of data collection worksheet

---

### Final Deliverable 3: Technical Justification
**File:** `aws-cost-estimate-justification.md` (to create)  
**Purpose:** 10-page detailed analysis with PRD/ADR references  
**Who needs it:** Technical reviewers, future reference  
**Timeline:** Draft Feb 17-18, finalize Feb 18  
**Template:** See `aws-cost-estimate-to-approval.md` Section "Deliverable 3"

**Contents:**
- Section 1: Architecture overview (why NeutronOS on AWS?)
- Section 2: Cost driver justification (why each service?)
- Section 3: Cost of staying TACC-only (what we gain)
- Section 4: ITAR & compliance considerations
- Section 5: Risk analysis & contingencies
- Section 6: References to NeutronOS docs (specs, PRDs, ADRs)
- Section 7: Approval checklist for Dr. Clarno

**Data feeds:** From Sections A-E + technical context

---

## Document Hierarchy

```
README-COST-ESTIMATE.md (orientation)
│
├─ aws-cost-estimate-data-collection.md (input)
│  ├─ Section A: Cole's questions
│  ├─ Section B: Nick's questions
│  ├─ Section C: Max's questions
│  ├─ Section D: Jay's questions
│  ├─ Section E: Dr. Clarno's questions
│  ├─ Section F: Cost calculation framework
│  └─ Section I: Recording responses
│
├─ aws-cost-estimate-to-approval.md (process guide)
│  ├─ Workflow timeline (Feb 12-18)
│  ├─ Deliverable 1 template (executive summary)
│  ├─ Deliverable 2 template (cost tables)
│  ├─ Deliverable 3 template (justification)
│  └─ Distribution & collection guidance
│
├─ aws-cost-estimate-executive-summary.md ← CREATE Feb 17-18
├─ aws-cost-estimate-tables.md ← CREATE Feb 17-18
└─ aws-cost-estimate-justification.md ← CREATE Feb 17-18
```

---

## Updated Timeline & Milestones (Feb 13–27)

### FEB 13 (FRI) — DISTRIBUTION
- [x] Created simplified approach docs
- [x] Created 5 personalized forms
- [ ] **ACTION:** Send `COST-ESTIMATION-SIMPLIFIED-COVER.md` to all stakeholders
- [ ] **ACTION:** Include personalized form links
- [ ] **ACTION:** Note blocking gate deadlines (Feb 16 vs. Feb 20)

### FEB 14-15 (WKD) — EARLY RESPONSES
- [ ] Monitor Max + Jay responses (blocking gates due Feb 16)
- [ ] Send reminders if needed
- [ ] Clarify ambiguous answers

### FEB 16 (MON) ⚠️ FIRST HARD DEADLINE
- [ ] **DEADLINE EOD:** Collect responses from Max (PiXie) + Jay (ML)
- [ ] **ACTION:** Review blocking gate answers
- [ ] **ACTION:** Flag any "TBD" items requiring escalation
- [ ] **ACTION:** Confirm architecture scope based on PiXie + ITAR decisions

### FEB 17-19 (TUE-THU) — FINAL RESPONSES
- [ ] Monitor Cole + Nick + Dr. Clarno responses
- [ ] Send reminders to non-respondents
- [ ] Clarify ambiguous answers via email/chat

### FEB 20 (FRI) ⚠️ SECOND HARD DEADLINE
- [ ] **DEADLINE EOD:** Collect all remaining responses (Cole, Nick, Dr. Clarno)
- [ ] **ACTION:** Consolidate all responses (6 questions × 5 people = complete data)
- [ ] **ACTION:** Identify any remaining "TBD" or "depends on decision" items
- [ ] **ACTION:** Flag assumptions clearly

### FEB 24 (TUE) — COST CALCULATION
- [ ] **ACTION:** Load responses into cost_estimation_tool (Python)
- [ ] **ACTION:** Run cost scenarios: Minimal, Recommended, Full Cloud
- [ ] **ACTION:** Generate markdown/JSON/CSV outputs
- [ ] **ACTION:** Cross-validate against manual calculations

### FEB 25-26 (WED-THU) — DELIVERABLES DRAFT
- [ ] Draft Executive Summary (1 page)
- [ ] Draft Detailed Cost Tables (5 pages)
- [ ] Draft Technical Justification (10 pages)
- [ ] Cross-check numbers across all three (should match)
- [ ] Send DRAFT to Cole/Nick for sanity check (optional)

### FEB 27 (FRI) — SUBMISSION DEADLINE ✅
- [ ] Incorporate any feedback from reviewers
- [ ] Final review of all three documents
- [ ] **ACTION:** Email to Dr. Clarno
  - Subject: "NeutronOS Phase 1 AWS Cost Estimate – Budget Approval Request"
  - Attach: Executive summary (main), cost tables (detail), justification (reference), methodology (appendix)
- [ ] **ACTION:** Request meeting with Dr. Clarno to discuss (especially blocking gates)

### FEB 28+ (WEEK OF) — APPROVAL & PROCUREMENT
- [ ] Dr. Clarno reviews, asks clarifying questions
- [ ] Resolve any open items
- [ ] Obtain signature/approval
- [ ] **ACTION:** Begin AWS account creation & procurement

---

## Three Blocking Decision Gates (Critical Path)

These must be resolved by **Feb 16 for Max/Jay, Feb 20 for Dr. Clarno**:

### Gate 1: PiXie Phase 1 Inclusion ⚠️ (Max — Due Feb 16)
**Question:** Is PiXie hardware connected to cluster in 2026, yes or no?  
**Cost impact:** Yes = +$200–300/mo (Redpanda + storage); No = baseline only  
**Owner:** Max  
**Action:** Answer by Feb 16; blocks architecture decisions  
**Impact:** Affects Redpanda sizing, storage tiers, network egress budget

### Gate 2: ITAR Compliance Ruling ⚠️ (Dr. Clarno — Due Feb 20)
**Question:** Can we use standard AWS, or must we use AWS GovCloud?  
**Cost impact:** Standard AWS = $1,134/mo; GovCloud = $1,474/mo (+30%)  
**Owner:** Dr. Clarno (likely escalates to export control office)  
**Action:** Get legal/compliance ruling by Feb 20; build into final estimates  
**Impact:** Affects region selection, vendor negotiations, entire cost model

### Gate 3: TACC Allocation Status ⚠️ (Dr. Clarno — Due Feb 20)
**Question:** Is TACC HPC allocation active through 2027 or expiring 2026?  
**Cost impact:** Active = MPACT stays on TACC (implicit cost); Expiring = shift to AWS GPU nodes (+$200–300/mo)  
**Owner:** Dr. Clarno  
**Action:** Get confirmation by Feb 20; plan contingency if expiring  
**Impact:** Affects MPACT compute strategy, HPC allocation planning

### Non-Blockers (OK if TBD)
- [ ] Exact data egress (can estimate 100 GB/mo)
- [ ] Exact MPACT archive size (can estimate 100 GB)
- [ ] Exact number of RAG documents (can estimate 1,000)
- [ ] Exact Claude API usage (can estimate 10 calls/day)

---

## Cost Estimate Baseline

**Based on current best estimates (subject to data collection):**

| Metric | Estimate | Data Source |
|--------|----------|-------------|
| Daily data volume | 400 MB/day | Jay (150GB/yr = 410MB/day) |
| MPACT runs/day | 20 | Cole (TBD, ~20 states/day) |
| Production batches/week | 1 | Nick (typical Monday) |
| Isotope types | 3–5 | Nick (TBD) |
| Documents for RAG | ~1,000 | Jay estimate |
| PiXie Phase 1? | TBD | Max decision |
| **Monthly AWS Cost (Scenario B)** | **$700–900** | Framework calc |
| **Annual AWS Cost (2026)** | **$6.3–8.1K** | ×9 months |
| **Annual AWS Cost (2027)** | **$8.4–10.8K** | ×12 months |

---

## Answers You're Waiting For

### From Cole (MPACT & Physics) — Expected by Feb 16
- A1a: States per nightly run? (affects # of MPACT outputs)
- A1b: Wall-clock time per MPACT? (affects HPC allocation utilization)
- A2c: Total MPACT archive size on TACC? (affects migration cost)
- A4a: How do you compute confidence intervals? (affects model training complexity)

### From Nick (Operations & Production) — Expected by Feb 16
- B1a: Operating hours/week? (affects data volume)
- B2a-e: Isotope types & modeling approach? (affects training data complexity)
- B3a-d: Prediction validation frequency? (affects database size)
- B4a-c: Breakdown of 150GB/year baseline? (validates storage estimate)

### From Max (PiXie Hardware) — Expected by Feb 15 ⚠️ BLOCKING
- C1a-d: PiXie current status & configuration? (Phase 1 inclusion decision)
- C2a-c: Current daily data volume? (affects streaming cost)
- C3a: Is PiXie in Phase 1 or Phase 2? (CRITICAL DECISION GATE)

### From Jay (ML/Data Engineering) — Expected by Feb 16
- D1a-e: RAG corpus size, embedding strategy? (affects API costs)
- D2a-e: Model training data & frequency? (affects GPU compute)
- D3a-d: Shadowcasting approach? (affects database size)

### From Dr. Clarno (Approval Gates) — Expected by Feb 15 ⚠️ BLOCKING
- E1a: ITAR classification ruling? (standard AWS vs. GovCloud, +30% cost impact)
- E1d: TACC allocation status through 2027? (affects HPC compute planning)

---

## How This Feeds Your Budget Approval

Once you have data:

```
Data Collection Worksheet (with responses)
       ↓
Cost Calculation Framework (Section F)
       ↓
Executive Summary ($700–900/mo baseline)
       ↓
Detailed Cost Tables (monthly breakdown)
       ↓
Technical Justification (why each service)
       ↓
Dr. Clarno Approval ← Subject to ITAR & PiXie gates
       ↓
AWS Account Creation & Procurement (Feb 21)
       ↓
Phase 1 Deployment (~Apr 1, 2026)
```

---

## Next Actions (This Week)

**By EOD FEB 12:**
1. [ ] Review these three documents for accuracy/clarity
2. [ ] Customize questions if you want different wording
3. [ ] Identify any questions you think will be hard to answer
4. [ ] Prepare email to stakeholders

**By FEB 13 9 AM:**
1. [ ] Send data collection worksheet to Cole, Nick, Max, Jay, Dr. Clarno
2. [ ] Include this note:
   ```
   Your responses are critical for finalizing the AWS cost estimate 
   for Dr. Clarno's budget approval by Feb 18.
   
   Deadline: EOD Feb 16 (firm deadline for Feb 18 submission)
   
   If you're uncertain about a question, it's OK to answer:
   - "I'll measure" (then provide by Feb 16)
   - "TBD pending decision" (we'll note as assumption)
   - "Not applicable" (skip it)
   
   Time estimate: 30–60 min per section
   ```
3. [ ] Schedule 15-min calls with Max (PiXie decision) & Dr. Clarno (ITAR/TACC)

**By FEB 16 EOD:**
1. [ ] Collect all responses
2. [ ] Consolidate in Section I of worksheet
3. [ ] Run cost calculations

**By FEB 17 EOD:**
1. [ ] Draft all three deliverables
2. [ ] Send to Cole/Nick for sanity check

**By FEB 18 EOD:**
1. [ ] Submit to Dr. Clarno

---

## References & Supporting Documentation

### NeutronOS Core Docs
- [Executive PRD](../prd/neutron-os-executive-prd.md) — Product vision & roadmap
- [Master Tech Spec](../specs/neutron-os-master-tech-spec.md) — Architecture decisions
- [Data Architecture Spec](../specs/data-architecture-spec.md) — Lakehouse design, retention policy

### Architecture Decision Records
- [ADR-003: Iceberg Lakehouse](../adr/003-lakehouse-iceberg-duckdb.md)
- [ADR-006: MCP Agents](../adr/006-mcp-server-agentic-access.md)
- [ADR-007: Streaming-First](../adr/007-streaming-first-architecture.md)
- [ADR-008: WASM Surrogates](../adr/008-wasm-extension-runtime.md)

### Product Requirements
- [Medical Isotope PRD](../prd/medical-isotope-prd.md)
- [Data Platform PRD](../prd/data-platform-prd.md)
- [Analytics Dashboards PRD](../prd/analytics-dashboards-prd.md)

### Incident Analysis (Drives Requirements)
- [Sm-153 Incident Analysis](../Neutron_OS/docs/analysis/Sm153_Incident_Analysis_PRD_Implications.md)

---

## Contact & Questions

**Cost Estimate Coordinator:** Ben  
**Technical Lead:** Cole (physics), Nick (ops)  
**Hardware Lead:** Max (PiXie)  
**Data/ML Lead:** Jay  
**Approval Authority:** Dr. Clarno

If you have questions about the cost estimate structure or process, ask Ben.  
If you have specific technical questions about your section, respond in the worksheet with "Question:" and Ben will clarify.

---

**Last Updated:** Feb 12, 2026  
**Next Review:** Feb 16 (after data collection)

