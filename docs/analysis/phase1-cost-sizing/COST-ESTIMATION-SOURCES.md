# Cost Estimation Sources & Tools Reference

**Quick guide to where every cost number comes from and what tools we use**

Created: February 12, 2026  
For: Stakeholders completing cost data collection

---

## TL;DR — The Five Tools We Use

| Tool | Purpose | When | How It Works |
|------|---------|------|---|
| **AWS Pricing Calculator** | Verify specific service configurations | Feb 17–18 | Input node count, storage size, region → get monthly cost |
| **AWS Cost Explorer** | Track actual spending after launch | Feb 2026+ (monthly) | Compare estimated vs. actual costs; spot anomalies |
| **cost_estimation_tool** | Automate cost calculations | Feb 17 | Load stakeholder responses → run Python calculator → get costs |
| **AWS Pricing Pages** | Source truth for unit prices | Ongoing (3-month validity) | Look up $0.023/GB for S3, $72/mo for EKS, etc. |
| **External Service Pricing** | Redpanda, Claude API rates | Ongoing | Check https://redpanda.com/pricing and https://www.anthropic.com/pricing |

---

## The Three Layers of Cost Information

### Layer 1: Base Unit Prices (Tier 1: Official AWS)

These are the "raw material" prices from AWS, Redpanda, Anthropic.

**Example: S3 Storage**
```
AWS Pricing Page: https://aws.amazon.com/s3/pricing/
Current Rate (Feb 12, 2026): S3 Standard = $0.023/GB/month
This price is updated continuously by AWS; we assume it's current within ±5%
```

**Example: EKS Control Plane**
```
AWS Pricing Page: https://aws.amazon.com/eks/pricing/
Current Rate (Feb 12, 2026): $0.10/hour = $73/month per cluster
Fixed cost; doesn't change with cluster size
```

**Example: Claude API**
```
Anthropic Pricing Page: https://www.anthropic.com/pricing
Current Rates (Feb 12, 2026):
  - Input tokens: $3 per 1M tokens
  - Output tokens: $15 per 1M tokens
```

### Layer 2: Assumptions (Our Responsibility)

We turn unit prices into monthly costs by making assumptions about **usage patterns**.

**Example: S3 Storage Assumption**
```
Unit Price: $0.023/GB/month (from AWS)
Our Assumption: 150 GB/year data volume
  - Baseline from Jay's estimate (ZOC CSVs + MPACT outputs)
  - 2-year hot retention (S3 Standard)
  - 5-year cold retention (S3 Glacier)

Calculation:
  Hot storage:   (150 GB/yr ÷ 365 days) × 2 years × $0.023/GB = $0.019/month
  Cold storage:  (150 GB/yr ÷ 365 days) × 5 years × $0.004/GB = $0.008/month
  Total baseline: $0.027/month

But if PiXie adds 100 GB/day: 100 × 365 = 36,500 GB/yr additional
  → This changes everything!
```

**Example: EKS Compute Assumption**
```
Unit Prices:
  - EKS Control Plane: $72/month (fixed)
  - t3.large on-demand: $0.1104/hour = $80/month per node

Our Assumptions:
  - Number of nodes: 2 (default), 3 (recommended), 4 (full cloud)
  - Justification: Operating hours/week (from Nick)
    80 hrs/week operating → ~20% utilization → 2–3 nodes sufficient

Calculation:
  Minimal:      EKS ($72) + nodes ($80×2) + ALB ($16) + ... = $167/mo compute
  Recommended:  EKS ($72) + nodes ($80×3) + ALB ($16) + ... = $250/mo compute
  Full Cloud:   EKS ($72) + nodes ($90×4) + ALB ($32) + ... = $350/mo compute
```

### Layer 3: Aggregation (Our Responsibility)

We combine all 9 AWS services + 3 external services into monthly/annual totals.

**Example: Recommended Scenario**
```
Compute:           $250/mo
Storage:           $75/mo
Database:          $75/mo
Analytics:         $20/mo
Networking:        $100/mo
Security:          $60/mo
Monitoring:        $60/mo
Developer Tools:   $15/mo
Management:        $8/mo
─────────────────────────
AWS Subtotal:      $663/mo

External Services: $350/mo  (Redpanda $200 + Claude API $150)
─────────────────────────
Total Subtotal:    $1,013/mo
Contingency (20%): $203/mo
─────────────────────────
TOTAL:             $1,134/mo
```

---

## Source Map: Every Cost Has a Reason

### Compute Costs

