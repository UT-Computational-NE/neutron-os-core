# Cost Estimation Form: Cole — Physics/MPACT

**For:** Cole (TRIGA Physics/MPACT Simulation)  
**Time to Complete:** 3–5 minutes  
**Deadline:** Friday, Feb 20, 2026, 5 PM  
**Submit to:** Ben  

---

## Precision Expectation

Order-of-magnitude estimates (±50%) are perfect. Rough ranges beat false precision. T-shirt sizing or "I don't know" is fine—we have fallbacks.

---

## Overview

I need your help with:
- MPACT simulation workloads
- Historical data volume and retention needs
- How much data flows out of the system for external validation

Your answers drive **compute costs** and **storage costs**.

---

## Question 1: Data Egress (Network Costs)

### How much data leaves AWS monthly?

This includes:
- Reports sent to external collaborators
- Validation datasets shared with other institutions
- Backups to external systems
- Cloud-to-TACC syncs

**T-Shirt Size (pick one):**
- [ ] **S (Small):** < 50 GB/month = ~$5/mo egress
- [ ] **M (Medium):** 50–200 GB/month = ~$9–18/mo egress
- [ ] **L (Large):** 200–500 GB/month = ~$18–45/mo egress
- [ ] **XL (Extra Large):** 500+ GB/month = ~$45+/mo egress
- [ ] **I don't know** (we'll estimate **Medium** as baseline)

**Your answer:** _______________________________________________

---

## Question 2: Historical MPACT Archive Migration

### How much historical MPACT data should migrate to AWS?

This includes all HDF5 files, simulation outputs, and supporting data from prior years.

**T-Shirt Size (pick one):**
- [ ] **S (Small):** None; keep on TACC only = $0
- [ ] **M (Medium):** ~50–200 GB archive = $1–5 one-time + $2–5/mo storage
- [ ] **L (Large):** ~200–500 GB archive = $5–12 one-time + $5–12/mo storage
- [ ] **XL (Extra Large):** 500+ GB archive = $12+/mo storage (specify: _____ GB)
- [ ] **Unknown** (we'll estimate **Medium**)

**Your answer:** _______________________________________________

---

## Question 3: Bias Correction Model Training

### How often should bias correction models retrain?

This is the ML model that corrects MPACT predictions using measured reactor data.

**T-Shirt Size (pick one):**
- [ ] **S (Small):** None/annual = ~$20/year on AWS
- [ ] **M (Medium):** Monthly retraining = ~$50/month on AWS
- [ ] **L (Large):** Weekly retraining = ~$200/month on AWS
- [ ] **Unknown** (we'll estimate **Medium** as typical)

**Your answer:** _______________________________________________

---

## Additional Context (Optional)

Anything else that affects MPACT costs, storage, or data flow?

_______________________________________________

---

## Thank You!

**Return to:** Ben  
**Deadline:** Friday, Feb 20, 5 PM
