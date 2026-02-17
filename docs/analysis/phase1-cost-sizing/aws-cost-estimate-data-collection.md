# AWS Cost Estimate: Data Collection Worksheet

**Document Purpose:** Systematic data gathering to estimate NeutronOS Phase 1 (2026-2027) AWS infrastructure costs for UT TRIGA  
**Status:** IN PROGRESS (Feb 12, 2026)  
**Deadline:** Tuesday, Feb 18 (for Dr. Clarno budget submission)  
**Organized by:** Stakeholder + Cost Driver  

**📋 Related Documents:**
- **[COST-ESTIMATION-SOURCES.md](COST-ESTIMATION-SOURCES.md)** ← TL;DR version (start here!)
- [aws-cost-estimation-methodology.md](aws-cost-estimation-methodology.md) — Deep dive: methodology, pricing sources, tool integration
- [aws-comprehensive-utility-usage.md](aws-comprehensive-utility-usage.md) — Detailed service breakdown (9 categories + external)
- [aws-cost-estimate-to-approval.md](aws-cost-estimate-to-approval.md) — Workflow to final deliverables
- [README-COST-ESTIMATE.md](README-COST-ESTIMATE.md) — Master orientation & timeline

---

## Quick Reference: Who to Ask, What They Know

| Person | Role | Key Questions | Priority |
|--------|------|----------------|----------|
| **Cole** | Digital Twin Physics | MPACT frequency, historical data volume, bias correction retraining | P0 |
| **Nick** | TRIGA Operations | Production workflow, isotope types, validation requirements | P0 |
| **Max** | PiXie Hardware | DAQ device count, sample rates, data format, data retention | P0 |
| **Jay** | ML/Data Eng | Training data breakdown, model retraining frequency, shadowcasting volume | P1 |
| **Dr. Clarno** | Approval Gate | TACC allocation status, compliance requirements, budget flexibility | P0 |

---

## How This Worksheet Connects to Cost Estimation

### Questions → Pricing Tools → Cost Components

Each question below is designed to feed directly into the **AWS Pricing Calculator** or **cost_estimation_tool** Python library.

| Section | Question | Maps To | AWS Pricing Page | Tool |
|---------|----------|---------|---|---|
| A | MPACT frequency, wall-clock | EKS compute hours | https://aws.amazon.com/eks/pricing/ | cost_estimation_tool.CostCalculator |
| A | Archive size | S3 Glacier storage | https://aws.amazon.com/s3/pricing/ | AWS Pricing Calculator |
| B | Operating hours/week | EKS node utilization % | https://aws.amazon.com/eks/pricing/ | cost_estimation_tool.CostCalculator |
| B | Data volume (150 GB/yr) | S3 Standard + Glacier | https://aws.amazon.com/s3/pricing/ | AWS Pricing Calculator |
| C | PiXie Phase 1 yes/no | Redpanda Cloud base tier | https://redpanda.com/pricing | cost_estimation_tool.CostCalculator |
| C | PiXie data volume (GB/day) | Redpanda throughput tiers | https://redpanda.com/pricing | Redpanda capacity calculator |
| D | RAG document count | Claude API input tokens | https://www.anthropic.com/pricing | cost_estimation_tool.CostCalculator |
| D | Training frequency | CloudWatch logs volume | https://aws.amazon.com/cloudwatch/pricing/ | AWS Pricing Calculator |
| E | Region (standard vs GovCloud) | Regional pricing delta | https://aws.amazon.com/pricing/ | AWS Pricing Calculator |
| E | Audit retention (years) | S3 Glacier long-term storage | https://aws.amazon.com/s3/pricing/ | AWS Pricing Calculator |

**How answers are used:**
1. Stakeholder fills worksheet (this doc, Feb 12–16)
2. Responses loaded into cost_estimation_tool (Feb 17)
3. Tool queries AWS Pricing Calculator inputs
4. Final costs generated with citations (Feb 18)

See [aws-cost-estimation-methodology.md](aws-cost-estimation-methodology.md) **Section 2.1** for detailed mappings.

---

## Pricing Data Current As Of

