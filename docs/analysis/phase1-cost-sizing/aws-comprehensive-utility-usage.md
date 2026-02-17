# AWS Comprehensive Utility Usage Estimation

**Purpose:** Estimate ALL AWS service costs (not just storage), organized by service category  
**Status:** IN PROGRESS (Feb 12, 2026)  
**Scope:** NeutronOS Phase 1 (TRIGA only, 2026-2027)  
**Target Accuracy:** ±30% (typical for blue-sky estimates)

---

## Executive Summary: Service Categories

AWS charges across **9 major categories**. NeutronOS Phase 1 will use services from **all 9**:

```
1. COMPUTE (EC2, EKS, Fargate, Lambda)          → ~$200–400/mo
2. STORAGE (S3, EBS, Glacier)                   → $50–150/mo
3. DATABASE (RDS, DynamoDB, ElastiCache)       → $100–200/mo
4. ANALYTICS (Athena, Glue, Redshift)          → $50–150/mo
5. NETWORKING (Data transfer, NAT, VPN)        → $100–300/mo
6. SECURITY & COMPLIANCE (KMS, Secrets Manager)→ $20–50/mo
7. MONITORING & OBSERVABILITY (CloudWatch)     → $30–80/mo
8. DEVELOPER TOOLS (ECR, CodeBuild)            → $10–30/mo
9. MANAGEMENT & GOVERNANCE (Config, Backup)    → $20–50/mo
   ────────────────────────────────────────────────────────
   SUBTOTAL (AWS Native Services)              → $580–1,410/mo

10. EXTERNAL SERVICES (Redpanda, Claude API)    → $300–500/mo
    ────────────────────────────────────────────────────────
    TOTAL (AWS + External)                      → $880–1,910/mo
    
    With 20% contingency: $1,056–2,292/mo
```

**Key insight:** Storage is only ~5% of total cost. Compute, networking, and external services dominate.

---

## SECTION 1: COMPUTE ($200–400/mo)

### 1.1 Kubernetes (EKS) — Orchestration Layer

**What it is:**
- Managed Kubernetes service for running containers
- Hosts: Dagster (orchestration), dbt runners, Superset (BI), Flask apps, Jupyter
- Typical workload: mix of persistent services + scheduled batch jobs

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **EKS Control Plane** | per cluster | $72 | Always running; fixed cost |
| **EC2 Worker Nodes** | per node | $30–80 | Auto-scaling; 2–4 nodes typical |
| **Load Balancer** | per ALB | $16 | Entry point for Superset, Jupyter, APIs |
| **EBS Storage (node disks)** | per 100GB | $10 | Container images, ephemeral storage |
| **NAT Gateway** | per AZ | $32 | Egress for outbound traffic (see Section 5) |
| **VPC Endpoints** | per endpoint | $7 | S3, Secrets Manager private access |
| | **SUBTOTAL** | **$167–217** | |

**Questions for Cole/Nick/Jay:**
- Q1.1a: How many concurrent Superset users? (affects node size)
- Q1.1b: Peak memory for Dagster orchestration? (affects node type)
- Q1.1c: Acceptable pod startup latency? (<5sec, or >30sec OK?)

**Cost drivers:**
- If you use t3.large (general compute): $60/mo per node
- If you use c5.large (compute-optimized): $85/mo per node
- Auto-scaling between 2–4 nodes → $120–240/mo + control plane $72 = $192–312 total

---

### 1.2 Lambda (Serverless Functions) — Infrequent Tasks

**What it is:**
- Serverless compute for ad-hoc, infrequent tasks
- Use case: S3 triggers (new file ingestion), EventBridge scheduled jobs (missing data alerts)

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **Invocations** | per 1M | $0.20 | Very cheap; 1M = 1 month of hourly triggers |
| **Compute (duration)** | per 100ms | $0.0000166 | 128 MB, 100ms per run = $0.01/run |
| **Network** | per 1GB transferred | $0.09 | If Lambda talks to RDS (rare) |
| | **SUBTOTAL** | **$5–20** | |

