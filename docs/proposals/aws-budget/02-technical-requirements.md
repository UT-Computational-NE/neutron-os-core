---
type: proposal
section: Technical Requirements
draft: false
---

## 2. Technical Requirements

### 2.1 Compute Profile

Primary simulation codes in active use are CPU-bound, MPI-parallel applications. The optimal
AWS instance type is HPC-optimized (e.g., `hpc6a`, `hpc7g`) with high-bandwidth low-latency
interconnect for tightly coupled parallel jobs.

A secondary workload class — ML-assisted surrogate model training — benefits from GPU
instances (`p3`, `g5`) for initial training runs. GPU use is intermittent and does not require
reserved capacity.

| Workload Class | Instance Family | Typical Job Size | Typical Duration |
|----------------|-----------------|------------------|------------------|
| Monte Carlo transport | hpc6a / hpc7g | 32–256 vCPU | 2–24 hours |
| Thermal-hydraulic TH | c6i / c7i | 16–64 vCPU | 1–8 hours |
| Surrogate training | g5 / p3 | 8 vCPU + 1 GPU | 2–12 hours |
| Post-processing | t3 / m6i | 2–8 vCPU | <1 hour |

### 2.2 Storage Architecture

**Scratch (ephemeral)**: Instance store or EBS for simulation working directories.
Data retained only for job lifetime. No persistent cost.

**Results archive (S3)**: Simulation output files and QA records stored in S3 Standard
for 90 days post-job, then transitioned to S3 Glacier for long-term retention.
Estimated active dataset: 2–5 TB.

**Input data**: Nuclear data libraries and geometry files stored in S3 and mounted at
job start via S3 FUSE or pre-stage script. Libraries are read-only and shared across jobs.

### 2.3 Networking

Jobs requiring MPI communication across nodes use placement groups for low-latency
interconnect. External data transfer volume is modest (input libraries + results) — standard
data egress pricing applies.

### 2.4 Security and Compliance

- All compute runs in a VPC with no public inbound exposure.
- IAM roles scoped to minimum required S3 and EC2 permissions.
- No export-controlled technical data stored in AWS without prior review per 10 CFR 810 guidance.
- Job logs retained for 90 days per research data management policy.
