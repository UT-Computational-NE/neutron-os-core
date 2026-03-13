---
type: proposal
section: Budget Justification
draft: false
data-sources:
  - assets/cost-model.csv
---

## 3. Budget Justification

### 3.1 Methodology

Cost estimates are derived from a 12-month historical profile of simulation jobs run on
the on-campus cluster, translated to equivalent AWS instance-hours. The mapping uses
published AWS HPC pricing for `us-east-2` (Ohio) region, which provides the best
price-performance for academic HPC workloads.

The cost model source file is tracked for provenance: `assets/cost-model.csv`.
Any change to the model after this document is published will be flagged by
`neut pub status` as a data source change.

### 3.2 Annual Compute Estimate

| Workload | Annual Instance-Hours | Est. Cost (on-demand) | Est. Cost (Spot, 70% savings) |
|----------|-----------------------|----------------------|-------------------------------|
| Monte Carlo transport | ~2,400 | — | — |
| Thermal-hydraulic TH | ~800 | — | — |
| Surrogate training | ~200 | — | — |
| Post-processing / misc | ~400 | — | — |
| **Total** | **~3,800** | *see cost-model.csv* | *see cost-model.csv* |

> Exact dollar figures are maintained in `assets/cost-model.csv` and updated as AWS pricing
> changes. The table above reflects instance-hour estimates only; dollar amounts are
> computed from the model at time of submission.

### 3.3 Spot vs. On-Demand Strategy

Simulation workloads are checkpoint-tolerant: codes write restart files at configurable
intervals. This makes them excellent candidates for Spot instances, which are typically
60–70% cheaper than on-demand. The estimated budget accounts for a mixed fleet:
~80% Spot (fault-tolerant batch jobs) and ~20% on-demand (time-sensitive interactive
or non-checkpointed runs).

### 3.4 Storage Cost

S3 Standard for active results (~3 TB average): estimated at current S3 Standard pricing.
Glacier transition after 90 days reduces ongoing retention cost substantially for archival data.

### 3.5 Total 12-Month Budget Request

| Category | Basis | Notes |
|----------|-------|-------|
| Compute (Spot + On-demand) | cost-model.csv | Mixed fleet, checkpoint-tolerant |
| Storage (S3 + Glacier) | 3 TB active + archive | 90-day S3, then Glacier |
| Data transfer egress | Nominal | Input libraries + results |
| Support (Standard) | Flat rate | PI team manages |

*Final dollar totals to be confirmed from cost-model.csv at submission time.*
