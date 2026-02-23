# Cost Estimation Form: Ben — Neutron OS Platform & NuclearBench

**For:** Ben (NeutronOS Platform Architecture & NuclearBench)  
**Deadline:** Friday, February 28, 2026, 5 PM  
**Time to complete:** 8–10 minutes  
**Completed by:** _____________________ (Your name)

---

## Precision Expectation

Order-of-magnitude estimates (±50%) are perfect. Rough ranges beat false precision. T-shirt sizing or "I don't know" is fine—we have fallbacks.

---

## Overview

I need your help with:
- Neutron OS platform architecture and shared infrastructure decisions
- NuclearBench infrastructure footprint and growth
- Integration patterns for all initiatives (TRIGA DT, MSR DT, OffGas DT, etc.)
- Multi-tenant vs. dedicated infrastructure choices

**Context:** Your platform decisions directly affect cloud costs. We need to understand shared infrastructure scope (Iceberg lakehouse, EKS cluster sizing, RDS, Superset, Claude API) and NuclearBench requirements.

---

## Question 1: Neutron OS Platform Scope

### What components are in Phase 1 scope?

**Core platform components (check all that apply):**
- [ ] **Iceberg lakehouse** (S3 Bronze/Silver/Gold layers for all data)
- [ ] **EKS cluster** (Kubernetes for Dagster jobs, dbt transformations, inference)
- [ ] **RDS PostgreSQL** (shared metadata, Gold tables, lineage tracking)
- [ ] **Superset** (dashboards for all initiatives)
- [ ] **Dagster** (workflow orchestration)
- [ ] **dbt** (data transformations)
- [ ] **Claude API** (RAG, analysis, automation)
- [ ] **Redpanda** (event streaming; TBD by Max)
- [ ] **Monitoring/Logging** (CloudWatch, structured logs)

**Your answer:** _______________________________________________

---

## Question 2: Shared Infrastructure Model

### How will initiatives share Neutron OS infrastructure?

**Sharing model:**
- [ ] **Fully shared** — TRIGA DT, MSR DT, OffGas DT, NuclearBench all use same EKS, Iceberg, RDS
- [ ] **Mostly shared** — Share storage (Iceberg) + RDS; compute (EKS) partially separate
- [ ] **Hybrid** — Core platform shared; each initiative has dedicated sub-clusters/buckets
- [ ] **Mostly separate** — Own AWS accounts/clusters for each initiative (coordinated via API)
- [ ] **TBD** — Waiting on architecture decision

**Your answer:** _______________________________________________

### If shared, what's the isolation level?

**Isolation approach:**
- [ ] **Multi-tenant within cluster** (all jobs in same EKS; namespace/RBAC isolation)
- [ ] **Separate namespaces** (same cluster, logical isolation)
- [ ] **Separate subnets/security groups** (VPC-level isolation)
- [ ] **Separate AWS accounts** (hard isolation; cross-account IAM)
- [ ] **TBD** (decision pending)

**Your answer:** _______________________________________________

---

## Question 3: NuclearBench Infrastructure Needs

### What's NuclearBench's primary purpose?

**Primary use case:**
- [ ] Benchmark database (static reference data for comparison)
- [ ] Continuous ingestion (new data feeds from multiple facilities)
- [ ] Computational pipeline (model evaluation, validation, training)
- [ ] Multi-facility collaboration (shared reference infrastructure)
- [ ] Multiple of above (specify): _______________

**Your answer:** _______________________________________________

### NuclearBench data volume:

**Current size:**
- [ ] < 10 GB (small curated reference dataset)
- [ ] 10–100 GB (moderate multi-source database)
- [ ] 100 GB–1 TB (large historical archive)
- [ ] > 1 TB (extensive multi-facility data)
- [ ] Unknown; need to assess

**Your answer:** _______________________________________________

### Growth rate (per year):

- [ ] < 10% (stable; minimal new data)
- [ ] 10–50% (regular updates; new facilities/years added)
- [ ] 50–100% (rapid; continuous new data feeds)
- [ ] > 100% (exponential; unpredictable)
- [ ] Unknown; depends on adoption

**Your answer:** _______________________________________________

---

## Question 4: NuclearBench Compute Profile

### What compute workloads will NuclearBench have?

**Workload types (check all that apply):**
- [ ] **Read-only** (queries, analysis, no processing)
- [ ] **Light processing** (validation scripts, aggregation)
- [ ] **Moderate compute** (model evaluation, benchmarking, comparison)
- [ ] **Heavy compute** (ML training, uncertainty propagation, sensitivity analysis)

**Your answer:** _______________________________________________

### Estimated compute per month:

**CPU hours:** _____ (or "minimal" / "variable; depends on campaign")