**Baseline Date:** February 12, 2026  
**Pricing Sources:** AWS, Redpanda, Anthropic (all updated continuously; calculator.aws/ always reflects current rates)  
**Validity:** Through May 12, 2026 (3-month horizon)

If you need current pricing, use:
- **AWS Services:** https://calculator.aws/
- **Redpanda Cloud:** https://redpanda.com/pricing
- **Claude API:** https://www.anthropic.com/pricing

---

## SECTION A: COLE — Digital Twin Training & Simulation

### Context: MPACT Simulation Volume & Physics Data

From [TRIGA_DT_Notes.md](../TRIGA_Digital_Twin/docs/data_flow/TRIGA_DT_Notes.md):
```
Current pipeline (nightly at 12:30 AM):
1. rclone syncs ZOC logs from Box → TACC corral-secure
2. ZOC parser → CSVs (100ms resolution)
3. Change point detection → identifies stable reactor states
4. SLURM jobs → MPACT simulations for each state
5. Results: HDF5 → PostgreSQL/TimescaleDB
```

**Cost Driver:** MPACT simulation frequency + archive size = HPC allocation implications + historical data migration cost

---

### A1. MPACT Simulation Frequency & Compute

**Question Chain:**

**A1a.** How many distinct reactor "states" are identified per nightly Shadowcaster run?  
*Example: 10-20 stable states per day?*  
**Cost impact:** If 20 states/day × 365 = 7,300 MPACT runs/year

**A1b.** How long does one MPACT simulation take (wall-clock on TACC)?  
*Example: 30 sec? 5 min? 30 min?*  
**Cost impact:** Core-hours/year = compute allocation utilization

**A1c.** Will Phase 1 (2026) scale the nightly batch, or keep 1x/day?  
**Cost impact:** If scaled to 3x/day, HPC allocation pressure increases

**A1d.** Are you planning to shift MPACT off TACC to AWS in Phase 1, or keep TACC as primary?  
**Cost impact:** If AWS: add EKS GPU nodes ($3+/hour). If TACC: implicit allocation cost.

---

### Data Collected: A1 MPACT Frequency

| Field | Your Answer | Notes |
|-------|------------|-------|
| States per nightly run | _____ | (estimated or measured) |
| Wall-clock time per MPACT | _____ | (in seconds or minutes) |
| Annual MPACT runs | _____ | (auto-calculated: states/day × 365) |
| Phase 1 scaling plan | _____ | (1x/day batch or 3x/day or continuous?) |
| MPACT compute location | _____ | (TACC primary / AWS primary / hybrid) |

---

### A2. Historical MPACT Archive & Migration

**Question Chain:**

**A2a.** How many historical MPACT HDF5 output files exist (all time)?  
*Example: 1,000? 10,000? How many years of archive?*

**A2b.** What's the typical size of one MPACT HDF5 output?  
*Example: 1 MB? 5 MB? 20 MB?*

**A2c.** What's the current total size on TACC (corral-secure)?  
*Command: `du -sh /path/to/mpact/archive` or estimate from allocation usage*

**A2d.** Will you migrate all historical HDF5 to AWS S3 in Phase 1, or keep on TACC only?  
**Cost impact:** One-time S3 import cost (~$0.02/GB) vs. ongoing storage (negligible if archive tier)

---

### Data Collected: A2 Historical MPACT Archive

| Field | Your Answer | Notes |
|-------|------------|-------|
| Total # of HDF5 files | _____ | (all historical) |
| Avg size per HDF5 | _____ | (MB each) |
| Total archive size on TACC | _____ | (GB) |
| Years of history | _____ | (e.g., 3 years? 10 years?) |
| Migration to AWS plan | _____ | (migrate all? keep on TACC?) |
| One-time migration cost | _____ | (auto-calc: size × $0.02/GB) |

---

### A3. Bias Correction Model Training

**Question Chain:**

**A3a.** Do you have a bias correction model (measured vs. MPACT predictions)?  
*Answer: yes/no + describe*

**A3b.** How many (MPACT prediction, measured actual) pairs exist for training?  
*Example: 100 pairs? 1,000? 10,000?*

**A3c.** How often do you refit the bias correction model?  
*Example: annually? Monthly after new fuel? Only after facility changes?*

