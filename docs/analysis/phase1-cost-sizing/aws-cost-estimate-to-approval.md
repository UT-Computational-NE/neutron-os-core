# From Data Collection to Budget Approval

**Document Purpose:** Shows workflow from data collection → budget approval package for Dr. Clarno  
**Timeline:** Feb 13–27, 2026 (simplified 6-question approach)  
**Responsible:** Ben (coordinator), Cole (physics), Nick (ops), Max (hardware), Jay (ML), Dr. Clarno (approval)

---

## Workflow Overview

```
FEB 13 (DISTRIBUTION)
  └─ Send personalized forms to stakeholders
     (Cole, Nick, Max, Jay, Dr. Clarno)

FEB 16, 5 PM (BLOCKING GATES)
  └─ Collect responses from Max (PiXie) + Jay (Claude)
  └─ Review critical decisions

FEB 20, 5 PM (HARD DEADLINE)
  └─ Collect responses from Cole, Nick, Dr. Clarno
  └─ Consolidate all responses

FEB 24 (COST CALCULATION)
  └─ Load responses into cost_estimation_tool
  └─ Generate cost scenarios

FEB 25-26 (DELIVERABLES DRAFT)
  └─ Draft three documents:
     1. Executive Summary (1 page)
     2. Detailed Cost Tables (5 pages)
     3. Technical Justification (10 pages)

FEB 27, 5 PM (FINAL DEADLINE)
  └─ Submit budget approval package to Dr. Clarno
```

---

## Three Deliverable Documents

### Deliverable 1: Executive Summary (1 page)

**File:** `aws-cost-estimate-executive-summary.md`

**Content (template):**
```
# AWS Cost Estimate: Executive Summary

## Request
Approve AWS infrastructure budget for NeutronOS Phase 1 (UT TRIGA only, 2026-2027).
Total: $420–1,440/month depending on PiXie scope (to be confirmed with Max).

## Three Scenarios

### Scenario A: Minimal (PiXie excluded, defer to Phase 2)
- Monthly: $350–450
- Annual (2026): $3,150–4,050
- Annual (2027): $4,200–5,400
- Best for: Conservative approach, validate data pipeline first

### Scenario B: Recommended (PiXie included, medium integration)
- Monthly: $700–900
- Annual (2026): $6,300–8,100
- Annual (2027): $8,400–10,800
- Best for: Complete digital twin stack, operational visibility

### Scenario C: Full Cloud (AWS primary, move compute off TACC)
- Monthly: $1,200–1,800
- Annual (2026): $10,800–16,200
- Annual (2027): $14,400–21,600
- Best for: Future multi-facility scaling, independence from TACC

## Critical Approval Gates

1. **ITAR Compliance Decision** (BLOCKER)
   - Use standard AWS (cost ✓, compliance ✗), or
   - Use AWS GovCloud (+30% cost, compliance ✓)?

2. **PiXie Inclusion Decision** (by Feb 15 from Max)
   - Phase 1 (scope now, +$300-400/mo), or
   - Phase 2 (scope later, defer cost)?

3. **TACC Allocation Status** (by Feb 15 from Dr. Clarno)
   - Still active through 2027? (use for HPC)
   - Expiring soon? (plan transition to AWS)

## Recommended Action

Approve Scenario B ($700–900/month) contingent on:
- [ ] ITAR clarification (standard vs. GovCloud)
- [ ] PiXie Phase 1 confirmation from Max
- [ ] TACC allocation timeline from Dr. Clarno

## Budget Line Item

**2026 (9 months):** $6,300–8,100  
**2027 (12 months):** $8,400–10,800  
**2-Year Total:** $14,700–18,900  

This enables: Digital twin validation, medical isotope scheduling agents, RAG-powered knowledge assistant, 7-year regulatory compliance archival.

---

[See detailed cost breakdown & technical justification below]
```

---

### Deliverable 2: Detailed Cost Tables (5 pages)

**File:** `aws-cost-estimate-tables.md`

**Content (template):**

