# Generic Data Builder Questionnaire

**For:** Anyone building systems that generate, collect, or process data for Neutron OS  
**Deadline:** Friday, February 20, 2026, 5 PM  
**Time to complete:** 5–10 minutes  
**Completed by:** _____________________ (Your name)

---

## Precision Expectation

Order-of-magnitude estimates (±50%) are perfect. Rough ranges beat false precision. T-shirt sizing or "I don't know" is fine—we have fallbacks.

---

## Overview

I need your help with:
- What you're building and what data it generates
- How much data, how often, and for how long
- What storage, compute, and external services you'll need
- Integration points with the rest of the platform

**Context:** You have domain expertise we don't. Your answers help us size infrastructure accurately and avoid under-provisioning.

---

## Question 1: What Are You Building?

### What component or system are you developing?

**Examples:**
- A new sensor integration pipeline
- A data validation framework
- A simulation output processor
- An external data connector
- A custom analytics module
- An experiment automation tool

**Your answer:** 
_______________________________________________

### What problem does it solve?

_______________________________________________

### When will Phase 1 (2026) include this?

- [ ] Active development in 2026 (budget for it)
- [ ] Planning phase; defer to 2027 (estimate placeholder costs)
- [ ] Exploratory; too early to budget (flag as future)

**Your answer:** _______________________________________________

---

## Question 2: Data Volume & Update Frequency

### How much data does your system generate or process?

**Options:**
- [ ] **Minimal:** < 1 GB/month (small configs, metadata, logs)
- [ ] **Moderate:** 1–100 GB/month (sensor streams, simulation outputs)
- [ ] **Heavy:** 100 GB–1 TB/month (continuous high-frequency data)
- [ ] **Extreme:** > 1 TB/month (requires streaming architecture)

**Your answer:** _______________________________________________

### If you chose "Moderate," "Heavy," or "Extreme," estimate:

**Data volume:** _____ GB/day (or TB/month)

**Data type examples:**
- CSV files? (yes/no)
- JSON/XML? (yes/no)
- Binary (HDF5, protobuf, custom)? (yes/no)
- Database records? (yes/no)
- Media (audio, video)? (yes/no)

**Your answer:** _______________________________________________

### How often do you generate or update data?

- [ ] **Real-time/streaming** (continuous, < 1 sec latency)
- [ ] **Frequent** (minute-level, hourly updates)
- [ ] **Regular batch** (daily, weekly)
- [ ] **Irregular** (event-driven, on-demand)
- [ ] **One-time** (historical migration only)

**Your answer:** _______________________________________________

### Why this frequency?

(e.g., "Sensors sample at 10 Hz", "Simulations run nightly", "User-triggered analysis")

_______________________________________________

---

## Question 3: Storage & Retention

### How long should data stay accessible (hot storage)?

- [ ] **Short-term:** 1–2 weeks (real-time dashboards only)
- [ ] **Medium-term:** 1–3 months (active analysis window)
- [ ] **Long-term:** 6–12 months (historical reference)
- [ ] **Forever** (compliance archive)

**Your answer:** _______________________________________________

### After hot storage, what happens?

- [ ] **Delete** (data not needed longer)
- [ ] **Archive to cold storage** (S3 Glacier; occasional access)
- [ ] **Keep in place** (long-term hot cost)

**Your answer:** _______________________________________________

### Where should data live?

- [ ] **In the Neutron OS lakehouse** (Iceberg tables in S3)
- [ ] **In a specialized database** (PostgreSQL, DuckDB, etc.)
- [ ] **External system** (TACC, Box, external API)
- [ ] **Multiple locations** (sync between systems)

**Your answer:** _______________________________________________

---

## Question 4: Compute & Processing

### Does your system require compute resources?

- [ ] **None** (just storage; read-only access)
- [ ] **Light** (occasional batch jobs, < 1 hr/day)
- [ ] **Moderate** (daily batch, dbt transformations, orchestration)
- [ ] **Heavy** (continuous processing, real-time transformations)
- [ ] **GPU-intensive** (ML training, simulations)