**A3d.** What's the compute cost of retraining?  
*Example: 1 minute on laptop? 30 min on TACC? Requires re-running MPACT?*

---

### Data Collected: A3 Bias Correction

| Field | Your Answer | Notes |
|-------|------------|-------|
| Has bias correction model? | ☐ Yes ☐ No | |
| # of training pairs | _____ | (measured vs. MPACT) |
| Retraining frequency | _____ | (annual/monthly/on-demand?) |
| Retraining compute | _____ | (lightweight/moderate/heavy?) |

---

### A4. Model Validation & Uncertainty Quantification

**Question Chain:**

**A4a.** How do you compute confidence intervals on predictions (e.g., ±7% on yield)?  
*Example: historical scatter? UQ propagation? Ensemble methods?*

**A4b.** Do you have a published validation dataset for MPACT V&V?  
*Example: for NRC licensing, OSTI/Zenodo archive?*

**A4c.** How many operating points (distinct reactor states) are documented in validation data?  
*Example: 50? 500? Full year archive?*

---

### Data Collected: A4 Validation

| Field | Your Answer | Notes |
|-------|------------|-------|
| UQ methodology | _____ | (how computed?) |
| Published V&V dataset? | ☐ Yes ☐ No | (plans?) |
| # of validation operating points | _____ | (coverage estimate) |

---

## SECTION B: NICK — TRIGA Operations & Production Workflow

### Context: Operational Data Rates & Medical Isotope Production

From [medical-isotope-prd.md](../Neutron_OS/docs/prd/medical-isotope-prd.md):
```
Weekly production batches (Mondays typically)
State machine: Ordered → Scheduled → Producing → QA → Shipped → Delivered
Each batch generates: pre-prod prediction, real-time monitoring, post-prod validation
```

**Cost Driver:** Prediction validation volume + isotope model variants = database size + training data

---

### B1. Reactor Operating Schedule

**Question Chain:**

**B1a.** How many hours per week is TRIGA operating (average)?  
*Example: 16 h/week? 40 h/week?*

**B1b.** Is ZOC logging continuous (24/7) or only during power ops?  
**Cost impact:** Continuous = more CSV storage; ops-only = less

**B1c.** Are there seasonal variations in operating schedule?  
*Example: summer shutdown? Maintenance windows?*

---

### Data Collected: B1 Operating Schedule

| Field | Your Answer | Notes |
|-------|------------|-------|
| Avg operating hours/week | _____ | |
| ZOC logging schedule | ☐ 24/7 ☐ Ops only | |
| Seasonal variations | _____ | (% downtime) |

---

### B2. Medical Isotope Production Rate & Isotope Types

**Question Chain:**

**B2a.** How many isotope types does UT currently produce?  
*Example: Sm-153, I-131, Mo-99, other?*

**B2b.** What's the current weekly production rate?  
*Example: 1 batch/week? 2 batches/week? Multiple isotopes per batch?*

**B2c.** For each isotope, do you plan separate yield prediction models, or one generalized model?  
**Cost impact:** N models = N training datasets, N validation workflows

**B2d.** Are there position-specific flux effects (like Sm-153 incident highlighted)?  
*Example: 3-5 distinct irradiation positions?*

**B2e.** If position-specific: do you plan separate models per position, or correction factors?  
**Cost impact:** More models = more training data, more validation

---

### Data Collected: B2 Production