| Cost Item | Unit Price | Source | Assumption | Formula | Monthly Cost |
|-----------|-----------|--------|-----------|---------|---|
| EKS Control Plane | $0.10/hr | https://aws.amazon.com/eks/pricing/ | 1 cluster, always on | 730 hrs × $0.10 | $73 |
| t3.large Node | $0.1104/hr | https://aws.amazon.com/ec2/pricing/on-demand/ | 2–4 nodes (depends on scenario) | 730 hrs × $0.1104 × num_nodes | $80–320 |
| Load Balancer | $0.0219/hr | https://aws.amazon.com/elasticloadbalancing/pricing/ | 1 ALB, always on | 730 hrs × $0.0219 | $16 |
| NAT Gateway | $0.045/hr | https://aws.amazon.com/vpc/pricing/ | 1 per AZ (single or multi) | 730 hrs × $0.045 × num_az | $32–64 |

### Storage Costs

| Cost Item | Unit Price | Source | Assumption | Formula | Monthly Cost |
|-----------|-----------|--------|-----------|---------|---|
| S3 Standard | $0.023/GB/mo | https://aws.amazon.com/s3/pricing/ | 150 GB/yr baseline, 2yr hot | (150÷365)×2×0.023 | $0.02 + PiXie data |
| S3 Glacier | $0.004/GB/mo | https://aws.amazon.com/s3/pricing/ | 150 GB/yr baseline, 5yr cold | (150÷365)×5×0.004 | $0.01 + PiXie data |
| Data Egress | $0.09/GB | https://aws.amazon.com/ec2/pricing/data-transfer/ | 50–200 GB/mo (moderate scenario) | 50–200 × $0.09 | $5–18 |

### Database Costs

| Cost Item | Unit Price | Source | Assumption | Formula | Monthly Cost |
|-----------|-----------|--------|-----------|---------|---|
| RDS PostgreSQL (t3.small) | $0.104/hr | https://aws.amazon.com/rds/pricing/ | 1 instance, always on | 730 hrs × $0.104 | $76 |
| RDS Multi-AZ premium | 2× | https://aws.amazon.com/rds/pricing/ | Single-AZ (Phase 1) | N/A for Phase 1 | $0 |

### External Services

| Service | Unit Price | Source | Assumption | Formula | Monthly Cost |
|---------|-----------|--------|-----------|---------|---|
| Redpanda Cloud | $150 base + $50/10K events/sec above 100K/sec | https://redpanda.com/pricing | PiXie Phase 1 = ~10K events/sec | $150 (base only) | $150–300 |
| Claude API | $3 per 1M input, $15 per 1M output | https://www.anthropic.com/pricing | 10 queries/day × 5K input + 500 output tokens | (150K×3 + 15K×15)÷1M | $0.68/10-queries/day |

---

## How We'll Verify These Numbers

### Method 1: AWS Pricing Calculator (Official Verification)

**When:** Feb 17–18  
**How:** Input exact configuration, let calculator compute costs

```
1. Go to https://calculator.aws/
2. Add services:
   - EKS: 1 cluster, 2–4 t3.large nodes, US East 1
   - S3: 150 GB/month of storage (adjust for PiXie)
   - RDS: 1 × t3.small PostgreSQL, Multi-AZ off
   - [etc. for all 9 services]
3. Calculator outputs: $XXX/month
4. Compare to our estimate: variance should be <5%
5. Export as JSON; attach to cost report
```

### Method 2: Cross-Check Against Known Workloads

**When:** After Phase 1 launches  
**How:** Find similar AWS customer (case study) + compare

```
Example: AWS case study - "Genomics Research on EKS"
  - Similar: 2–4 nodes, moderate data volume, RDS database
  - Their cost: $800–1,200/month for similar workload
  - Our estimate: $1,134/month (recommended scenario)
  - Variance: +5% (within tolerance)
  - Conclusion: Estimate seems reasonable
```

### Method 3: AWS Cost Explorer (Real Data)

**When:** Feb 2026 onwards (monthly)  
**How:** Activate cost tracking; compare to estimate

```
February 2026 (1 month actual data):
  Estimated (from this analysis): $1,134
  Actual (from Cost Explorer):    $1,180
  Variance:                        +4% ✓ (within contingency)

March 2026:
  Estimated: $1,134
  Actual:    $1,210
  Variance:  +6.7% → investigate why

If variance > 10% two months in a row:
  → Root cause analysis
  → Adjust assumptions for remaining 10 months
  → Update Phase 2 estimate
```

---

## Confidence Levels

### High Confidence (±5%)

These costs are **stable** and well-understood:
- ✅ EKS control plane ($72/mo flat cost)
- ✅ RDS instance pricing (published hourly rates)
- ✅ S3 storage tiers (commodity pricing, rarely changes)
- ✅ NAT Gateway ($32/mo per AZ, fixed)
- ✅ Data transfer egress (published per GB; occasional decreases)