**Your answer:** _______________________________________________

### If "Light," "Moderate," or "Heavy," describe your workload:

(e.g., "Daily dbt runs that transform 50 GB", "Hourly data validation checks", "Model training 2x/week")

_______________________________________________

### Estimated compute requirements:

- CPU hours/month: _____ (or "don't know")
- Memory: _____ GB (or "don't know")
- GPU required? (yes/no): _____

**Your answer:** _______________________________________________

---

## Question 5: External Services & APIs

### Do you use external APIs or services?

- [ ] **No external dependencies**
- [ ] **Yes—cloud services** (e.g., Claude API, commercial tools)
- [ ] **Yes—data sources** (e.g., external sensor feeds, public APIs)
- [ ] **Yes—both**

**Your answer:** _______________________________________________

### If yes, what services and how often?

**Examples:**
- "Claude API: 100 queries/day for text summarization"
- "External weather API: 1 call/hour"
- "Anthropic API for RAG: 10 queries/hour during business hours"

**Your answer:** 
_______________________________________________

### Estimated cost of external services (if known):

**Per month:** $_____ (or estimate)

**Your answer:** _______________________________________________

---

## Question 6: Integration Points

### What other Neutron OS systems does your component integrate with?

**Check all that apply:**
- [ ] **Data Platform** (Iceberg lakehouse, dbt, Dagster)
- [ ] **Reactor Ops Log** (logs, compliance tracking)
- [ ] **Experiment Manager** (sample tracking, scheduling)
- [ ] **Analytics Dashboards** (Superset visualizations)
- [ ] **Digital Twin** (predictions, model validation)
- [ ] **RAG/Search** (Claude API, embeddings)
- [ ] **External** (TACC, Box, other systems)
- [ ] **None** (standalone for now)

**Your answer:** _______________________________________________

### Do you read from other systems? Write to other systems? Both?

_______________________________________________

---

## Question 7: Cost Estimate Category

### Based on your answers, what cost tier does your component fit?

- [ ] **Minimal** ($0–50/mo) — Small datasets, occasional processing
- [ ] **Moderate** ($50–200/mo) — Regular data flow, some compute
- [ ] **Significant** ($200–500/mo) — High volume or intensive compute
- [ ] **Major** ($500+/mo) — Continuous streaming, GPU, or heavy external API usage
- [ ] **Unknown** (need to build it first to measure)

**Your answer:** _______________________________________________

### What's your biggest cost uncertainty?

(e.g., "Don't know data volume until we test", "Compute needs depend on data size", "External API pricing unclear")

_______________________________________________

---

## Question 8: Additional Context

### Is there anything else we should know?

(E.g., constraints, dependencies, timeline pressures, opportunities to save costs)

_______________________________________________

---

## Summary Table

| Aspect | Your Answer |
|--------|-------------|
| **Component name** | _____ |
| **Data volume estimate** | _____ GB/month |
| **Update frequency** | _____ |
| **Hot retention** | _____ |
| **Compute needs** | _____ (Light/Moderate/Heavy/GPU) |
| **External APIs** | _____ |
| **Integration points** | _____ |
| **Cost tier estimate** | _____ |
| **Key uncertainty** | _____ |

---

## How Your Answers Are Used

1. **Feb 20:** Your form is received and reviewed
2. **Feb 24:** Your component's costs are calculated using the AWS Pricing Calculator
3. **Feb 25–26:** Your costs are included in the final budget submission
4. **Feb 27:** Dr. Clarno approves (or asks for clarification)

**Your role:** Provide domain expertise. We handle the AWS pricing and tool selection.

---

## Need Help?

If you're unsure about any question:
- Email Ben with the question number and your context
- Example: "I know I'm generating ~5 GB/day, but I'm not sure if that's 'Moderate' or 'Heavy'"

We'll help you estimate and ensure accuracy.
