# Cost Estimation Form: Cole — Physics/MPACT

**For:** Cole (TRIGA Physics/MPACT Simulation)  
**Time to Complete:** 3–5 minutes  
**Deadline:** Friday, Feb 20, 2026, 5 PM  
**Submit to:** Ben  

---

## Overview

I need your help with:
- MPACT simulation workloads
- Historical data volume and retention needs
- How much data flows out of the system for external validation

Your answers drive **compute costs** and **storage costs**.

---

## Question 1: Data Egress (Networks Costs)

### How much data leaves AWS monthly?

This includes:
- Reports sent to external collaborators
- Validation datasets shared with other institutions
- Backups to external systems
- Cloud-to-TACC syncs

**Options:**
- [ ] I don't know (we'll estimate **100 GB/month**)
- [ ] Less than 100 GB/month
- [ ] 100–500 GB/month (typical research)
- [ ] 500 GB–2 TB/month
- [ ] More than 2 TB/month (why? give details)

**Your answer:** _______________________________________________

**Impact:**
- 100 GB/mo = $9/mo egress cost
- 500 GB/mo = $45/mo egress cost
- 2 TB/mo = $180/mo egress cost

---

## Question 2: Historical MPACT Archive Migration

### How much historical MPACT data should migrate to AWS?

This includes all HDF5 files, simulation outputs, and supporting data from prior years.

**Options:**
- [ ] Don't migrate; keep on TACC only (cost: $0)
- [ ] Migrate less than 50 GB archive (one-time: $1)
- [ ] Migrate 50–500 GB archive (one-time: $10–25)
- [ ] Migrate more than 500 GB archive (specify size below)

**Your answer:** _______________________________________________

**If "more than 500 GB," how much total?**  
_____ GB (or _____ TB)

**Impact:**
- 100 GB migration = $2 one-time + $2/mo storage
- 500 GB migration = $10 one-time + $10/mo storage

---

## Question 3: Bias Correction Model Training (Optional Detail)

### How often should bias correction models retrain?

This is the ML model that corrects MPACT predictions using measured reactor data.

**Options:**
- [ ] Annual retraining (cost: ~$200/year on AWS)
- [ ] Monthly retraining (cost: ~$50/month on AWS)
- [ ] Ad-hoc/on-demand (cost: ~$0 baseline)
- [ ] We handle this outside AWS (cost: $0)

**Your answer:** _______________________________________________

**Note:** We'll estimate if you don't have a preference. Monthly is typical for production ML systems.

---

## Optional: Additional Context

If you have other considerations that affect compute or storage, add them here:

```
(e.g., planned expansions, new simulation types, compliance requirements)
```

---

## Thank You!

Your 3–5 minute response helps ensure the cost estimate reflects real TRIGA operations.

**Return to:** Ben (email or this form filled out)  
**Deadline:** Friday, Feb 20, 5 PM

---

## How Your Answers Are Used

| Your Answer | Maps To | AWS Service | Impact |
|------------|---------|---|---|
| Q1: Egress | Data transfer costs | EC2 Data Transfer | $9–180/mo |
| Q2: Archive size | S3 storage | S3 Glacier | $0–30/mo |
| Q3: ML retraining | Compute hours | EC2 instances | $0–50/mo |

All costs will be traceable to official AWS pricing with specific assumptions noted.