**Questions for Jay:**
- Q1.2a: Will you use Lambda for S3 triggers, or handle in Dagster?
- Q1.2b: Expected daily triggers? (e.g., 10 new files/day = 300/month)

**Cost drivers:**
- If 100 triggers/month × $0.01 = $1
- Unlikely to be major cost driver

---

### 1.3 CloudFront (CDN) — Optional for Superset

**What it is:**
- Content Delivery Network for caching Superset dashboards
- Optional; only if you have external collaborators with high latency

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **Data transfer** | per 1GB | $0.085 | Only if using CDN |
| **Requests** | per 10K | $0.0075 | Cheap; hit caching |
| | **SUBTOTAL** | **$0 or $20–50** | |

**Questions for Nick:**
- Q1.3a: Will Superset be accessed only from UT, or external collaborators?
- Q1.3b: If external: acceptable latency, or need CDN?

**Recommendation:** Skip CloudFront for Phase 1 (internal use only).

---

**SUBTOTAL COMPUTE: $200–350/mo**

---

## SECTION 2: STORAGE ($50–150/mo)

*(Already covered in data-collection.md, but expanded here)*

### 2.1 S3 (Object Storage) — Lakehouse

**What it is:**
- Primary data store for Bronze/Silver/Gold Iceberg tables
- Also: backup destination, artifact repository

**Cost Components:**

| Component | Unit | Annual | Monthly | Notes |
|-----------|------|--------|---------|-------|
| **S3 Standard (hot, 2yr)** | per GB/mo | $2.76 | $0.023 | 150GB/yr baseline |
| **S3 Standard-IA (archive warm)** | per GB/mo | $0.12 | $0.01 | Older data, infrequent access |
| **S3 Glacier (cold, 7yr)** | per GB/mo | $0.48 | $0.004 | Long-term compliance archive |
| **S3 Intelligent-Tiering** | per 1K objects | $0.0025 | Auto-moves objects between tiers |
| **Data Transfer OUT** | per 1GB | varies | See Section 5 |
| | **SUBTOTAL** | **~$45/yr** | **~$4/mo** | |

**Questions for Cole/Nick:**
- Q2.1a: Confirmed data volume 150GB/year, or adjust?
- Q2.1b: Acceptable retrieval latency for archived data? (24h, or <5min?)

**Cost drivers:**
- Storage is cheap (~$0.023/GB/mo for hot data)
- Actual cost driven by egress (data transfer) — see Section 5

---

### 2.2 EBS (Block Storage) — Node Storage

**What it is:**
- Virtual hard drives for EKS nodes
- Attached to EC2 instances; contains container images, logs, ephemeral state

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **EBS General Purpose (gp3)** | per GB/mo | $0.10 | Typical; 100GB per node |
| **EBS-optimized throughput** | per Mbps/mo | varies | Extra for high I/O |
| | **SUBTOTAL (2-4 nodes)** | **$20–40/mo** | |

**Questions for Ops:**
- Q2.2a: Node disk space: 100GB per node sufficient?

---

### 2.3 RDS (Managed Database) — PostgreSQL

**What it is:**
- Hosted PostgreSQL database for operational data
- Stores: Gold tables, TimescaleDB for time-series, pgvector embeddings

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **Instance (db.t3.micro)** | per hour | $9 | 1 GB RAM; free tier eligible |
| **Instance (db.t3.small)** | per hour | $25 | 2 GB RAM; typical starting |
| **Instance (db.t3.medium)** | per hour | $50 | 4 GB RAM; if >100 concurrent users |
| **Storage (gp3)** | per GB/mo | $0.10 | 50–100 GB typical |
| **Backup storage** | per GB/mo | $0.023 | Auto backups (35-day retention) |
| **Data transfer (replica)** | per 1GB | $0.01 | If multi-AZ failover |
| | **SUBTOTAL** | **$40–100/mo** | |

**Questions for Jay/Nick:**
- Q2.3a: Concurrent database users? (Peak: 5? 50? 500?)
- Q2.3b: Acceptable downtime for maintenance? (single-AZ, or multi-AZ HA?)

