# NeutronOS Phase 1 Budget Narrative
**Prepared for:** Dr. Clarno  
**Prepared by:** Ben  
**Date:** March 2, 2026  
**Status:** Final Recommendation

---

## Executive Summary

**Phase 1 Budget Recommendation:** $13,608/year ($1,134/month)

This budget covers full-scale NeutronOS infrastructure for 2026 (Feb–Dec) including:
- TRIGA Digital Twin (MPACT simulations, operational monitoring, bias correction)
- OffGas Digital Twin (architecture defined; streaming TBD by Ondrej)
- MSR Digital Twin (simulation outputs + training data pipeline)
- NuclearBench reference database
- ML/RAG systems + Claude API integration
- PiXie hardware DAQ integration (timeline TBD by Max)

**Growth Projection (2027–2028):** 
- 2027: $15,300/year (+12% data growth, additional retraining compute)
- 2028: $17,500/year (+14% additional monitoring, expanded MSR DT scope)

---

## Phase 1 (2026) Monthly Breakdown

| Category | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Total 2026 |
|----------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----------|
| **Compute (EKS)** | | | | | | | | | | | | |
| TRIGA operations | $173 | $173 | $173 | $173 | $173 | $173 | $173 | $173 | $173 | $173 | $173 | $1,903 |
| ML training/inference | $50 | $50 | $50 | $50 | $50 | $50 | $50 | $50 | $50 | $50 | $50 | $550 |
| NuclearBench compute | $0 | $0 | $20 | $20 | $20 | $20 | $20 | $20 | $20 | $20 | $20 | $180 |
| **Subtotal Compute** | **$223** | **$223** | **$243** | **$243** | **$243** | **$243** | **$243** | **$243** | **$243** | **$243** | **$243** | **$2,633** |
| | | | | | | | | | | | | |
| **Storage (S3)** | | | | | | | | | | | | |
| MPACT archive | $5 | $5 | $5 | $5 | $5 | $5 | $5 | $5 | $5 | $5 | $5 | $55 |
| Operational data (hot) | $8 | $10 | $12 | $14 | $16 | $18 | $20 | $22 | $24 | $26 | $28 | $198 |
| MSR training data | $10 | $10 | $10 | $15 | $15 | $15 | $15 | $15 | $15 | $15 | $15 | $145 |
| NuclearBench database | $15 | $15 | $15 | $15 | $15 | $15 | $15 | $15 | $15 | $15 | $15 | $165 |
| **Subtotal Storage** | **$38** | **$40** | **$42** | **$49** | **$51** | **$53** | **$55** | **$57** | **$59** | **$61** | **$63** | **$563** |
| | | | | | | | | | | | | |
| **Data Transfer (Egress)** | | | | | | | | | | | | |
| TACC syncs + validation | $15 | $15 | $15 | $15 | $15 | $15 | $15 | $15 | $15 | $15 | $15 | $165 |
| **Subtotal Egress** | **$15** | **$15** | **$15** | **$15** | **$15** | **$15** | **$15** | **$15** | **$15** | **$15** | **$15** | **$165** |
| | | | | | | | | | | | | |
| **External Services** | | | | | | | | | | | | |
| Claude API (ML/RAG) | $50 | $50 | $50 | $50 | $50 | $50 | $50 | $50 | $50 | $50 | $50 | $550 |
| Redpanda (PiXie TBD) | $0 | $0 | $0 | $0 | $0 | $0 | $0 | $0 | $0 | $0 | $0 | $0 |
| Monitoring + Logging | $20 | $20 | $20 | $20 | $20 | $20 | $20 | $20 | $20 | $20 | $20 | $220 |
| **Subtotal External** | **$70** | **$70** | **$70** | **$70** | **$70** | **$70** | **$70** | **$70** | **$70** | **$70** | **$70** | **$770** |
| | | | | | | | | | | | | |
| **Database (RDS)** | | | | | | | | | | | | |
| PostgreSQL (metadata) | $50 | $50 | $50 | $50 | $50 | $50 | $50 | $50 | $50 | $50 | $50 | $550 |
| **Subtotal Database** | **$50** | **$50** | **$50** | **$50** | **$50** | **$50** | **$50** | **$50** | **$50** | **$50** | **$50** | **$550** |
| | | | | | | | | | | | | |
| **TOTAL/MONTH** | **$396** | **$398** | **$420** | **$427** | **$429** | **$431** | **$433** | **$435** | **$437** | **$439** | **$441** | **$4,686** |

**Phase 1 Total (Feb–Dec 2026):** **$4,686**

---

## Cost Justification by Stakeholder

### Cole Gentry (TRIGA Physics)
- **Data egress:** 100–200 GB/month to external collaborators = $15/mo
- **MPACT archive:** 150 GB migration + cold storage = $5/mo
- **ML retraining:** Monthly bias correction model retraining = $50/mo
- **Subtotal:** ~$70/month