| Field | Your Answer | Notes |
|-------|------------|-------|
| # of isotope types | _____ | (list them) |
| Batches/week | _____ | (current rate) |
| Modeling approach | ☐ 1 generalized ☐ per-isotope | |
| # of isotope models planned | _____ | (auto-calc from above) |
| Position-specific effects? | ☐ Yes ☐ No | (# positions if yes) |
| Position modeling approach | ☐ sep models ☐ correction factors | |

---

### B3. Prediction Validation & Shadowcasting

**Question Chain:**

**B3a.** For each production batch, what data do you capture?  
*Example: pre-prod prediction (1 file)? Real-time monitoring during irradiation (how frequent?)? Post-prod yield measurement?*

**B3b.** During irradiation (4-8 hours), what's the monitoring frequency?  
*Example: 1 prediction/min? 1 per 10 min? Continuous?*

**B3c.** What variables are predicted/monitored?  
*Example: power, fuel temp, xenon state, yield, other?*

**B3d.** How long do you retain prediction validation data?  
*Example: 1 year rolling? 7 years archive? Permanent?*

---

### Data Collected: B3 Prediction Validation

| Field | Your Answer | Notes |
|-------|------------|-------|
| Pre-prod data captured | _____ | (what? size?) |
| Real-time monitoring freq | _____ | (1/min? continuous?) |
| Irradiation duration (avg) | _____ | (hours) |
| Variables predicted | _____ | (list them) |
| Predictions per batch | _____ | (auto-calc: freq × duration) |
| Annual predictions | _____ | (auto-calc: per batch × 52) |
| Retention policy | _____ | (1yr? 7yr?) |

---

### B4. Data Volume from Operations

**Question Chain:**

**B4a.** The current baseline is "150GB/year" (from Jay). Can you break this down by category?  
*Example: ZOC CSVs? MPACT HDF5? Plotly visualizations? Database? Other?*

**B4b.** Does this 150GB include:
- [ ] Raw serial CSVs (100ms, all channels)?
- [ ] MPACT HDF5 outputs?
- [ ] PostgreSQL/TimescaleDB backup?
- [ ] Plotly HTML visualizations?
- [ ] Documentation/metadata?

**B4c.** What does "safe breathing room" imply? (Jay said "150GB should be plenty")  
*Estimate: current burn rate? Expected 2026 growth?*

---

### Data Collected: B4 Data Volume Breakdown

| Field | Your Answer | Notes |
|-------|------------|-------|
| Current annual burn (measured) | _____ | (GB/yr) |
| ZOC CSV component | _____ | (% or GB?) |
| MPACT HDF5 component | _____ | (% or GB?) |
| Database component | _____ | (% or GB?) |
| Visualization component | _____ | (% or GB?) |
| Growth rate 2026 projection | _____ | (+20%? +50%?) |

---

## SECTION C: MAX — PiXie Hardware DAQ

### Context: SMU & Thermocouple Data Acquisition

From [netl_pxi/docs/architecture/](../TRIGA_Digital_Twin/netl_pxi/docs/architecture/):
```
PXI Chassis Hardware:
- SMU (Source Measure Unit): slot 8, measures mini fission chamber bias
- Thermocouple: slot 11, 6-channel K-type temperature acquisition
- Communication: gRPC over Ethernet (NI gRPC server)
```

**Cost Driver:** If PiXie included in Phase 1, data volume could increase 10-100x; if excluded, minimal impact

---

### C1. Current PiXie Configuration & Status

**Question Chain:**

**C1a.** Is PiXie currently logging data continuously, or in development/testing phase?  
**Cost impact:** If "testing", defer PiXie from Phase 1 cost estimate

**C1b.** Current device configuration:
- SMU sampling rate: (config shows 0.1-1.8MHz possible, what's actual?)
- Thermocouple sampling rate: (config shows 10Hz default, is this correct?)

**C1c.** Are there other NI modules planned beyond SMU + TC?  
*Example: pressure transducers, flow meters, gamma spectroscopy inputs?*

**C1d.** Current data storage location:  
*Example: local server disk? TACC? Box? On-demand only?*

---

### Data Collected: C1 PiXie Status

| Field | Your Answer | Notes |
|-------|------------|-------|
| Current status | ☐ Prod ☐ Testing ☐ Planned | |
| SMU sampling rate | _____ Hz | (actual deployment) |
| TC sampling rate | _____ Hz | (actual deployment) |
| # of TC channels | _____ | (6 as config shows?) |
| Other modules? | ☐ Yes ☐ No | (list if yes) |
| Storage location | _____ | |

---

### C2. Data Volume Estimation

**Question Chain:**

**C2a.** What's the current daily data volume from PiXie?  
*Command: `du -sh /path/to/pixie/data` for past week?*  
Or estimate: (# devices) × (sample rate Hz) × (bytes/sample) × (operating hours/day)

**C2b.** Data format:  
*Example: binary protobuf (.pb2)? CSV? HDF5? Direct to DB?*

**C2c.** Operating schedule:  
*Example: 24/7? Only during reactor ops (4-8h/day)? Duty cycle?*

**C2d.** Retention requirement:  
*Example: keep raw data, or can aggregate/compress?*

---

### Data Collected: C2 Data Volume

| Field | Your Answer | Notes |
|-------|------------|-------|
| Current daily volume (measured) | _____ MB/day | |
| Data format | _____ | (binary/CSV/HDF5/DB) |
| Operating duty cycle | _____ | (% uptime) |
| Annual volume (calc) | _____ GB/yr | (auto-calc: daily × 365 × duty%) |
| Retention policy | _____ | (days/weeks/years?) |
| Compression possible? | ☐ Yes ☐ No | |

---

### C3. PiXie Inclusion in Phase 1

**Question Chain:**

**C3a.** Will PiXie data be ingested into NeutronOS Phase 1 (2026), or deferred to Phase 2/3?  
**Cost impact:** Phase 1 = add storage + streaming; Phase 2+ = scope later

**C3b.** If Phase 1: when should archival to AWS begin?  
*Example: day 1 of deployment? After pilot validation?*

**C3c.** Are there any scaling plans (more devices, higher sample rates)?  
**Cost impact:** 10x more devices = 10x more data = significant cost jump

---

### Data Collected: C3 Phase 1 Inclusion

| Field | Your Answer | Notes |
|-------|------------|-------|
| PiXie in Phase 1? | ☐ Yes ☐ No ☐ Pilot only | |
| Archival start date | _____ | (if Phase 1) |
| Future scaling plans | _____ | (# devices, rates?) |

---

## SECTION D: JAY — ML/Data Engineering

### Context: Training Data, Model Retraining, Inference Patterns

**Cost Driver:** Training compute (CPU vs. GPU), embedding API calls, vector DB size, model versioning

---

### D1. RAG Training Data (Document Embeddings)

**Question Chain:**

**D1a.** How many documents need to be embedded for the RAG knowledge base?  
*Example: 100? 1000? 10,000 PDFs, meeting transcripts, SOPs?*

**D1b.** What's the total size of the document corpus?  
*Example: 1 GB? 10 GB? 100 GB?*

**D1c.** Embedding model & cost:  
*Current: OpenAI text-embedding-ada-002 (~$0.00002 per 1K tokens)?*  
*Or self-hosted: Ollama on TACC (free, but uses GPU hours)?*

**D1d.** How often are new documents added?  
*Example: daily? weekly? monthly?*

**D1e.** Vector DB storage:  
*Example: pgvector (PostgreSQL, free)? Pinecone managed ($100+/mo)?*

---

### Data Collected: D1 RAG & Embeddings

| Field | Your Answer | Notes |
|-------|------------|-------|
| # of documents for RAG | _____ | |
| Document corpus size | _____ GB | |
| Embedding model | _____ | (OpenAI / Ollama / other) |
| One-time embedding cost | _____ | (auto-calc: corpus × model cost) |
| Document add frequency | _____ | (monthly rate) |
| Recurring embedding cost | _____ | (auto-calc: monthly adds × cost) |
| Vector DB choice | _____ | (pgvector / Pinecone / other) |

---

### D2. Model Training Data & Retraining Frequency

**Question Chain:**

**D2a.** For physics model training (point kinetics, xenon dynamics, bias correction):  
*How many hours of historical reactor log data do you have?*  
*Example: 1 year = 8,760 hours? 5 years = 43,800 hours?*

**D2b.** Are you planning deep learning models (requires GPU), or interpretable models (CPU)?  
*Example: point kinetics ODE solver? Gaussian processes? Neural networks?*

**D2c.** If DL: typical GPU training time?  
*Example: 10 hours? 100 hours? Per training cycle?*

**D2d.** Retraining frequency:  
*Example: once after Phase 1 deployment, then quarterly? Monthly?*

**D2e.** Model versioning & registry:  
*How many model versions do you expect to keep? (10? 50? 100+?)*

---

### Data Collected: D2 Model Training

| Field | Your Answer | Notes |
|-------|------------|-------|
| Historical training data (hours) | _____ | |
| Model type | ☐ Interpretable ☐ DL | |
| GPU training hours per refit | _____ | (if DL) |
| Retraining frequency | _____ | (per year) |
| Annual GPU hours (calc) | _____ | (auto-calc: freq × hours) |
| Model registry size | _____ | (# versions) |

---

### D3. Shadowcasting & Prediction Validation

**Question Chain:**

**D3a.** From the Sm-153 incident analysis, you need "predicted vs. actual" dashboards.  
*Data grain: daily aggregates? Per-state? Continuous?*

**D3b.** Storage approach:  
*Example: store every prediction tuple, or summarize?*

**D3c.** Validation metrics computed:  
*Example: RMSE, MAPE, max error, per-isotope accuracy?*

**D3d.** Triggering retraining:  
*Example: if RMSE > threshold, auto-retrain? Or manual review?*

---

### Data Collected: D3 Shadowcasting

| Field | Your Answer | Notes |
|-------|------------|-------|
| Prediction storage grain | _____ | (daily/per-state/continuous?) |
| Annual # of predictions stored | _____ | |
| Validation metrics | _____ | (list computed metrics) |
| Retrain trigger logic | ☐ Auto ☐ Manual ☐ Scheduled | |

---

## SECTION E: COMPLIANCE & APPROVAL GATES

### E1. Regulatory & Compliance Requirements

**Question for:** Dr. Clarno (or compliance officer)

**E1a.** What regulatory framework applies?  
*Options: ITAR (export control)? FDA (medical isotopes)? NRC (nuclear facility)? Other?*

**E1b.** Data residency requirements:  
*Must all data stay in US? Can use standard AWS, or must be AWS GovCloud?*

**E1c.** Audit trail requirements:  
*Immutable records needed? For how long? (1 year? 7 years? Permanent?)*

**E1d.** What's the current TACC allocation status?  
*Active? Expiring? What's the implicit annual cost/budget?*

---

### Data Collected: E1 Compliance

| Field | Your Answer | Notes |
|-------|------------|-------|
| Regulatory frameworks | _____ | (ITAR/FDA/NRC?) |
| AWS region requirement | _____ | (standard / GovCloud?) |
| Audit trail retention | _____ | (years) |
| TACC allocation status | _____ | (active until when?) |

---

## SECTION F: COST CALCULATION FRAMEWORK

### How Answers Drive Costs

Once data collection complete, costs calculated as:

```
STORAGE COSTS (Monthly):
─────────────────────────────────────────
S3 Standard (hot data, 2yr):
  = (Daily volume GB) / 365 × 2 × $0.023 per GB/mo

S3 Glacier (cold archive, 5-7yr):
  = (Daily volume GB) / 365 × 5 × $0.004 per GB/mo

RDS PostgreSQL (Gold tables + vectors):
  = (Database size) × instance cost ($40-100/mo)

Total Storage:  $20-100/mo baseline

─────────────────────────────────────────

STREAMING COSTS (Monthly):
─────────────────────────────────────────
If PiXie Phase 1:
  Redpanda Cloud: $200-300/mo (managed)
  OR MSK Serverless: $200-400/mo (AWS)
  OR self-hosted on EKS: ~$50 compute + ops

If PiXie deferred:
  Redpanda: $100-150/mo (lower throughput)

Total Streaming:  $100-400/mo

─────────────────────────────────────────

COMPUTE COSTS (Monthly):
─────────────────────────────────────────
dbt + DuckDB (transformations):
  = hourly Dagster jobs × $0.10/run
  ≈ 30 runs/day × $0.10 × 30 = $90/mo

Model training (if GPU required):
  = annual GPU hours × ($3.06/hr for p3.2xlarge)
  ÷ 12 = _____/mo

LLM inference (Claude API):
  = monthly queries × $0.30 per embedding
  ≈ $300-500/mo for interactive RAG

EKS cluster (optional):
  = control plane $72/mo + nodes $100-300/mo
  = $172-372/mo (or $0 if using TACC)

Total Compute:  $200-700+/mo

─────────────────────────────────────────

PHASE 1 TOTAL (2026-2027):
  Storage: $50-100/mo
  Streaming: $100-400/mo (if PiXie included)
  Compute: $200-700/mo
  ──────────────────────
  Subtotal: $350-1200/mo

  Contingency (20%): +$70-240
  ══════════════════════════
  TOTAL: $420-1440/mo

  2026 (9 months): $3,780-12,960
  2027 (12 months): $5,040-17,280
```

---

## SECTION G: DATA COLLECTION CHECKLIST

### By Deadline (Feb 18, 2026)

**For Cole (MPACT & Physics):**
- [ ] A1a: States per nightly run
- [ ] A1b: Wall-clock time per MPACT
- [ ] A1d: MPACT compute location (TACC vs. AWS)
- [ ] A2c: Total MPACT archive size on TACC
- [ ] A3a-A3c: Bias correction model details
- [ ] A4a: UQ methodology

**For Nick (Operations & Production):**
- [ ] B1a: Operating hours/week
- [ ] B2a-B2e: Isotope types, production rate, modeling approach
- [ ] B3a-B3d: Prediction validation details
- [ ] B4a-B4c: Data volume breakdown of 150GB/year

**For Max (PiXie Hardware):**
- [ ] C1a-C1d: Current PiXie status & config
- [ ] C2a-C2c: Daily data volume, format, operating schedule
- [ ] C3a-C3c: Phase 1 inclusion decision

**For Jay (ML/Data Engineering):**
- [ ] D1a-D1e: RAG document count, corpus size, embedding strategy
- [ ] D2a-D2e: Training data, model type, retraining frequency
- [ ] D3a-D3d: Shadowcasting validation approach

**For Dr. Clarno (Approval):**
- [ ] E1a-E1d: Regulatory framework, TACC allocation status

---

## SECTION H: NEXT STEPS

1. **Share this worksheet** with Cole, Nick, Max, Jay (Feb 12-13)
2. **Collect answers** by Feb 16 EOD
3. **Consolidate responses** in Section I (Feb 17)
4. **Calculate costs** using framework in Section F (Feb 17)
5. **Draft executive summary** for Dr. Clarno (Feb 17-18)
6. **Submit budget approval** by Feb 18 deadline

---

## SECTION I: RESPONSES (To be filled in)

### Cole's Answers (MPACT & Physics)

**A1a: States per nightly run**  
```
[response here]
```

**A1b: Wall-clock time per MPACT**  
```
[response here]
```

**A1d: MPACT compute location**  
```
[response here]
```

**A2c: Total MPACT archive size**  
```
[response here]
```

**A3a-c: Bias correction model**  
```
[response here]
```

**A4a: UQ methodology**  
```
[response here]
```

---

### Nick's Answers (Operations & Production)

**B1a: Operating hours/week**  
```
[response here]
```

**B2a-e: Isotope types & modeling**  
```
[response here]
```

**B3a-d: Prediction validation**  
```
[response here]
```

**B4a-c: Data volume breakdown**  
```
[response here]
```

---

### Max's Answers (PiXie Hardware)

**C1a-d: PiXie status & config**  
```
[response here]
```

**C2a-c: Data volume & format**  
```
[response here]
```

**C3a-c: Phase 1 inclusion**  
```
[response here]
```

---

### Jay's Answers (ML/Data Engineering)

**D1a-e: RAG & embeddings**  
```
[response here]
```

**D2a-e: Model training**  
```
[response here]
```

**D3a-d: Shadowcasting**  
```
[response here]
```

---

### Dr. Clarno's Answers (Approval)

**E1a-d: Compliance & allocation**  
```
[response here]
```

---

## REFERENCES

- [TRIGA Data Flow Architecture](../TRIGA_Digital_Twin/docs/data_flow/TRIGA_DT_Notes.md)
- [Superset Reactor Performance Analytics](../Neutron_OS/docs/scenarios/superset/reactor-performance-analytics/scenario.md)
- [Medical Isotope Production PRD](../Neutron_OS/docs/prd/medical-isotope-prd.md)
- [Data Platform PRD](../Neutron_OS/docs/prd/data-platform-prd.md)
- [Sm-153 Incident Analysis](../Neutron_OS/docs/analysis/Sm153_Incident_Analysis_PRD_Implications.md)
- [PiXie Architecture](../TRIGA_Digital_Twin/netl_pxi/docs/architecture/system-overview.md)
- [Original Cost Estimation Plan](#) (from planning phase)