**GPU hours:** _____ (or "none")

**Peak concurrent users/jobs:** _____

**Your answer:** _______________________________________________

---

## Question 5: Integration with Neutron OS Lakehouse

### Will NuclearBench data live in the Neutron OS lakehouse?

**Integration model:**
- [ ] **Yes, fully integrated** — NuclearBench data in Iceberg Bronze/Silver/Gold
- [ ] **Yes, partial** — Some data in lakehouse; sensitive/restricted data separate
- [ ] **No, separate storage** — NuclearBench has own S3 buckets/database
- [ ] **TBD** — Waiting on data governance decision

**Your answer:** _______________________________________________

### If integrated, which components?

**Check all that apply:**
- [ ] **S3 storage** (store benchmark data in Iceberg)
- [ ] **EKS cluster** (run benchmarking jobs on shared cluster)
- [ ] **RDS PostgreSQL** (metadata, results tables, lineage)
- [ ] **Superset** (dashboards for NuclearBench results)
- [ ] **Dagster** (orchestrate validation/benchmarking workflows)
- [ ] **dbt** (transform benchmark data)

**Your answer:** _______________________________________________

---

## Question 6: Multi-Initiative Architecture Decisions

### Which components should be dedicated vs. shared?

**For each, mark Shared (S) or Dedicated (D):**

- **EKS cluster:** [ ] Shared [ ] Dedicated (per initiative)
- **S3 buckets:** [ ] Shared Iceberg [ ] Separate by initiative
- **RDS instance:** [ ] Shared [ ] Dedicated per initiative
- **Superset instance:** [ ] Shared [ ] Separate per initiative
- **Monitoring/Logging:** [ ] Shared [ ] Separate per initiative

**Your answer:** _______________________________________________

### Rationale for any dedicated components:

(E.g., "MSR needs GPU cluster; separate EKS for that"; "NuclearBench must be isolated for compliance"; etc.)

_______________________________________________

---

## Question 7: Cross-Initiative Data Flow

### How will data flow between initiatives?

**Data movement patterns (check all that apply):**
- [ ] **Pull-based** (initiatives query shared Iceberg; no data movement)
- [ ] **Push-based** (initiatives push results to shared RDS/Iceberg)
- [ ] **Event-driven** (Redpanda topics for cross-initiative notifications)
- [ ] **Batch sync** (periodic exports; minimal real-time sharing)
- [ ] **API-based** (REST/GraphQL for cross-initiative queries)
- [ ] **TBD** (data architecture still being designed)

**Your answer:** _______________________________________________

### Are there data residency or compliance constraints?

(E.g., "NuclearBench data must be separate from TRIGA"; "OffGas must be on GovCloud"; etc.)

_______________________________________________

---

## Question 8: Estimated Platform Costs

### Based on Phase 1 scope, what's the platform infrastructure footprint?

**T-shirt size (compute + storage + services combined):**
- [ ] **S (Small):** < $300/mo — Minimal lakehouse, small EKS, basic RDS
- [ ] **M (Medium):** $300–700/mo — Full lakehouse, moderate EKS, shared RDS
- [ ] **L (Large):** $700–1,200/mo — Large lakehouse, high-performance EKS, high-availability RDS
- [ ] **XL (Extra Large):** > $1,200/mo — Production-grade everything, multi-AZ, extensive monitoring
- [ ] **Unknown** (need detailed sizing)

**Your answer:** _______________________________________________

### How much of Phase 1 budget should be platform vs. initiative-specific?

(E.g., "60% platform, 40% initiatives"; "50/50 split"; etc.)

_______________________________________________

---

## Additional Context (Optional)

Anything else about platform architecture, NuclearBench, shared infrastructure, or cross-initiative integration that affects Phase 1 costs?

(E.g., "Planning to open-source NuclearBench for community use"; "Need strong data governance for sensitive reactor data"; etc.)

_______________________________________________

---

## Summary Table

| Aspect | Your Answer |
|--------|-------------|
| **Core platform components** | List checked items |
| **Shared vs. dedicated model** | Fully shared / Mostly shared / Hybrid / Mostly separate |
| **NuclearBench size** | _____ GB |
| **NuclearBench growth rate** | _____% per year |
| **Compute profile** | Light / Moderate / Heavy |
| **Isolated or integrated with lakehouse?** | Fully / Partial / Separate |
| **Platform cost estimate** | S / M / L / XL |
| **Key architecture constraint** | _____ |

---

## Thank You!

**Return to:** Ben  
**Deadline:** Friday, Feb 20, 5 PM ⚠️

(This form is self-assessment; no external review needed. Finalize architecture by Feb 20 to lock platform costs.)