**Cost drivers:**
- Instance size dominates; storage is secondary
- Multi-AZ HA = 2x instance cost + data transfer
- Read replicas (for scaling dashboards) = +$40–50/mo per replica

---

**SUBTOTAL STORAGE: $60–190/mo**

---

## SECTION 3: DATABASE ($100–200/mo)

*(Includes RDS from Section 2.3, plus additional options)*

### 3.1 DynamoDB (NoSQL) — Optional for Caching

**What it is:**
- Serverless NoSQL database; alternative to ElastiCache
- Use case: caching frequently-accessed data (user preferences, dashboard configs)

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **Write units (WCU)** | per 100 | $1.25 | Rarely needed; cache hits are reads only |
| **Read units (RCU)** | per 100 | $0.25 | On-demand pricing (pay per request) |
| **Storage** | per GB | $0.25 | Small tables only (~1GB) |
| | **SUBTOTAL** | **$10–30/mo** | Optional |

**Recommendation:** Skip for Phase 1. RDS is sufficient.

---

### 3.2 ElastiCache (In-Memory Cache) — Optional for Performance

**What it is:**
- Redis/Memcached for caching Superset query results, session data
- Speeds up dashboard refresh

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **cache.t3.micro (0.5GB)** | per hour | $15 | Minimal; for testing |
| **cache.t3.small (1.37GB)** | per hour | $35 | Typical for Superset caching |
| **Data transfer (same AZ)** | per 1GB | $0 | Free within AZ |
| **Data transfer (cross-AZ)** | per 1GB | $0.01 | If replication enabled |
| | **SUBTOTAL** | **$15–50/mo** | Optional |

**Questions for Nick:**
- Q3.2a: Acceptable Superset refresh time: <1s, or <10s OK?
- Q3.2b: Number of concurrent dashboard users?

**Recommendation:** Start without cache (RDS alone). Add ElastiCache if dashboards slow.

---

**SUBTOTAL DATABASE: $100–200/mo** (RDS only for Phase 1)

---

## SECTION 4: ANALYTICS & BIG DATA ($50–150/mo)

### 4.1 Athena (SQL Queries on S3)

**What it is:**
- Serverless SQL query engine running directly on S3 data
- Alternative to DuckDB for one-off analyst queries

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **Scan volume** | per 1TB scanned | $5 | Charged per GB scanned; ~$0.005/GB |
| **Data returned** | (free) | — | No additional charge |
| | **SUBTOTAL** | **$0–30/mo** | Depends on query volume |

**Questions for Researchers:**
- Q4.1a: Expected ad-hoc queries per month? (10? 50? 100?)
- Q4.1b: Typical query scope? (Single file = 100MB scan, or full year = 150GB scan?)

**Cost drivers:**
- 100 queries × 1GB avg scan = 100GB scanned = $0.50/mo (negligible)
- But if researchers run full-year scans: 100 queries × 150GB = 15TB scanned = $75/mo

---

### 4.2 Glue (ETL/Crawler)

**What it is:**
- AWS data pipeline service for discovering and cataloging data
- Use case: auto-catalog S3 files, create Athena tables

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **Crawler runs** | per DPU-hour | $0.44 | Discovering S3 schema; ~2 runs/day |
| **ETL jobs** | per DPU-hour | $0.44 | If using Glue for transformations (instead of dbt) |
| | **SUBTOTAL** | **$5–30/mo** | If used |

**Recommendation:** Skip Glue for Phase 1. Use dbt (already chosen) for transformations.

---

### 4.3 QuickSight (BI) — Alternative to Superset

**What it is:**
- AWS native BI tool; alternative to open-source Superset
- Cost: per-user licensing (annoying for research)

**Recommendation:** Skip QuickSight. Superset is already chosen (open-source).

---

**SUBTOTAL ANALYTICS: $5–30/mo** (minimal if using dbt + Superset)

---

## SECTION 5: NETWORKING ($100–300/mo) — 🚨 OFTEN OVERLOOKED

### 5.1 Data Transfer (Egress) — THE HIDDEN COST

