# Cost Estimation Form: Ondrej — MSR & OffGas Digital Twins

**For:** Ondrej Chvala (MSR DT, OffGas DT Lead)  
**Deadline:** Wednesday, February 26, 2026, 5 PM  
**Time to complete:** 8–10 minutes  
**Completed by:** _____________________ (Your name)

---

## Precision Expectation

Order-of-magnitude estimates (±50%) are perfect. Rough ranges beat false precision. T-shirt sizing or "I don't know" is fine—we have fallbacks.

---

## Overview

I need your help with:
- Data volumes and compute requirements for MSR Digital Twin and OffGas DT
- Simulation outputs, model training data, and real-time monitoring pipelines
- Storage and compute needs for Phase 1

**Context:** Your operational digital twin systems (MSR, OffGas) are substantial infrastructure additions. We need to understand their cloud requirements so we can size AWS correctly. (NuclearBench and Neutron OS platform architecture are covered in separate forms.)

---

## Question 1: MSR Digital Twin Data Volume & Frequency

### What's the data flow for MSR DT?

**Options:**
- [ ] **Simulation-heavy:** MPACT/SAM outputs processed nightly/weekly
- [ ] **Real-time monitoring:** Streaming sensor data + online model predictions
- [ ] **Hybrid:** Some real-time, some batch processing
- [ ] **Research-focused:** One-off simulations, not production operations

**Your answer:** _______________________________________________

### Estimated data volumes:

**MPACT/SAM simulation outputs per run:**
- [ ] < 100 MB (small domain, coarse mesh)
- [ ] 100 MB–1 GB (typical 3D core)
- [ ] 1–5 GB (high-resolution, multi-physics)
- [ ] > 5 GB (unknown; need to measure)

**Frequency of simulations in Phase 1:**
- Daily: _____ runs/day
- Weekly: _____ runs/week
- On-demand: _____ runs/month estimated

**Your answer:** _______________________________________________

### Training data for MSR models:

**Total dataset size (all historical + new data):**
- [ ] < 1 GB (small parameter studies)
- [ ] 1–10 GB (moderate historical archive)
- [ ] 10–100 GB (extensive multi-year dataset)
- [ ] > 100 GB (large-scale uncertainty quantification)

**Your answer:** _______________________________________________

---

## Question 2: OffGas Digital Twin — Streaming & Storage

### Is OffGas DT real-time monitoring or batch analysis?

- [ ] **Real-time streaming** (continuous sensor data, sub-second latency)
- [ ] **Near-real-time** (buffered streaming, minute-level updates)
- [ ] **Batch processing** (daily or weekly analysis)
- [ ] **TBD** (still designing the pipeline)

**Your answer:** _______________________________________________

### OffGas monitoring data volume:

**Sensor data rate (if streaming):**
- Number of sensors: _____
- Sampling rate: _____ Hz (or _____ measurements/second)
- Data points per sensor per day: _____ (auto-calculated or measured)

**Example:** 10 sensors × 1 Hz × 86,400 sec/day = 864,000 points/day ≈ 10 MB/day (depends on data type)

**Your answer:** _______________________________________________

### Data retention for OffGas:

- [ ] **Real-time only** (last 24 hours; older data archived)
- [ ] **1–3 months** (active monitoring window)
- [ ] **6–12 months** (compliance/historical analysis)
- [ ] **Forever** (research archive)

**Your answer:** _______________________________________________

---

## Question 3: Compute & Processing Workloads (MSR & OffGas DT)

### What's your compute profile?

- [ ] **Minimal** (queries only; < 1 hr/week compute)
- [ ] **Light** (daily batch jobs; 1–5 hrs/week)
- [ ] **Moderate** (regular simulations + training; 10–30 hrs/week)
- [ ] **Heavy** (continuous processing; 50+ hrs/week)
- [ ] **GPU-intensive** (model training, uncertainty quantification)

**Your answer:** _______________________________________________

### Estimated resource needs (per month):

**CPU hours:** _____ (or "variable; depends on simulation campaign")

**Memory requirements:** _____ GB (peak)

**GPU hours (if applicable):** _____

**Your answer:** _______________________________________________

---

## Question 4: External Dependencies & APIs

### Do you use external services?

**Check all that apply:**
- [ ] **TACC allocation** (MPACT simulations, storage)
- [ ] **Anthropic Claude API** (analysis, report generation)
- [ ] **Commercial ML services** (training, optimization)
- [ ] **Data ingestion APIs** (external sensors, public datasets)
- [ ] **None** (standalone, no external dependencies)

**Your answer:** _______________________________________________

### If TACC-dependent, what's your allocation status?

- [ ] **Active through 2027** (no urgent AWS need)
- [ ] **Ending 2026** (need AWS capacity by Q4)
- [ ] **Uncertain** (pending renewal decision)

**Your answer:** _______________________________________________

---

## Question 5: Cost Estimate & Timeline (MSR & OffGas DT)

### What cost tier makes sense for your initiatives?

- [ ] **Minimal** ($0–100/mo) — If fully TACC-dependent, archived data only
- [ ] **Moderate** ($100–300/mo) — Partial cloud integration, occasional compute
- [ ] **Significant** ($300–1,000/mo) — Regular processing, hybrid TACC/AWS
- [ ] **Major** ($1,000+/mo) — Production systems, continuous streaming, heavy compute
- [ ] **Unknown** (need to measure first)

**Your answer:** _______________________________________________

### When does Phase 1 scope lock for your systems?

- [ ] **Now** (design is set; we're implementing)
- [ ] **End of 2026** (still prototyping; Phase 1 is exploratory)
- [ ] **2027+** (not in Phase 1 budget; plan for Phase 2)

**Your answer:** _______________________________________________

---

## Question 6: Biggest Uncertainties

### What's your top blocker for sizing?

(E.g., "Don't know if we'll use AWS or stay on TACC", "Simulation scale TBD", "Sensor data volume unknown until we deploy", etc.)

_______________________________________________

---

## Additional Context (Optional)

Anything else about MSR DT, OffGas DT, NuclearBench, or architecture that affects Phase 1 sizing?

_______________________________________________

---

## Summary Table

| Aspect | Your Answer |
|--------|-------------|
| **MSR DT data volume** | _____ GB/month |
| **OffGas DT type** | Real-time / Batch / TBD |
| **Compute profile** | Light / Moderate / Heavy / GPU |
| **TACC dependency** | Active / Ending / Uncertain |
| **Cost tier estimate** | Minimal / Moderate / Significant / Major |
| **Key uncertainty** | _____ |

---

## How Your Answers Are Used

1. **Feb 26:** You provide data
2. **Feb 27:** Ben consolidates all responses (Cole, Nick, Max, Jay, Ondrej, Shayan, Dr. Clarno)
3. **Feb 28–Mar 1:** Final cost calculation using AWS Pricing Calculator
4. **Mar 2:** Submit consolidated budget to Dr. Clarno for Phase 1 approval

Your input ensures MSR DT and OffGas DT costs are visible and defensible.

---

## Questions?

Email Ben or schedule a brief call. No question is too technical—the more detail, the better the estimate.
