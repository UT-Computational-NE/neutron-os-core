---
type: proposal
section: Timeline and Milestones
draft: false
---

## 4. Timeline and Milestones

### 4.1 Activation Plan

| Phase | Timeframe | Activity |
|-------|-----------|----------|
| **Setup** | Month 1 | VPC provisioning, IAM role setup, S3 bucket configuration, job submission tooling |
| **Pilot** | Month 2 | Run existing benchmark suite on AWS; validate cost model against actuals |
| **Active Use** | Months 3–10 | Simulation campaigns tied to grant deliverables (see §1.1) |
| **Review** | Month 11 | Review actual vs. estimated costs; adjust Spot/on-demand mix |
| **Reporting** | Month 12 | Usage summary for grant reports and renewal planning |

### 4.2 Deliverable Dependencies

The following funded deliverables have explicit compute requirements that this allocation supports:

| Deliverable | Target Date | Compute Dependency |
|-------------|-------------|-------------------|
| UQ study — fuel performance | Month 4 | 1,200 Monte Carlo runs (~600 instance-hours) |
| Safety analysis report | Month 6 | Coupled TH/neutronics campaign (~300 instance-hours) |
| Surrogate model v1 | Month 8 | GPU training run (~50 instance-hours) |
| Digital twin validation | Month 10 | High-fidelity benchmark suite (~800 instance-hours) |

### 4.3 Cost Governance

- Monthly AWS Cost Explorer review by PI and research computing admin.
- Automated billing alert at 80% of monthly allocation.
- Spot interruption rate reviewed at Month 3; on-demand fraction adjusted if needed.
- Final utilization report delivered with Month 12 grant progress report.