```
# AWS Cost Estimate: Detailed Cost Tables

## Table 1: Monthly Recurring Costs (2026-2027)

| Service | Unit | Jan 2026 | Mar 2026 | Jun 2026 | Dec 2026 | 2027 |
|---------|------|----------|----------|----------|----------|------|
| **STORAGE** |
| S3 Standard (2yr live) | GB/mo | 7.5 | 7.5 | 7.5 | 7.5 | 7.5 |
| S3 Glacier (5yr archive) | GB/mo | 2.0 | 2.0 | 2.0 | 2.0 | 2.0 |
| RDS PostgreSQL | instance | $50 | $50 | $80* | $80 | $80 |
| **Subtotal Storage** | | **$67** | **$67** | **$100** | **$100** | **$100** |
| | | | | |
| **STREAMING** (if PiXie Phase 1) |
| Redpanda Cloud | events/sec | — | $250 | $250 | $250 | $250 |
| **Subtotal Streaming** | | **$0** | **$250** | **$250** | **$250** | **$250** |
| | | | | |
| **COMPUTE & ANALYTICS** |
| dbt + Dagster (hourly jobs) | runs/day | $90 | $90 | $90 | $90 | $90 |
| EKS (optional, control plane + 2 nodes) | mo | $0* | $200 | $200 | $200 | $200 |
| Claude API (RAG inference) | queries/mo | $300 | $300 | $300 | $300 | $300 |
| GPU training (if monthly retrain) | hr/mo | — | $150 | $150 | $150 | $150 |
| **Subtotal Compute** | | **$390** | **$740** | **$740** | **$740** | **$740** |
| | | | | |
| **CONTINGENCY (20%)** | | **$91** | **$211** | **$238** | **$238** | **$238** |
| | | | | |
| **TOTAL MONTHLY** | | **$548** | **$1,268** | **$1,328** | **$1,328** | **$1,328** |

*  Jan: pre-deployment (minimal). Mar: Phase 1 go-live. Jun: PiXie integration. Dec: full scale.

---

## Table 2: One-Time Costs (2026)

| Item | Quantity | Unit Cost | Total | Notes |
|------|----------|-----------|-------|-------|
| **Data Migration** |
| Historical MPACT HDF5 to S3 | [from Cole] GB | $0.02/GB | $[calc] | One-time import |
| Document corpus to S3 + Glacier | [from Jay] GB | $0.02/GB | $[calc] | One-time RAG setup |
| | | | |
| **Infrastructure Setup** |
| AWS account setup, IAM, VPC | lump sum | $500 | $500 | Consulting/labor |
| Iceberg + DuckDB setup | lump sum | $200 | $200 | Tools config |
| Dagster + dbt setup | lump sum | $300 | $300 | Orchestration setup |
| | | | |
| **Model Training & Validation** |
| Initial physics model training | GPU-hours | [from Jay] | $[calc] | Bias correction, UQ |
| Historical data labeling (if needed) | hours | $50/hr | $[calc] | QA review |
| | | | |
| **TOTAL ONE-TIME** | | | **$[SUM]** | Spring 2026 |

---

## Table 3: Annual Forecast (2026-2027)

| Category | 2026 (9mo) | 2027 (12mo) |
|----------|-----------|-----------|
| Storage | $675 | $900 |
| Streaming | $1,350 | $2,250 |
| Compute & LLM | $4,230 | $5,640 |
| Contingency | $1,620 | $2,160 |
| **Subtotal Recurring** | **$7,875** | **$10,950** |
| One-time (Spring 2026) | **$3,000–5,000** | — |
| **TOTAL BUDGET** | **$10,875–12,875** | **$10,950** |

---

## Table 4: Cost Sensitivity

| Assumption | Impact on 2026 Cost |
|-----------|-----------------|
| PiXie Phase 1 included | +$3,600/yr ($300/mo) |
| PiXie Phase 2 (deferred) | -$3,600/yr |
| TACC allocation expires (move compute) | +$2,400/yr ($200/mo) |
| High-frequency shadowcasting (continuous) | +$1,200/yr ($100/mo) |
| Multiple isotope models (5 vs. 1) | +$1,000/yr (training labor) |
| ITAR GovCloud (vs. standard AWS) | +$2,500/yr (+30%) |

---

## Table 5: Comparison: AWS vs. Alternative Architectures

| Architecture | Monthly Cost | Pros | Cons |
|--------------|-------------|------|------|
| **AWS Native (Proposed)** | $700–900 | Modern, scalable, cloud-native | Cloud lock-in, ITAR complexity |
| **TACC Primary + AWS DR** | $300–400 | Leverage existing allocation | Limited scalability, no multi-facility |
| **Hybrid (TACC physics + AWS analysis)** | $400–600 | Compliance-friendly, balanced | Operational complexity |
| **Full Self-Hosted (SeaweedFS on TACC)** | $0 (implicit) | No cloud costs | Maintenance burden, limited tools |

---

[Detailed breakdown by service category follows in technical appendix]
```