**What it is:**
- AWS charges for data leaving AWS to the internet
- Most AWS internal transfers are free (same region, same AZ)
- Biggest cost driver after compute

**Cost Components:**

| Path | Unit | Cost | Monthly | Notes |
|------|------|------|---------|-------|
| **Internet egress** | per GB | $0.09 | TBD | Largest cost driver |
| **Cross-region** | per GB | $0.02 | $0–10 | If multi-region redundancy |
| **CloudFront → internet** | per GB | $0.085 | $0 | (not using CloudFront) |
| | **SUBTOTAL** | — | **$50–200/mo** | |

**Scenarios:**

**Scenario A: Minimal Egress (Data Stays in AWS)**
- S3 → Superset (same region): free
- RDS → Superset (same region): free
- Dagster → S3 (same region): free
- **Total egress:** ~10 GB/mo (just backups, logs) = $0.90/mo

**Scenario B: Moderate Egress (Scientists Download Data)**
- 10 researchers × 10 GB/month = 100 GB/mo = $9/mo
- Daily backups to off-region S3 (disaster recovery): 5 GB/day = 150 GB/mo = $13.50/mo
- **Total egress:** ~250 GB/mo = $22.50/mo

**Scenario C: Heavy Egress (Publishing Data, External Collaboration)**
- Research publications require data download: 500 GB/mo = $45/mo
- Daily replicas to multiple regions: 5 GB/day × 3 regions = 450 GB/mo = $40.50/mo
- External collaborators accessing dashboards: streaming tiles = 100 GB/mo = $9/mo
- **Total egress:** ~1000 GB/mo = $90/mo

**Questions for Nick/Cole:**
- Q5.1a: Will researchers download data regularly, or just query in dashboards?
- Q5.1b: Do you need multi-region replication for disaster recovery?
- Q5.1c: Will external collaborators access live dashboards, or one-time data exports?

**Cost drivers:**
- If data stays in AWS (queries only): ~$5–10/mo
- If moderate downloads: ~$20–50/mo
- If heavy external access: ~$100–200/mo

---

### 5.2 NAT Gateway — Outbound Internet Access

**What it is:**
- Allows EKS pods to reach internet (e.g., Claude API calls, Docker Hub)
- Charges for data processed + hourly fee

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **NAT Gateway (hourly)** | per hour | $32 | Per availability zone; 1 AZ = $32, 2 AZ HA = $64 |
| **Data processed** | per GB | $0.045 | Usually negligible |
| | **SUBTOTAL** | **$32–64/mo** | |

**Questions for Ops:**
- Q5.2a: Need high availability (multi-AZ NAT)? Or single NAT OK for Phase 1?

---

### 5.3 VPC Endpoints (Private Access)

**What it is:**
- Direct private connections to AWS services (S3, Secrets Manager, etc.)
- Avoid going through NAT Gateway / internet
- Cost: per endpoint, per-hour

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **S3 Gateway Endpoint** | per AZ | $7 | Free to create; charged per hour per AZ |
| **DynamoDB Gateway Endpoint** | per AZ | $7 | Free to create |
| **Secrets Manager Interface Endpoint** | per AZ | $7 | Private key access |
| | **SUBTOTAL** | **$7–30/mo** | |

**Recommendation:** Use S3 Gateway Endpoint (reduces NAT egress charges). Interface endpoints optional.

---

**SUBTOTAL NETWORKING: $100–300/mo** (depends heavily on egress patterns)

---

## SECTION 6: SECURITY & COMPLIANCE ($20–50/mo)

### 6.1 KMS (Key Management Service) — Encryption

**What it is:**
- AWS-managed encryption keys for S3, RDS, EBS, secrets
- Required for ITAR compliance (encrypted at rest)

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **Customer Master Key (CMK)** | per key | $1 | Monthly fee per key |
| **API calls** | per 10K | $0.03 | encrypt/decrypt operations |
| | **SUBTOTAL** | **$5–15/mo** | |

**Questions for Dr. Clarno:**
- Q6.1a: ITAR requires encryption at rest?