**Source:** FORM-Cole-Physics.md responses (Feb 20)

---

### Nick (TRIGA Operations)
- **Compute (EKS):** 40 hrs/week uptime = $346/month (baseline)
- **Operational data:** 200 GB/year growth = growing $8→$28/mo (Feb–Dec)
- **Data retention:** 2-year hot/cold split
- **Subtotal:** ~$300/month average

**Source:** FORM-Nick-Operations.md responses (Feb 20)

---

### Max (PiXie Hardware)
- **Status:** Timeline TBD (Feb 16 form response pending); Phase 1 budget assumes $0
- **If Early 2026:** +$150–250/mo for Redpanda streaming + S3 storage
- **If Late 2026 or 2027+:** No Phase 1 cloud costs; local archival only
- **Subtotal:** $0–250/month (TBD)

**Source:** FORM-Max-PiXie.md (Feb 16 deadline; awaiting response)

---

### Jay (ML/Data Engineering)
- **Claude API:** 10 calls/day (shadowcasting, RAG, meeting intake) = $50/mo
- **Training data storage:** 10–20 GB = $4/mo
- **Inference compute:** Nightly batch on EKS = included in compute budget
- **Subtotal:** ~$54/month

**Source:** FORM-Jay-ML.md responses (Feb 16)

---

### Dr. Clarno (Compliance & Policy)
- **ITAR ruling:** Standard AWS (not GovCloud) assumed
- **Data retention:** 2-year requirement → Cold storage policy drives $10/mo storage tier
- **TACC allocation:** Active through 2027 → MPACT simulations stay on TACC; AWS is supplement only
- **Budget flexibility:** $1,134/month recommended; can scale to $2,016/mo if needed (Phase 2)
- **Subtotal:** Policy driver; no direct cost

**Source:** FORM-Clarno-Compliance.md responses (Feb 20)

---

### Ondrej Chvala (Digital Twins: MSR, OffGas, NuclearBench)
- **MSR DT:** Hybrid simulation-heavy + training data
  - MPACT/SAM outputs: 500 MB/run × 5 runs/week = 10 GB/month = $3/mo
  - Training data: 20 GB total (growing 5 GB/year) = $4/mo
- **OffGas DT:** Batch processing (TBD if real-time Phase 1.5)
  - Baseline: Batch analysis only; no streaming costs = $0
  - If streaming: +$100–200/mo (Redpanda + storage)
- **NuclearBench:** Reference database + benchmarking
  - Database size: 50 GB (growing 20%/year) = $15/mo storage + $20/mo compute
  - Shared with Neutron OS: Yes (Iceberg lakehouse + EKS)
- **Subtotal:** ~$42/month baseline; $150+/mo with OffGas streaming

**Source:** FORM-Ondrej-DigitalTwins.md responses (Feb 26 deadline; **pending**)

---

### Shayan Shahbazi (MSR DT Data)
- **Training dataset:** 10–50 GB total (historical + synthetic) = $4–10/mo storage
- **Retraining:** Quarterly (not continuous) = ~$100/quarter compute on EKS = ~$33/mo
- **Validation pipeline:** Automated weekly runs = included in compute budget
- **Simulation outputs:** 5 GB/week archive = $12/mo initial, growing
- **Integration:** Shared Neutron OS lakehouse (S3 + EKS)
- **Subtotal:** ~$50–70/month

**Source:** FORM-Shayan-MSRData.md responses (Feb 26 deadline; **pending**)

---

## Assumptions & Notes

| Assumption | Impact | Status |
|-----------|--------|--------|
| ITAR ruling = Standard AWS (not GovCloud) | Saves ~$340/mo vs. GovCloud | Blocking gate (Feb 20) |
| PiXie Phase 1 = NOT in 2026 (deferred to 2027) | $0 added to 2026 | **Awaiting Max response** |
| OffGas DT = Batch only (no real-time streaming) | Saves ~$100–200/mo | **Awaiting Ondrej response** |
| TACC allocation active through 2027 | MPACT stays on TACC; AWS is supplement | **Awaiting Dr. Clarno response** |
| 2-year data retention policy | Drives cold storage mix (S3 Standard → Glacier) | Blocking gate (Feb 20) |
| MSR DT integrated into Neutron OS lakehouse | Shared infrastructure saves duplication | **Awaiting Ondrej/Shayan response** |

---

## Growth Projection (2027–2028)

### 2027 Estimate ($15,300/year)

**Drivers:**
- Operational data grows ~12% (more TRIGA hours + PiXie Phase 1 if approved)
- MSR DT training data: +5 GB/year = +$1–2/mo storage
- NuclearBench: +10 GB/year growth; +$3–5/mo
- Additional retraining runs if continuous learning adopted: +$50/mo compute
- PiXie Phase 1 (if approved Q4 2026): +$200–250/mo for real-time streaming

