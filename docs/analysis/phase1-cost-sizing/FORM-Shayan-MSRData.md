# Cost Estimation Form: Shayan — MSR Chemistry & Digital Twin Data

**For:** Shayan Shahbazi (MSR Chemistry / Digital Twin Postdoc)  
**Deadline:** Wednesday, February 26, 2026, 5 PM  
**Time to complete:** 5–10 minutes  
**Completed by:** _____________________ (Your name)

---

## Precision Expectation

Order-of-magnitude estimates (±50%) are perfect. Rough ranges beat false precision. T-shirt sizing or "I don't know" is fine—we have fallbacks.

---

## Overview

I need your help with:
- Training and validation datasets for MSR chemistry models (thermochemistry, kinetics, corrosion)
- Real-time sensor data from molten salt monitoring systems (if Phase 1 includes live facility data)
- Simulation output storage and archival (MPACT/SAM + chemistry-specific outputs)
- Data pipeline compute requirements for chemistry model training and validation

**Context:** You're building MSR chemistry expertise for the digital twin. We need to understand your data infrastructure needs (training datasets, validation pipelines, monitoring sensors) so AWS sizing is accurate for Phase 1.

---

## Question 1: Training Data for MSR Chemistry Models

### What datasets are you using to build MSR chemistry models?

**Data sources (check all that apply):**
- [ ] Historical MSR operational data (ORNL, INL facility records; chemistry/composition logs)
- [ ] MPACT/SAM simulation outputs + chemistry sub-model data (thermochemistry, salt behavior)
- [ ] Parameter sweeps / uncertainty quantification (corrosion rates, salt properties)
- [ ] Experimental measurements (kinetics tests, salt composition analysis, corrosion coupons)
- [ ] Thermochemistry databases (NIST, other published salt chemistry)
- [ ] Custom-generated synthetic data (kinetic simulations, phase diagrams)

**Your answer:** _______________________________________________

### Total training dataset size:

- [ ] < 1 GB (small curated dataset)
- [ ] 1–10 GB (moderate multi-source dataset)
- [ ] 10–50 GB (extensive historical archive)
- [ ] 50–100 GB (very large uncertainty quantification)
- [ ] > 100 GB (unknown; need to measure)

**Your answer:** _______________________________________________

### Is this data growing over time?

- [ ] **Static** (training set locked, not updated)
- [ ] **Slow growth** (minor additions; < 10 GB/year)
- [ ] **Steady growth** (regular updates; 10–50 GB/year)
- [ ] **Rapid growth** (continuous ingestion; > 50 GB/year)

**Your answer:** _______________________________________________

---

## Question 2: Chemistry Model Training & Compute

### How often do you retrain MSR chemistry models (thermochemistry, kinetics, corrosion)?

- [ ] **One-time** (Phase 1 is training only; no retraining)
- [ ] **Occasional** (retraining once or twice per year)
- [ ] **Regular** (monthly or quarterly retraining)
- [ ] **Continuous** (online learning, updating as new data arrives)

**Your answer:** _______________________________________________

### Estimated compute per training run:

**Wall-clock time:**
- Hours per run: _____ (or minutes: _____)

**Resources:**
- CPU cores: _____ (or "unknown")
- Memory (GB): _____ (peak during chemistry model training)
- GPU required? (yes/no): _____ (typical for thermochemistry UQ)
- GPU type (if yes): _____ (e.g., NVIDIA A100, V100 for kinetic/uncertainty propagation)

**Your answer:** _______________________________________________

### Total compute in Phase 1 (Feb–Dec 2026):

**Estimate:**
- How many retraining runs: _____
- Total CPU hours: _____ (auto-calculated or measured)
- Total GPU hours: _____ (or none)

**Your answer:** _______________________________________________

---

## Question 3: Chemistry Model Validation & Testing

### Do you have a validation/testing pipeline for chemistry models?

**Validation types:**
- [ ] **No** (training only; compare against literature/prior work manually)
- [ ] **Light** (occasional validation against experimental data; spot checks)
- [ ] **Regular** (weekly/monthly validation runs with new facility data or literature)
- [ ] **Continuous** (automated testing as new salt chemistry or kinetic data arrives)

**Your answer:** _______________________________________________

### Validation datasets:

**Validation data size/source:**
- [ ] Shared with training set (same chemistry data, cross-validation splits)
- [ ] Separate held-out experimental data (_____ GB; corrosion tests, salt analysis, thermal logs)
- [ ] External published datasets (size: _____; thermochemistry literature, ORNL/INL benchmarks)
- [ ] Unknown; depends on data availability