---

### 6.2 AWS Secrets Manager — Credential Management

**What it is:**
- Stores database passwords, API keys (Claude token, etc.)
- Automatically rotates credentials

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **Secrets stored** | per secret | $0.40 | E.g., 5 secrets = $2/mo |
| **API calls** | per 10K | $0.05 | Retrieving secrets; usually negligible |
| | **SUBTOTAL** | **$2–10/mo** | |

---

### 6.3 AWS Config (Compliance Monitoring)

**What it is:**
- Tracks configuration changes to AWS resources
- Useful for ITAR audit trail

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **Config recorder** | per configuration item | $0.003 | Very cheap |
| **Config rules** | per rule evaluation | $1 | ~$10/mo for 10 rules |
| | **SUBTOTAL** | **$10–20/mo** | Optional |

---

**SUBTOTAL SECURITY: $20–50/mo**

---

## SECTION 7: MONITORING & OBSERVABILITY ($30–80/mo)

### 7.1 CloudWatch (Logs & Metrics)

**What it is:**
- AWS logging service for all resources
- Stores application logs, infrastructure metrics

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **Log ingestion** | per 1GB | $0.50 | Application logs from EKS |
| **Log storage** | per 1GB/mo | $0.03 | Retention (e.g., 30 days) |
| **Metric storage** | per custom metric | $0.30 | E.g., 10 custom metrics = $3/mo |
| **Alarms** | per alarm | $0.10 | E.g., 20 alarms = $2/mo |
| | **SUBTOTAL** | **$30–80/mo** | |

**Scenarios:**

- **Minimal logging** (errors + warnings only): ~30 GB/month = $15 + $0.90 = $16/mo
- **Moderate logging** (info level): ~100 GB/month = $50 + $3 + $2 = $55/mo
- **Verbose logging** (debug): ~300 GB/month = $150 + $9 + $2 = $161/mo

**Questions for Jay:**
- Q7.1a: Preferred log level: info, debug, or errors-only?
- Q7.1b: Log retention: 7 days, 30 days, or 1 year?

**Cost drivers:**
- Log retention (7 days vs. 30 days vs. 1 year) = 4x cost difference
- Debug vs. info logging = 3x volume increase

---

### 7.2 CloudWatch Dashboards & Alarms

**What it is:**
- Custom dashboards for EKS monitoring, RDS health, pipeline status
- Alarms trigger notifications (SNS, Slack)

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **Dashboards** | per dashboard | free | First 3 free; $3 each after |
| **Alarms** | per alarm | $0.10 | Include operational, compliance alerts |
| **SNS notifications** | per 1M | $0.50 | Very cheap; minimal usage |
| | **SUBTOTAL** | **$5–20/mo** | |

---

### 7.3 X-Ray (Distributed Tracing) — Optional

**What it is:**
- Traces API requests across microservices
- Useful for debugging slow dashboards

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **Recorded traces** | per 1M | $5 | Expensive for high-volume services |
| | **SUBTOTAL** | **$0–50/mo** | Optional |

**Recommendation:** Skip X-Ray for Phase 1. Use CloudWatch alarms only.

---

**SUBTOTAL MONITORING: $40–100/mo**

---

## SECTION 8: DEVELOPER TOOLS ($10–30/mo)

### 8.1 ECR (Elastic Container Registry) — Docker Images

**What it is:**
- Private Docker image repository for custom containers (Dagster, dbt, Flask apps)
- Alternative to Docker Hub

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **Storage** | per GB/mo | $0.10 | E.g., 50 GB images = $5/mo |
| **Data transfer (pulls from EKS)** | per 1GB | free | Free within region |
| | **SUBTOTAL** | **$5–10/mo** | |

---

### 8.2 CodeBuild (CI/CD) — Optional

**What it is:**
- AWS build service for testing/deploying code
- Alternative: GitHub Actions, GitLab CI

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **Build minutes** | per minute | $0.005 | 100 builds × 10 min = 1000 min/mo = $5 |
| | **SUBTOTAL** | **$0–20/mo** | Optional |