**Action:** Use these as-is in estimate

### Medium Confidence (±15%)

These costs **depend heavily on assumptions** we make:
- ⚠️ EKS worker node count (depends on operating hours)
- ⚠️ Data egress volume (depends on external access patterns)
- ⚠️ CloudWatch log ingestion (depends on logging verbosity)
- ⚠️ Claude API usage (depends on RAG query volume)

**Action:** Get stakeholder estimates for assumptions; sensitivity test

### Low Confidence (±30%)

These costs have **high uncertainty** until we have real data:
- ❓ PiXie data volume (not yet operational in Phase 1)
- ❓ Redpanda throughput tier (depends on PiXie stream characteristics)
- ❓ Storage growth rate (depends on operational scale)

**Action:** Use pre-defined scenarios (minimal/recommended/full-cloud); flag as risk

---

## What Changes Over Time?

### Stable (Won't Change)
- ✅ EKS control plane cost ($72/mo): AWS hasn't changed this since 2019
- ✅ Unit pricing structure: S3 Standard tier pricing model stable
- ✅ NAT Gateway: $32/mo per AZ (stable for 5+ years)

### Occasionally Change (Quarterly Reviews)
- 📈 EC2 instance prices: AWS adjusts rates ~2x/year based on competition
- 📈 S3 pricing: Rarely changes; usually decreases with scale
- 📈 Regional pricing: New regions sometimes cheaper
- 📊 External service pricing: Redpanda, Anthropic may adjust

**Action:** Quarterly pricing reviews (Feb → May → Aug → Nov)

### Will Change (By Design)
- 🔄 PiXie data volume: Unknown until Phase 1 actually runs
- 🔄 Log volume: Depends on debug vs. info logging decision
- 🔄 Egress patterns: Depends on external collaboration scope
- 🔄 Claude API usage: Depends on RAG adoption

**Action:** Monitor Cost Explorer; re-estimate if assumption changes by >20%

---

## Reference URLs (Always Current)

**AWS (Tier 1 Sources):**
- https://aws.amazon.com/eks/pricing/
- https://aws.amazon.com/ec2/pricing/on-demand/
- https://aws.amazon.com/s3/pricing/
- https://aws.amazon.com/rds/pricing/
- https://aws.amazon.com/cloudwatch/pricing/
- https://aws.amazon.com/ec2/pricing/data-transfer/
- https://aws.amazon.com/vpc/pricing/
- https://calculator.aws/ (for manual verification)

**External Services:**
- https://redpanda.com/pricing (Streaming)
- https://www.anthropic.com/pricing (Claude API)
- https://openai.com/api/pricing (OpenAI Embeddings)

**Related NeutronOS Documents:**
- [aws-cost-estimation-methodology.md](aws-cost-estimation-methodology.md) — Detailed tool mapping
- [aws-comprehensive-utility-usage.md](aws-comprehensive-utility-usage.md) — Full 9-service breakdown
- [aws-cost-estimate-data-collection.md](aws-cost-estimate-data-collection.md) — Stakeholder questionnaire

---

## For Finance/Approval Teams

If you need to verify these estimates:

1. **Check AWS Pricing Calculator** (https://calculator.aws/)
   - Input the configuration we describe
   - Compare output to our estimate
   - Variance should be ±10%

2. **Review Data Collection Worksheet** (aws-cost-estimate-data-collection.md)
   - See where assumptions come from
   - Check if assumptions are reasonable

3. **Ask for Cost Explorer Dashboard** (Feb 2026+)
   - Once infrastructure is live, activate AWS Cost Explorer
   - Run monthly reports showing actual vs. estimated
   - Investigate variances >10%

4. **Read Technical Justification** (aws-cost-estimate-justification.md, to be created)
   - Why each service is necessary
   - References to PRDs/ADRs supporting design

---

## Key Takeaways for Stakeholders

✅ **Your answers drive costs.** The data collection questions directly map to cost inputs.

✅ **All prices are sourced.** Every unit price traces back to official AWS/external service pricing pages.

✅ **We have contingency.** 20% built into all estimates for unknowns.

✅ **We'll track actuals.** After launch, we'll compare estimated vs. actual using AWS Cost Explorer.

✅ **Questions are designed for tools.** Each question feeds into AWS Pricing Calculator or cost_estimation_tool.

---

**Questions?** See [aws-cost-estimation-methodology.md](aws-cost-estimation-methodology.md) for detailed explanation of each assumption.