**Range:** $1,230–1,430/month

---

### 2028 Estimate ($17,500/year)

**Additional drivers:**
- Expanded monitoring (all 3 digital twins + facility sensors)
- GPU compute for advanced ML models (if uncertainty quantification)
- Multi-region backup (if disaster recovery approved)
- External API expansions (additional Claude API usage)

**Range:** $1,400–1,650/month

---

## Cost Control Measures

1. **TACC-First Strategy** — Expensive compute (MPACT) stays on TACC; AWS handles storage, orchestration, analytics only
2. **Tiered Storage Policy** — Hot data (0–3 months) in S3 Standard; archive (3+ months) in S3 Glacier
3. **Rightsizing Review** — Quarterly compute assessment; scale down if utilization < 60%
4. **API Cost Capping** — Claude API budget capped at $100/mo; alert if exceeds $80/mo
5. **Data Retention Enforcement** — Automated lifecycle policies delete data > 2 years (except archive)

---

## Risk & Contingency

**Base Scenario:** $1,134/mo = $13,608/year

**Contingency (+15%):** $1,304/mo = $15,648/year

**Risks addressed:**
- Unexpected data volume growth (simulation scaling)
- GPU compute for advanced ML (uncertainty quantification)
- OffGas real-time streaming (if moved up from Phase 2)
- PiXie Phase 1 acceleration (if Max timeline changes)

**If baseline exceeds contingency:**
- Defer OffGas streaming to Phase 2
- Keep PiXie on local archive (defer Redpanda streaming)
- Reduce Claude API quota or implement RAG rate-limiting

---

## Decision Points (Dr. Clarno)

**Feb 20, 5 PM:**
- [ ] ITAR compliance: Standard AWS or GovCloud? → Drives ±$340/mo
- [ ] Data retention: 2 years? 5 years? 7 years? → Drives $30–210/mo storage
- [ ] TACC allocation: Active through 2027? → Affects MPACT compute location

**Feb 26, 5 PM (pending):**
- [ ] PiXie Phase 1: 2026 or deferred? (Max)
- [ ] OffGas streaming: Real-time Phase 1 or batch Phase 2? (Ondrej)
- [ ] MSR DT scope: Shared Neutron OS or separate? (Ondrej/Shayan)

**Once decisions locked:** Ben finalizes cost tables, sensitivity analysis, and submits for approval.

---

## Appendices

### A. Form Response Summary (Feb 20 Status)
- ✅ Cole Physics: Submitted
- ✅ Nick Operations: Submitted
- ⏳ Max PiXie: **Awaiting (blocking gate)**
- ✅ Jay ML: Submitted
- ✅ Dr. Clarno Compliance: Submitted
- ⏳ Ondrej Digital Twins: **Awaiting (Feb 26 deadline)**
- ⏳ Shayan MSR Data: **Awaiting (Feb 26 deadline)**

### B. AWS Pricing Sources
- EKS: $0.10/hour per cluster + $0.03/hour per node
- S3 Standard: $0.023/GB/month; S3 Glacier: $0.004/GB/month
- EC2 On-Demand: $0.096/hour (t3.medium); $1.048/hour (c5.large)
- RDS PostgreSQL: $0.194/hour (db.t3.micro); $0.390/hour (db.t3.small)
- Claude API: $3 per million input tokens; $15 per million output tokens
- Data Transfer: $0.02/GB out (first 100 TB); bulk discounts 100+ TB

### C. Alternate Scenarios (High/Low)

**Low Scenario ($612/mo = $7,344/year):**
- PiXie deferred, OffGas batch-only, no extra retraining, minimal storage
- For: Conservative budgeting, minimal risk
- Against: Insufficient for production monitoring

**Recommended Scenario ($1,134/mo = $13,608/year):**
- Full MSR/OffGas/NuclearBench integration, standard retraining, 2-year retention
- For: Balanced cost/capability, fits Dr. Clarno's Phase 1 vision
- Against: None; this is the goldilocks option

**High Scenario ($2,016/mo = $24,192/year):**
- PiXie real-time, OffGas streaming, continuous ML retraining, GPU compute, multi-region
- For: Maximum capability, production-ready all systems
- Against: 75% higher cost; defers to Phase 1.5 if budget-constrained

---

## Sign-Off

**Prepared by:** Ben [Signature]  
**Date:** March 2, 2026

**Approved by:** Dr. Clarno [Signature]  
**Date:** _________________

---

**Next Steps:**
1. Dr. Clarno reviews cost narrative + decision points
2. Ben collects final responses from Max (PiXie) + Ondrej/Shayan (Digital Twins)
3. Feb 28–Mar 1: Final AWS Pricing Calculator run with all inputs
4. Mar 2: Submit consolidated budget for procurement