**Recommendation:** Use GitHub Actions (free) instead of CodeBuild.

---

**SUBTOTAL DEVELOPER TOOLS: $5–10/mo**

---

## SECTION 9: MANAGEMENT & GOVERNANCE ($20–50/mo)

### 9.1 AWS Backup (Automated Backups)

**What it is:**
- Automated backup of RDS, EBS, S3
- Enforces backup policies (daily, weekly, monthly, yearly)

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **Backup storage** | per GB/mo | $0.05 | E.g., 100 GB backups = $5/mo |
| **Backup jobs** | per job | free | No charge for runs |
| | **SUBTOTAL** | **$5–20/mo** | |

**Questions for Ops:**
- Q9.1a: Backup retention: 30 days, 1 year, or 7 years?
- Q9.1b: Multi-region replication (disaster recovery)?

---

### 9.2 AWS Cost Explorer & Budget Alerts

**What it is:**
- Monitoring tool for actual AWS spend
- Free to use; helps prevent bill shock

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **Cost Explorer** | per month | free | Built-in |
| **Budget alerts** | per budget | free | Built-in |
| | **SUBTOTAL** | **$0** | |

---

### 9.3 Service Quotas Monitoring

**What it is:**
- Prevents hitting account limits (e.g., max 20 RDS instances)

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **Quota monitoring** | per account | free | Built-in |
| | **SUBTOTAL** | **$0** | |

---

**SUBTOTAL MANAGEMENT: $5–20/mo**

---

## SECTION 10: EXTERNAL SERVICES ($300–500/mo)

### 10.1 Redpanda Cloud (Event Streaming)

**What it is:**
- Managed Kafka alternative for PiXie data streaming

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **Base tier** | per month | $150 | Included: 100K events/sec |
| **Additional throughput** | per 10K events/sec | $50 | If PiXie exceeds 100K/sec |
| | **SUBTOTAL** | **$150–300/mo** | If PiXie included |

**Scenarios:**
- **PiXie excluded (Phase 2):** $0
- **PiXie Phase 1, light:** $150/mo
- **PiXie Phase 1, heavy:** $250–300/mo

---

### 10.2 Claude API (LLM Inference)

**What it is:**
- Anthropic Claude for RAG queries, agents, text processing

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **Input tokens** | per 1M | $3 | Prompt text |
| **Output tokens** | per 1M | $15 | Generated response |
| | **SUBTOTAL** | **$100–400/mo** | Depends on query volume |

**Scenarios:**

**Scenario A: Light Usage (10 RAG queries/day)**
- Avg prompt: 5K tokens = 150K/mo × $0.003 = $0.45
- Avg response: 500 tokens = 150K/mo × $0.015 = $2.25
- **Subtotal:** ~$2.70/mo

**Scenario B: Moderate Usage (100 RAG queries/day)**
- Prompts: 1.5M tokens/mo × $0.003 = $4.50
- Responses: 1.5M tokens/mo × $0.015 = $22.50
- **Subtotal:** ~$27/mo

**Scenario C: Heavy Usage (Research Assistant used constantly)**
- Prompts: 10M tokens/mo × $0.003 = $30
- Responses: 10M tokens/mo × $0.015 = $150
- **Subtotal:** ~$180/mo

**Questions for Researchers:**
- Q10.2a: How many RAG queries/day? (10? 100? 500?)
- Q10.2b: Typical query scope? (1 doc, or search 1000s of docs?)

**Cost drivers:**
- Input (prompt) tokens = search scope (10 docs vs. 1000 docs = 100x cost)
- Output (response) tokens = response length (short summary vs. detailed analysis)

---

### 10.3 OpenAI API (Embeddings) — Optional

**What it is:**
- Embedding API for RAG (text-embedding-ada-002)
- One-time cost to embed documents + recurring for new docs

**Cost Components:**

| Component | Unit | Monthly | Notes |
|-----------|------|---------|-------|
| **Embedding API** | per 1K tokens | $0.00002 | E.g., 10M tokens/month = $0.20 |
| **One-time (1000 docs)** | — | — | ~$1–2 one-time |
| | **SUBTOTAL** | **$0–20/mo** | Minimal |