---

### Deliverable 3: Technical Justification & PRD Links (10 pages)

**File:** `aws-cost-estimate-justification.md`

**Content (outline/template):**

```
# AWS Cost Estimate: Technical Justification

## Section 1: Architecture Overview (2 pages)

### Why NeutronOS on AWS?

From [NeutronOS Master Tech Spec](../specs/neutron-os-master-tech-spec.md):
- Modern data lakehouse (Apache Iceberg) for time-travel queries
- Streaming-first architecture (Redpanda) for PiXie real-time data
- Kubernetes for reproducible, scalable operations
- MCP-based agent framework for automated analysis

**Cost implication:** Cloud-native tools have lower operational friction than self-hosted alternatives. Maintenance labor savings offset cloud compute costs.

### Phase 1 Scope (TRIGA only, 2026-2027)

From [Executive PRD](../prd/neutron-os-executive-prd.md):
- ✓ Data Platform (Bronze/Silver/Gold lakehouse)
- ✓ Analytics Dashboards (Superset)
- ✓ Reactor Ops Log (compliance tracking)
- ✓ Digital Twin Analytics (prediction validation)
- ✗ Multi-facility (Phase 5+)
- ✗ Training module (Phase 4+)

**Cost implication:** Single-facility keeps infrastructure lean. Multi-facility scaling would 2-3x costs; that's a Phase 5 decision.

---

## Section 2: Component Justification by Cost Driver (5 pages)

### Storage: $50–100/month

**Iceberg lakehouse on S3 + PostgreSQL RDS**

Why Iceberg? [ADR-003: Lakehouse Iceberg DuckDB](../adr/003-lakehouse-iceberg-duckdb.md)
- Time-travel queries (regulatory requirement for 7-year audit trail)
- Schema evolution without downtime
- ACID transactions (data integrity)

Cost breakdown:
- S3 Standard (2-year live): 150GB/yr → $3.45/month (formula: daily_volume × 2yr × $0.023/GB/mo)
- S3 Glacier (5-year archive): 150GB/yr → $0.90/month (formula: daily_volume × 5yr × $0.004/GB/mo)
- RDS PostgreSQL: micro instance $40 → large instance $80 for Gold table queries

Why RDS vs. self-hosted?
- Automated backups & 35-day retention
- Multi-AZ failover (if HA required)
- pgvector extension for RAG embeddings (search cost included)

**Sensitivity:** If Cole confirms >500GB/year archive, upgrade storage plan (cost +$10–20/mo).

### Streaming: $200–400/month (if PiXie included)

**Redpanda Cloud for event streaming**

Why Redpanda? [ADR-007: Streaming-First Architecture](../adr/007-streaming-first-architecture.md)
- Multi-facility-ready topic architecture
- Lower latency than AWS MSK for research workloads
- Managed ops (no Kafka clusters to tune)

Cost breakdown:
- Base tier: $150/month
- +$50/month per 10K events/sec above 100K

**If PiXie excluded:** Just $50–100/month for nightly Box sync.
**If PiXie included (Phase 1):** SMU (1-10 kHz) + TC (10 Hz) + other sensors → 50–100K events/sec → $250–350/month.

**Why not self-hosted Redpanda on EKS?**
- Self-hosted: ~$50 compute + $300/mo ops labor = $350/mo (not cost-saving)
- Managed: $250/mo, no ops burden → prefer managed

### Compute: $400–700/month

**Breakdown:**

1. **dbt + Dagster (orchestration):** $90/month
   - Hourly dbt runs → 24 runs/day × $0.10/run = $72/day
   - (Dagster on EKS is cheaper than Airflow; using EKS cost below)
   - Why scheduled? See [Data Platform PRD](../prd/data-platform-prd.md) refresh requirements

2. **EKS (optional):** $200–300/month
   - Control plane: $72/month (always)
   - 2× t3.medium nodes (autoscaling): $100–200/month
   - Why optional? Can run Dagster on TACC if allocation available
   - Why EKS if running? Kubernetes-native tooling, portable to multi-facility later

3. **Claude API (RAG inference):** $300–500/month
   - Estimated 100 RAG queries/day × $0.30/embedding = $9/day = $270/month
   - Plus LLM text generation (~$0.003 per completion)
   - Why Claude? [ADR-006: MCP Server Agentic Access](../adr/006-mcp-server-agentic-access.md) architecture assumes Claude-powered agents

4. **GPU training (optional, if monthly retraining):** $150/month
   - Estimate: monthly bias correction refit = 10 GPU-hours × $3.06/hr = $30/month
   - Plus quarterly physics model retraining = 50 GPU-hours × $3.06/hr = $38/quarter
   - Optional: can run on TACC if allocation supports it

---

## Section 3: Cost of Staying TACC-Only (Impact Analysis)

### Current Limitations

1. **Flask app is VPN-gated:** Outside researchers can't self-serve
2. **No RAG:** Can't ask "What was fuel temp last Tuesday?"
3. **No medical isotope scheduling agents:** Reduces production efficiency
4. **No real-time dashboards:** Operators see day-after data
5. **Box deprecation risk:** UT moving off Box → documents at risk

### Why AWS Enables New Capabilities

| Capability | Enabled by AWS | Research Impact | Cost Driver |
|------------|--|--|--|
| Multi-user dashboards (Superset) | Kubernetes + S3 | 5+ researchers querying simultaneously | EKS: $200/mo |
| RAG + knowledge assistant | Claude API + pgvector | 30% faster experiment prep | Claude: $300/mo |
| Medical isotope scheduling | Real-time predictions + streaming | 2 extra batches/week = $50K revenue/yr | Redpanda: $250/mo |
| Compliance audit trail | Iceberg time-travel + immutable logs | 7-year regulatory compliance | Storage: $50/mo |

### Cost of Going Without

**Quantified in lost research productivity:**

Example: Each medical isotope batch requires ~4 hours of operator prep (manual MPACT run, spreadsheet yield calc, risk assessment).
- Current: 1 batch/week = 4 hours labor
- With AWS agents: 0.5 hours labor (automated predictions + scheduling)
- Savings: 3.5 hours/week × $50/hr burdened = $175/week = $9,100/year
- **AWS infrastructure ROI:** 9 months

---

## Section 4: ITAR & Compliance Considerations

### Issue: Standard AWS is non-compliant for export-controlled reactor data

From stakeholder interviews:
> "The public should not know when the reactor is at power." — Nick

ITAR implications:
- Reactor power levels = information about operational capacity
- Critical rod heights = information about reactivity control
- Flux maps = information about core physics design

**Options:**

1. **Standard AWS (current plan)**
   - Pros: Cost-effective ($700–900/mo)
   - Cons: Violates ITAR if data crosses international boundaries
   - Recommendation: ✗ Do not proceed without export control review

2. **AWS GovCloud (ITAR-compliant)**
   - Pros: Approved for export-controlled data; same tools/architecture
   - Cons: +30% cost premium (~$210–270/mo additional)
   - Recommendation: ✓ Recommended if ITAR applies

3. **Hybrid (TACC for reactor data + AWS for analysis)**
   - Pros: Compliance-friendly; reactor data stays on US national lab allocation
   - Cons: Operational complexity (dual-tier data architecture)
   - Recommendation: ⚠️ Discuss with export control office

**Action Required:** Dr. Clarno to clarify with compliance/export control before approval.

---

## Section 5: Risk Analysis & Contingencies

### Technical Risks

| Risk | Probability | Impact | Mitigation Cost |
|------|-------------|--------|-----------------|
| PiXie DAQ volume exceeds estimate | Medium | +$200–400/mo | Real-time testing (Feb 15) |
| TACC allocation expires early | Low | +$200–300/mo (shift compute) | Trigger contingency plan |
| ITAR requires GovCloud | Medium | +$210/mo | Plan for in budget approval |
| Multi-facility request emerges | Low | +$300–500/mo | Revisit Phase 2 plan |

### Schedule Risks

| Risk | Timeline Impact | Mitigation |
|------|---|---|
| Data collection delays (Cole/Nick responses) | Push approval deadline 1 week | Set Feb 16 hard deadline for responses |
| ITAR ruling takes >2 weeks | Cannot start AWS procurement | Escalate export control decision to Dr. Clarno TODAY |
| PiXie specs unclear from Max | Cannot size streaming | Schedule call with Max Feb 13 |

### Contingency Budget

Recommend 20% contingency ($140–270/month) for unknown unknowns.
- Model retraining takes longer than estimated
- Unexpected data retention requirements
- Scaling experiments (more dashboards, more users)

---

## Section 6: References to Existing Documentation

### Architecture & Vision
- [NeutronOS Master Tech Spec](../specs/neutron-os-master-tech-spec.md) — comprehensive system design
- [Data Architecture Spec](../specs/data-architecture-spec.md) — lakehouse, retention, backup policy
- [Digital Twin Architecture](../specs/digital-twin-architecture-spec.md) — prediction models, validation framework

### Product Requirements
- [Executive PRD](../prd/neutron-os-executive-prd.md) — Phase 1-5 roadmap
- [Data Platform PRD](../prd/data-platform-prd.md) — Bronze/Silver/Gold design
- [Medical Isotope PRD](../prd/medical-isotope-prd.md) — yield prediction, scheduling
- [Analytics Dashboards PRD](../prd/analytics-dashboards-prd.md) — Superset design

### Decisions & Rationale
- [ADR-003: Iceberg Lakehouse](../adr/003-lakehouse-iceberg-duckdb.md)
- [ADR-006: MCP Agents](../adr/006-mcp-server-agentic-access.md)
- [ADR-007: Streaming-First](../adr/007-streaming-first-architecture.md)
- [ADR-008: WASM Surrogates](../adr/008-wasm-extension-runtime.md)

### Incident Analysis (Justifies Real-Time Dashboards)
- [Sm-153 Incident Analysis](../Neutron_OS/docs/analysis/Sm153_Incident_Analysis_PRD_Implications.md) — pre-production validation needs
- [PRD Changes Summary](../Neutron_OS/docs/analysis/PRD_Change_Summary.md) — new dashboard scenarios

---

## Section 7: Approval Checklist for Dr. Clarno

Before authorizing AWS spend, confirm:

**Data Collection (due Feb 16):**
- [ ] Cole: MPACT simulation frequency & archive size
- [ ] Nick: Isotope types, production rate, prediction validation volume
- [ ] Max: PiXie Phase 1 inclusion decision + data volume estimate
- [ ] Jay: RAG corpus size, model training frequency

**Compliance & Strategy (due Feb 15):**
- [ ] ITAR classification ruling (standard AWS vs. GovCloud)
- [ ] TACC allocation status (active through 2027?)
- [ ] Multi-facility roadmap (single-facility 2+ years?)

**Financial:**
- [ ] Approve Scenario B ($700–900/month) as planning baseline
- [ ] Approve contingency (20% buffer)
- [ ] Authorize one-time migration costs ($3–5K spring 2026)

**Sign-off:**
- [ ] Dr. Clarno signature on budget approval
- [ ] CIO/Finance approval of AWS account creation
- [ ] Export control clearance (if ITAR applies)

---

[Appendix: Detailed service-by-service cost breakdown, historical AWS pricing, multi-facility cost scaling model]
```

