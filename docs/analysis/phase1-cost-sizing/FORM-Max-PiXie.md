# Cost Estimation Form: Max — PiXie Hardware

**For:** Max (PiXie DAQ / Hardware Integration)  
**Time to Complete:** 3 minutes  
**Deadline:** Wednesday, Feb 16, 2026, 5 PM ⚠️ **BLOCKING GATE**  
**Submit to:** Ben  

---

## Precision Expectation

Order-of-magnitude estimates (±50%) are perfect. Rough ranges beat false precision. T-shirt sizing or "I don't know" is fine—we have fallbacks.

---

## Overview

I need your help with:
- Whether PiXie Phase 1 is happening in 2026
- Current development status and testing timeline
- Data volume estimates (once sampling rates are finalized)
- Hardware integration constraints

**Context:** PiXie is in active development. You haven't yet tested with actual TRIGA data, and key parameters (sampling rates, data format, volume) are still TBD. Your answer to **Question 1** determines whether we budget for PiXie Phase 1, and answers to Q2–Q3 help us plan for the uncertainties.

---

## Question 1 (BLOCKING): PiXie Phase 1 in 2026? ⚠️

### What's the realistic timeline for PiXie data streaming to Neutron OS?

**Context:** PiXie is in active development. You haven't tested with actual TRIGA data yet, and sampling rates/data formats are still TBD with the digital twin team.

**Options:**
- [ ] **Early 2026** — Ready to stream nightly data to cloud (like ZOC logger today)
- [ ] **Late 2026** — Still in testing/optimization; archive locally first
- [ ] **2027+** — Defer to Phase 2 (data stays local, no cloud streaming)
- [ ] **UNCERTAIN** — Waiting on SMU/thermocouple decisions from team

**Your answer:** _______________________________________________

**Why this matters:**
- **Early 2026:** Adds Redpanda Cloud ($150–300/mo) + extra storage
- **Late 2026:** Local archive only, minimal new cloud costs until Q4
- **2027+:** Baseline cost stays $612/mo (Minimal scenario)
- **Cost range:** ~$0–300/mo depending on timeline

---

## Question 2: Sampling Rate & Data Format Strategy

### What are your planned SMU + thermocouple sampling rates?

**Context:** You mentioned SMU needs 1 KHz+, thermocouples could be 10s of Hz. These haven't been locked in with the digital twin team yet.

**Options:**
- [ ] **Conservative:** SMU 1 kHz, thermocouples 10 Hz (lower bandwidth, easier debugging)
- [ ] **Moderate:** SMU 2–5 kHz, thermocouples 50+ Hz (real-time control loop ready)
- [ ] **Aggressive:** SMU 10+ kHz, thermocouples 100+ Hz (captures transients)
- [ ] **TBD:** Waiting on digital twin team guidance on required sampling rates

**Your answer:** _______________________________________________

**Why this matters:** Sampling rate directly drives data volume. Without TRIGA test data, we'll estimate conservatively.

### What data format will you use? (CSV, HDF5, binary, or PostgreSQL?)

**Your answer:** _______________________________________________

**Note:** This affects storage costs and pipeline complexity. ZOC uses CSV currently.

---

## Question 3: Data Logging Strategy (Continuous vs. Burst)

### How will PiXie logging work in Phase 1?

**Options:**
- [ ] **Only during reactor ops** (e.g., 20–30 hrs/week) — Lower volume
- [ ] **24/7 continuous** (all day, every day) — Higher volume, captures decay rates
- [ ] **Determined by detector lifespan** — Log continuously until mini fission chamber burn-out
- [ ] **TBD** — Waiting on Dr. Charlton/Dr. Clarno guidance on detector deployment timeline

**Your answer:** _______________________________________________

**Why this matters:** 
- Reactor-only logging: ~$50–100/mo storage
- 24/7 logging: ~$200–400/mo storage
- Detector burn-out determines how long to keep this running

### Data retention in cloud:

**Plan:** Archive locally, sync nightly to TACC (like ZOC logger today). Real-time streaming to cloud is Phase 2+ decision.

**Immediate need:** How long should cloud keep hot data (for analysis/access)?
- [ ] 1–2 weeks
- [ ] 1–3 months
- [ ] TBD (we'll estimate 1–3 months)

---

## Additional Context (Optional)

Anything else about PiXie that affects data volume, timeline, or cloud costs?

_______________________________________________

---

## Thank You!

**Return to:** Ben  
**Deadline:** Wednesday, Feb 16, 5 PM ⚠️