**Note:** Can use local embeddings (Ollama on EKS) instead → $0/mo but uses compute.

---

**SUBTOTAL EXTERNAL: $300–500/mo**

---

## SECTION 11: HIDDEN COSTS & CONTINGENCY ($100–200/mo)

### 11.1 Things You Forgot

| Item | Est. Monthly | Notes |
|------|---|---|
| **Support plan** | $0–100 | AWS Business support = $100/mo (optional) |
| **Training/consulting** | $0–500 | Architect for compliance, ITAR review |
| **Tools not yet scoped** | $0–100 | New monitoring tool, database optimization, etc. |

---

### 11.2 20% Contingency for Unknown Unknowns

Expected range: $880–1,910/mo  
With 20% contingency: **$1,056–2,292/mo**

---

## COMPREHENSIVE COST TABLE: ALL SERVICES

| Service Category | Service | Est. Monthly | Notes |
|---|---|---|---|
| **COMPUTE** | EKS | $167–217 | Control plane + nodes |
| | Lambda | $5–20 | S3 triggers, ad-hoc tasks |
| | CloudFront | $0 | Skip for Phase 1 |
| | **Subtotal** | **$172–237** | |
|  | |  | |
| **STORAGE** | S3 | $4–50 | Hot + archive tiers |
| | EBS | $20–40 | Node disks |
| | **Subtotal** | **$24–90** | |
|  | |  | |
| **DATABASE** | RDS PostgreSQL | $40–100 | Instance + backups |
| | ElastiCache | $0–50 | Skip unless dashboard slow |
| | DynamoDB | $0–30 | Skip for Phase 1 |
| | **Subtotal** | **$40–180** | |
|  | |  | |
| **ANALYTICS** | Athena | $0–30 | Ad-hoc queries |
| | Glue | $0–30 | Skip; use dbt instead |
| | **Subtotal** | **$0–60** | |
|  | |  | |
| **NETWORKING** | Data transfer (egress) | $5–200 | Highest variance; depends on download patterns |
| | NAT Gateway | $32–64 | Outbound internet access |
| | VPC Endpoints | $7–30 | Private access to AWS services |
| | **Subtotal** | **$44–294** | |
|  | |  | |
| **SECURITY** | KMS | $5–15 | Encryption keys |
| | Secrets Manager | $2–10 | Credential storage |
| | AWS Config | $0–20 | Compliance monitoring (optional) |
| | **Subtotal** | **$7–45** | |
|  | |  | |
| **MONITORING** | CloudWatch | $30–80 | Logs, metrics, dashboards |
| | X-Ray | $0–50 | Skip for Phase 1 |
| | **Subtotal** | **$30–130** | |
|  | |  | |
| **DEVELOPER** | ECR | $5–10 | Docker image registry |
| | CodeBuild | $0–20 | Skip; use GitHub Actions |
| | **Subtotal** | **$5–30** | |
|  | |  | |
| **MANAGEMENT** | AWS Backup | $5–20 | Backup storage |
| | Cost Explorer | $0 | Free |
| | Service Quotas | $0 | Free |
| | **Subtotal** | **$5–20** | |
|  | |  | |
| **EXTERNAL** | Redpanda Cloud | $0–300 | $150 if PiXie Phase 1 |
| | Claude API | $100–400 | Depends on RAG usage |
| | OpenAI Embeddings | $0–20 | Minimal |
| | **Subtotal** | **$100–720** | |
|  | |  | |
| **CONTINGENCY (20%)** | — | **$150–330** | Unknown unknowns |
|  | |  | |
| **TOTAL MONTHLY** | — | **$580–2,100** | |
| **TOTAL ANNUAL (2026, 9mo)** | — | **$5,220–18,900** | |
| **TOTAL ANNUAL (2027, 12mo)** | — | **$6,960–25,200** | |

---

## THREE SCENARIOS: COMPREHENSIVE MONTHLY COSTS

### Scenario A: Minimal (PiXie excluded, conservative approach)

