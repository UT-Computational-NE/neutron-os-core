# Executive Summary: Feb 10 Sm-153 Incident → PRD/Dashboard Implications

## Bottom Line

Bill's incident report reveals **critical gaps in the "digital shadow" (DT model) integration for medical isotope production:**

**The Problem:**
- 130 mCi vs. 150 mCi target = 7% shortfall, barely acceptable for patient care
- **The DT could not predict this shortfall beforehand** → no pre-production warning
- **The DT could not diagnose the root cause in real-time** → operator flying blind during production
- This is preventable with proper DT integration as **P0 (critical), not P2 (optional)**

**Why It Matters for Neutron OS:**
- Medical Isotope Production PRD has DT integration as **P2** — this incident elevates it to **P0**
- Analytics Dashboards need **new scenarios** for production planning and anomaly detection
- Data Platform needs **new tables** for xenon state validation and model error tracking

**Immediate Action:**
1. Re-prioritize MI-020 (yield prediction model) from "planned P1" → **active P0 mission**
2. Create 3 new dashboard scenarios (see below)
3. Timeline: MVP deployed by end of Q1 2026 to prevent recurrence

---

## Three Critical Scenarios Missing from Current PRDs

### Before Production (Decision Support)
```
PRODUCTION MANAGER'S QUESTION:
"Should we schedule Sm-153 for Monday, or wait for xenon decay?"

CURRENT SYSTEM: 
"Let me think... xenon from Sunday is ~90% decayed by Monday. 
 Power looks stable. Fuel temp was normal last week. 
 I'll schedule it for Monday." [HOPES FOR BEST]

PROPOSED DIGITAL SHADOW:
"Given xenon inventory estimate (from rod calibration), predicted 
 activity is 143 ± 8 mCi. Confidence: MEDIUM (model has ±10% 
 historical scatter).
 
 RISK SCORE: YELLOW (yield may be 135-150 mCi).
 
 OPTION A: Proceed Monday — accept 10% shortfall risk
 OPTION B: Delay 6h for xenon decay → predicted 147 ± 8 mCi (GREEN)
 OPTION C: Delay 12h → predicted 150 ± 8 mCi (GREEN, xenon >95% decayed)"
```

### During Production (Real-Time Anomaly Detection)
```
OPERATOR'S OBSERVATION (actual from Feb 10):
"Fuel temp dropped from 373°C to 367°C despite stable 950 kW power. Xenon is 
higher than usual. Power monitors look fine. Position looks fine. Is this normal?"

CURRENT SYSTEM:
"Hmm, could be xenon effect or something else. Keep watching."
[WAITS FOR BATCH COMPLETION TO FIND OUT]

PROPOSED DIGITAL SHADOW:
"⚠️ ALERT: Fuel temperature 3°C below baseline for this power/xenon state.
 
 This suggests either:
 a) Xenon model underestimating reactivity (refine model)
 b) Local flux depression in CT position (check rod calibration)
 c) Coolant flow anomaly (check pump)
 
 IMPACT: Current prediction is 138 mCi (was 150 mCi forecasted).
 
 RECOMMEND: Extend irradiation by 15 min to recover +2 mCi if reactor 
 margin allows. Otherwise, expect 135-140 mCi final activity."
```

### After Production (Model Validation)
```
POST-MORTEM ANALYSIS:
"Predicted 138 mCi, actual 130 mCi. Explanation?
 
 ├─ Xenon model error: -3 mCi (xenon worth may be -2.8¢ vs. -2.3¢ model)
 ├─ Position-specific flux: -3 mCi (CT may have lower flux than assumed)
 ├─ Fuel burnup model: -1 mCi (minor contributor)
 ├─ Measurement noise: ±2 mCi (within typical ±2% radiometric accuracy)
 └─ ROOT CAUSE: Xenon model refinement + position-specific flux validation needed
 
 ACTION: Recalibrate xenon worth; run high-fidelity MPACT for CT position;
         re-fit Sm-153 yield curve for next production run."
```

---

## What This Means for PRDs

### Medical Isotope Production PRD
Most affected. Currently:
- **MI-020** (yield prediction model) = P1, not started
- **MI-023** (DT flux integration) = P2, low priority
- No pre-production validation workflow
- No real-time anomaly detection

**Action:** These become P0. Must be completed before next high-risk isotope production (Sm-153, Lu-177).