---

## How to Distribute & Collect

1. **Send to Cole, Nick, Max, Jay:**
   ```
   Subject: AWS Cost Estimate Data Collection — Response Due Feb 16 EOD
   
   Hi [name],
   
   We're finalizing the AWS infrastructure cost estimate for NeutronOS Phase 1 
   to submit to Dr. Clarno by Feb 18.
   
   Your input is critical. Please fill out the sections in the attached worksheet:
   
   - Cole: Sections A (MPACT & Physics)
   - Nick: Section B (Operations & Production)
   - Max: Section C (PiXie Hardware)
   - Jay: Section D (ML/Data Engineering)
   
   Estimated time: 30–60 min per section. Many questions can be answered with 
   "I'll measure" or "TBD pending decision" — those are fine, we'll note them 
   as constraints.
   
   Please reply by EOD Feb 16 so we can consolidate & finalize costs by Feb 17.
   
   [Link to aws-cost-estimate-data-collection.md]
   ```

2. **Follow up Feb 14-15:**
   - Send reminder to anyone who hasn't responded
   - Schedule quick calls with anyone uncertain about their answers

3. **Consolidate Feb 16-17:**
   - Fill in Section I (responses) of worksheet
   - Run cost calculations using Section F framework
   - Draft three deliverables (summary, tables, justification)

4. **Submit Feb 18:**
   - Email Dr. Clarno with executive summary
   - Attach detailed tables & technical justification
   - Request meeting if ITAR or other approvals needed

---

## Success Criteria

✓ Worksheet distributed by Feb 12 EOD  
✓ 80% response rate by Feb 16 (OK if some "TBD")  
✓ Cost estimate accurate to ±30% (typical for budgeting)  
✓ Dr. Clarno approves by Feb 20 (for March procurement)  
✓ AWS account creation starts Feb 21 (for Phase 1 deployment ~Apr 1)