**Your answer:** _______________________________________________

---

## Question 4: Chemistry Simulation Outputs & Storage

### How much chemistry simulation data do you generate?

**Per MPACT/SAM + chemistry sub-model run:**
- [ ] < 100 MB (coarse-grain thermochemistry)
- [ ] 100 MB–1 GB (detailed kinetics, multi-phase tracking)
- [ ] 1–5 GB (high-resolution, uncertainty quantification with 1000s of samples)
- [ ] > 5 GB (ensemble kinetics, corrosion propagation simulations)

**Frequency:**
- Runs per week: _____ (or per month)
- Total runs in Phase 1 (Feb–Dec): _____ estimated

**Total storage needed:** _____ GB

**Your answer:** _______________________________________________

### How long should chemistry simulation outputs be kept (for validation/comparison)?

- [ ] **Short-term** (1–2 weeks; just for active analysis)
- [ ] **Medium-term** (1–3 months)
- [ ] **Long-term** (6–12 months; historical reference)
- [ ] **Forever** (research archive, never delete)

**Your answer:** _______________________________________________

### After initial storage, archive or delete?

- [ ] Archive to cold storage (S3 Glacier; occasional access)
- [ ] Delete (data not needed long-term)
- [ ] Keep in hot storage (expensive but needed for active research)

**Your answer:** _______________________________________________

---

## Question 5: Real-Time Chemistry Monitoring (If Phase 1 Includes Live Data)

### Will MSR DT include real-time molten salt monitoring?

**Monitoring scope:**
- [ ] **No** (research-only; use historical data + simulations, no live facility)
- [ ] **Planned but not Phase 1** (design phase; data collection starts 2027)
- [ ] **Yes, limited** (pilot: 1–2 chemistry sensors; e.g., salt composition, temperature)
- [ ] **Yes, full** (comprehensive: multiple chemistry sensors + corrosion probes + thermal logging)

**Your answer:** _______________________________________________

### If yes, chemistry monitoring data volume:

**Chemistry sensors:**
- Salt composition sensors: _____
- Corrosion/redox monitoring probes: _____
- Thermal/kinetic rate sensors: _____

**Sampling rate:** _____ Hz (or measurements/second)

**Data points per day:** _____ (calculated or estimated)

**Size per day:** _____ MB (or GB)

**Your answer:** _______________________________________________

---

## Question 6: Approximate Cost Tier

### Based on your data + compute, what tier fits?

- [ ] **Minimal** ($0–50/mo) — Small datasets, occasional compute, mostly TACC
- [ ] **Moderate** ($50–200/mo) — Moderate data + regular training, hybrid TACC/AWS
- [ ] **Significant** ($200–500/mo) — Larger datasets, frequent retraining, some GPU
- [ ] **Major** ($500+/mo) — Continuous training, heavy GPU, production-scale monitoring
- [ ] **Unknown** (need to measure first)

**Your answer:** _______________________________________________

---

## Question 7: Key Data Gaps

### What don't we know yet?

(E.g., "Exact training dataset size until we pull all sources", "Whether we'll do continuous retraining", "GPU vs. CPU cost trade-off", etc.)

_______________________________________________

---

## Additional Context (Optional)

Anything else about MSR chemistry data, validation needs, monitoring, or integration that affects Phase 1 costs?

(E.g., "Need GPU for uncertainty propagation", "Salt composition data arrives monthly", "Corrosion model validation requires 6-month test cycles", etc.)

_______________________________________________

---

## Summary Table

| Aspect | Your Answer |
|--------|-------------|
| **Training data size** | _____ GB |
| **Retraining frequency** | One-time / Occasional / Regular / Continuous |
| **Compute per run** | _____ CPU hrs + _____ GPU hrs |
| **Chemistry simulation output/month** | _____ GB |
| **Real-time salt/corrosion monitoring?** | No / Planned / Yes (limited) / Yes (full) |
| **Cost tier estimate** | Minimal / Moderate / Significant / Major |
| **Key uncertainty** | _____ |

---

## How Your Answers Are Used

1. **Feb 26:** You submit this form
2. **Feb 27:** Ben consolidates with Ondrej's MSR DT form + others
3. **Feb 28–Mar 1:** Final sizing calculation
4. **Mar 2:** Budget submitted to Dr. Clarno for approval

Your answers ensure your data pipelines are budgeted accurately and can scale in Phase 2 if needed.

---

## Questions?

Email Ben or check with Ondrej if you need clarification. No technical detail is too small.