### Analytics Dashboards PRD
Secondary impact. Currently:
- Reactor Performance Analytics scenario great for ops monitoring
- **Missing:** Medical Isotope Production Planning scenario
- **Missing:** Real-time production batch monitoring scenario
- **Missing:** Post-production yield validation scenario

**Action:** Add 3 new scenarios (see attached detailed analysis).

### Data Platform PRD
Must support xenon state tracking + model validation:
- Need `xenon_state_hourly` table (already planned, but needs confidence intervals)
- Need `yield_prediction_history` table (predicted vs. actual for all batches)
- Need `rod_calibration_inference` (real-time xenon estimate from rod position)

**Action:** Prioritize these tables in ingestion roadmap.

---

## Timeline & Risk Factors

**Q1 2026 MVP (8 weeks):**
- ✓ Xenon state estimation from rod calibration
- ✓ Simple yield prediction model (trained on ≥20 historical batches)
- ✓ Pre-production dashboard + real-time monitoring
- ✓ Field validation with production team
- **Risk:** Historical data insufficiency if <20 good batches available

**Q2 2026 Enhancement (2-3 months):**
- Isotope-specific models (Sm, I-131, Mo-99 separate)
- What-if scenario engine for scheduling optimization
- Post-production RCA automation

**Q3-Q4 2026 Advanced:**
- Integration with Scheduling System PRD
- Yield-based revenue optimization

---

## Key Questions for Bill/Facility Director

1. **Feb 10 Root Cause:** Is fuel temp drop consistent with xenon model, or is there unmodeled physics?
   - *Answer informs xenon validation strategy*

2. **Historical Data:** How many Sm-153 production runs in past 12 months? Any pattern of yield variance?
   - *<10 runs = high uncertainty; >20 runs = model can be trained with confidence*

3. **CT Position Flux:** Is CT position known to have lower flux than other irradiation sites? Documented?
   - *If flux distribution unknown, high-fidelity MPACT calcs will be needed*

4. **Operator Decision Freedom:** In real-time during production, can operator extend irradiation by 15 min or increase power by 50 kW if warned of shortfall?
   - *Yes = real-time anomaly detection very valuable; No = only pre-production decision support relevant*

5. **Patient Impact Tolerance:** If prediction says "50% chance of shortfall," how should production manager decide?
   - *Informs confidence interval thresholds and risk scoring logic*

---

## How This Strengthens NEUP/Neutron OS Proposal

This incident is **exactly the use case NEUP Medical Isotopes DT proposal should address:**

> "DT-driven semi-autonomous operations capability... operator-facing DT validity and confidence communication for medical isotope production workflows."

**The incident demonstrates the value:**
1. **Predictive capability:** Foreseeing fluence shortfalls before committing batch
2. **Real-time monitoring:** Detecting off-nominal conditions mid-production
3. **Operator confidence:** Clear explanation of "why was fluence low" post-mortem
4. **Regulatory credibility:** FDA/NRC sees data-driven process, not just "we felt something was off"

**Next NEUP reporting can cite this:**
- "In Feb 2026, an unforecasted fluence shortfall occurred due to xenon buildup undetected by operators."
- "If DT validation capability had been implemented, this would have been predicted 24h in advance."
- "Documented here as motivation for our yield prediction model development."

---

## Recommended Next Steps

1. **This Week:**
   - [ ] Bill confirms root cause assessment with actual DCS data (temp trends, xenon inventory)
   - [ ] Facility director reviews analysis, prioritizes PRD changes
   - [ ] Request: How many Sm-153 runs available for model training?

2. **Next 2 Weeks:**
   - [ ] Cross-check xenon model vs. fuel temperature data (validation study)
   - [ ] Identify "gold standard" high-fidelity flux calculation (MCNP? MPACT?)
   - [ ] Begin design of pre-production planning dashboard

3. **Month 1-2:**
   - [ ] MVP implementation starts (xenon model → prediction model → dashboard)
   - [ ] Plan field deployment & operator training

---

**Attachments:**
1. [Full Analysis Document](./Sm153_Incident_Analysis_PRD_Implications.md) — 15-page detailed PRD gap analysis
2. 3 New Dashboard Scenarios (in full analysis)
3. Data models and acceptance criteria (in full analysis)

**Document Prepared:** February 10, 2026
**Status:** Ready for stakeholder review and decision