| Category | Cost |
|---|---|
| Compute (EKS) | $200 |
| Storage | $50 |
| Database (RDS micro) | $40 |
| Analytics | $10 |
| Networking (minimal egress) | $50 |
| Security & Monitoring | $50 |
| Developer + Management | $10 |
| External (Claude only, light usage) | $100 |
| **Subtotal** | **$510** |
| Contingency (20%) | $102 |
| **TOTAL** | **$612/mo** |

**2026 (9mo):** $5,508  
**2027 (12mo):** $7,344

---

### Scenario B: Recommended (PiXie Phase 1, balanced)

| Category | Cost |
|---|---|
| Compute (EKS, 3 nodes) | $250 |
| Storage | $75 |
| Database (RDS small) | $75 |
| Analytics | $20 |
| Networking (moderate egress) | $100 |
| Security & Monitoring | $60 |
| Developer + Management | $15 |
| External (Redpanda + Claude) | $350 |
| **Subtotal** | **$945** |
| Contingency (20%) | $189 |
| **TOTAL** | **$1,134/mo** |

**2026 (9mo):** $10,206  
**2027 (12mo):** $13,608

---

### Scenario C: Full Cloud (AWS primary, high-availability)

| Category | Cost |
|---|---|
| Compute (EKS, 4 nodes, multi-AZ) | $350 |
| Storage (multi-region backups) | $150 |
| Database (RDS multi-AZ, read replica) | $150 |
| Analytics | $50 |
| Networking (heavy egress, cross-region) | $250 |
| Security & Monitoring | $100 |
| Developer + Management | $30 |
| External (Redpanda premium + Claude heavy) | $600 |
| **Subtotal** | **$1,680** |
| Contingency (20%) | $336 |
| **TOTAL** | **$2,016/mo** |

**2026 (9mo):** $18,144  
**2027 (12mo):** $24,192

---

## KEY INSIGHTS: WHERE COSTS ACTUALLY GO

Based on this comprehensive analysis:

1. **Storage is cheap** (~$50–150/mo)
   - Most of "storage cost" is actually S3 egress (data transfer)

2. **Compute is significant** (~$200–350/mo)
   - EKS control plane ($72) + nodes ($100–250) dominates
   - Node count & size drive 80% of compute cost

3. **External services are expensive** (~$300–600/mo)
   - Redpanda Cloud ($150–300) if PiXie included
   - Claude API ($100–400) if heavy RAG usage
   - These are often hidden costs not counted in "AWS bill"

4. **Networking is surprisingly expensive** (~$100–250/mo)
   - Data egress (people downloading data) = $5–200/mo
   - NAT Gateway = $32–64/mo flat
   - Can easily become largest cost if researchers download terabytes

5. **Monitoring/observability matters** (~$30–100/mo)
   - CloudWatch logs retention drives this
   - Debug logging = 3x cost of info logging

---

## NEXT QUESTIONS FOR DATA COLLECTION

**Update aws-cost-estimate-data-collection.md Section A-E with these:**

### For Cole (Physics):
- Q New: Any high-volume data downloads or publishing requirements? (affects egress cost)

### For Nick (Operations):
- Q New: Will external collaborators access dashboards, or just UT staff?
- Q New: Acceptable log retention: 7 days, 30 days, or 1 year?

### For Max (PiXie):
- Q New: PiXie data retention: keep raw, or compress after N days? (affects storage growth)

### For Jay (ML/Data):
- Q New: Expected Claude API usage: light (10 queries/day), moderate (100/day), or heavy (500+/day)?
- Q New: Debug or info-level logging for Dagster pipelines?

### For Dr. Clarno (Approval):
- Q New: Multi-region disaster recovery needed, or single-region acceptable?
- Q New: AWS Business support ($100/mo for priority support) or Developer support?

---

## UPDATING THE COST COLLECTION WORKSHEET

Expand **Section A-E** of `aws-cost-estimate-data-collection.md` with these utility categories. Update **Section F (Cost Calculation Framework)** to include all 9 AWS service categories + external services.

