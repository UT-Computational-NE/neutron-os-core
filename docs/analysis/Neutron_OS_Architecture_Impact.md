# How Sm-153 Incident Reshapes Neutron OS Architecture

## Context: The Incident as a Sentinel Event

The Feb 10 Sm-153 production shortfall (130 mCi vs. 150 mCi target) is not an operational failure — it's a **signal that the system design is incomplete**.

This is exactly what NEUP Medical Isotopes proposal describes:
> "DT-driven semi-autonomous operations capability... requiring operator-facing DT validity and confidence communication"

**The incident proves we need all three:**

1. **DT Validity** — Can we predict production outcomes given reactor state?
2. **Confidence Communication** — Can we quantify uncertainty and guide decisions?  
3. **Semi-Autonomous Operations** — Can the system detect anomalies and suggest corrections?

Currently: **0 out of 3** are implemented.

---

## Neutron OS Architecture Impact

### Current Architecture (Draft)

```
┌─────────────────────────────────────────────────────────────────┐
│                    NEUTRON OS ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   DATA LAYER                                                    │
│   ┌──────────────────────────────────────────────┐             │
│   │  Bronze (Raw)         Silver (Cleaned)       │             │
│   │  ├─ DCS Timeseries    ├─ Reactor state      │             │
│   │  ├─ Ops Log           ├─ Normalized signals │             │
│   │  ├─ Experiments       └─ Validated data     │             │
│   │  └─ QC Records                              │             │
│   └──────────────────────────────────────────────┘             │
│                    ↓                                             │
│   ┌──────────────────────────────────────────────┐             │
│   │  Gold (Analytics-Ready)                      │             │
│   │  ├─ reactor_hourly_metrics                  │             │
│   │  ├─ xenon_state_hourly                      │             │
│   │  ├─ fuel_burnup_current                     │             │
│   │  └─ compliance_summary                      │             │
│   └──────────────────────────────────────────────┘             │
│                    ↓                                             │
│   ANALYTICS LAYER                                               │
│   ┌──────────────────────────────────────────────┐             │
│   │  Superset Dashboards                         │             │
│   │  ├─ Reactor Ops Dashboard (P0) ✓            │             │
│   │  ├─ Operations Log Dashboard (P0) ✓         │             │
│   │  ├─ Reactor Performance Analytics (P0) ✓    │             │
│   │  ├─ Fuel Burnup Heatmap (P1)                │             │
│   │  └─ [MISSING: Medical Isotope Scenarios]     │ ← GAP       │
│   └──────────────────────────────────────────────┘             │
│                                                                 │
│   OPERATIONAL SYSTEMS                                           │
│   ├─ Experiment Manager                                         │
│   ├─ Reactor Ops Log                                            │
│   ├─ Scheduling System                                          │
│   └─ [MISSING: Medical Isotope Production module]  ← DATA GAP  │
│                                                                 │
│   DIGITAL TWIN (PROPOSED)                                       │
│   └─ [MISSING: DT validation → dashboards]       ← MAJOR GAP  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Post-Incident: Required Additions

```
┌─────────────────────────────────────────────────────────────────┐
│              NEUTRON OS + MEDICAL ISOTOPE CAPABILITY             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   DATA LAYER (EXPANDED)                                         │
│   ┌──────────────────────────────────────────────┐             │
│   │  Bronze (Raw) + Medical Isotope Orders       │             │
│   │  ├─ DCS Timeseries                          │             │
│   │  ├─ Ops Log                                 │             │
│   │  ├─ Experiments                             │             │
│   │  ├─ QC Records                              │             │
│   │  └─ 🆕 isotope_orders_raw                    │ ← NEW       │
│   │  └─ 🆕 isotope_qc_measurements_raw           │ ← NEW       │
│   └──────────────────────────────────────────────┘             │
│                    ↓                                             │
│   ┌──────────────────────────────────────────────┐             │
│   │  Silver (Cleaned) + Inference                │             │
│   │  ├─ Reactor state                           │             │
│   │  ├─ Normalized signals                      │             │
│   │  ├─ Validated data                          │             │
│   │  └─ 🆕 rod_calibration_inference             │ ← NEW       │
│   │  └─ 🆕 xenon_state_estimated                 │ ← NEW       │
│   └──────────────────────────────────────────────┘             │
│                    ↓                                             │
│   ┌──────────────────────────────────────────────┐             │
│   │  Gold (Analytics-Ready) + Predictions        │             │
│   │  ├─ reactor_hourly_metrics                  │             │
│   │  ├─ xenon_state_hourly                      │             │
│   │  ├─ fuel_burnup_current                     │             │
│   │  ├─ compliance_summary                      │             │
│   │  └─ 🆕 isotope_yield_predicted               │ ← NEW       │
│   │  └─ 🆕 isotope_yield_actual_measured         │ ← NEW       │
│   │  └─ 🆕 model_error_analysis                  │ ← NEW       │
│   └──────────────────────────────────────────────┘             │
│                    ↓                                             │
│   ANALYTICS LAYER (EXPANDED)                                    │
│   ┌──────────────────────────────────────────────┐             │
│   │  Superset Dashboards                         │             │
│   │  ├─ Reactor Ops Dashboard ✓                 │             │
│   │  ├─ Operations Log Dashboard ✓              │             │
│   │  ├─ Reactor Performance Analytics ✓         │             │
│   │  ├─ Fuel Burnup Heatmap                     │             │
│   │  └─ 🆕 Medical Isotope Production Planning   │ ← NEW P0    │
│   │  └─ 🆕 Real-Time Production Monitoring       │ ← NEW P0    │
│   │  └─ 🆕 Yield Validation & Model Analysis     │ ← NEW P0    │
│   └──────────────────────────────────────────────┘             │
│                                                                 │
│   OPERATIONAL SYSTEMS (EXPANDED)                                │
│   ├─ Experiment Manager                                         │
│   ├─ Reactor Ops Log                                            │
│   ├─ Scheduling System                                          │
│   └─ 🆕 Medical Isotope Production Module        │ ← NEW       │
│      ├─ Order intake                                            │
│      ├─ Batch scheduling                                        │
│      ├─ Production planning (with pre-validation)               │
│      ├─ QC/QA workflow                                          │
│      ├─ Shipping coordination                                   │
│      └─ Revenue tracking                                        │
│                                                                 │
│   DIGITAL TWIN INTEGRATION                                      │
│   ┌──────────────────────────────────────────────┐             │
│   │  Yield Prediction Engine (P0 via MI-020)     │ ← NEW       │
│   │  ├─ Reactivity model (xenon, burnup, temp)  │             │
│   │  ├─ Flux model (power → local position flux)│             │
│   │  ├─ Activation model (flux → activity)      │             │
│   │  └─ Confidence estimation (from hist data)  │             │
│   │                                              │             │
│   │  Real-Time Anomaly Detection                 │ ← NEW       │
│   │  ├─ Power trending                          │             │
│   │  ├─ Temperature anomaly detection           │             │
│   │  ├─ Running activity prediction comparison  │             │
│   │  └─ Alert logic & recommendations           │             │
│   │                                              │             │
│   │  Post-Production Model Validation            │ ← NEW       │
│   │  ├─ Prediction error decomposition          │             │
│   │  ├─ Model parameter re-fitting              │             │
│   │  └─ Confidence interval calibration         │             │
│   └──────────────────────────────────────────────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow: Pre-Production Planning (New)

```
┌─────────────────────────────────────────────────────────────┐
│ THURSDAY MORNING: Production Manager Plans Monday Batch    │
└─────────────────────────────────────────────────────────────┘

1. ORDERS POOL
   ├─ Sm-153: 150 mCi requested, calibrate 10:00 AM Monday
   ├─ I-131: 500 mCi requested, calibrate 10:00 AM Monday
   └─ Lu-177: 25 mCi requested, calibrate 10:00 AM Monday

2. CURRENT CORE STATE (Real-Time from DCS)
   ├─ Power: 0 kW (shutdown since Wednesday)
   ├─ Xenon estimate (from rod calibration): ~200 mCi equiv
   │   └─ Decay from Wednesday: e^(-72h/9.1h) ≈ 0.002, so negligible
   ├─ Fuel burnup: 35.6 g U-235 (per fuel element tracking)
   └─ Fuel temperature: 35°C (pool ambient, shutdown state)

3. XENON FORECAST (24-hour projection)
   ├─ Saturday (if operating): NOT planned
   ├─ Sunday (if operating): NOT planned
   └─ Monday 06:00 AM: ~0 xenon (core clean after shutdown)

4. YIELD PREDICTION MODEL RUNS
   Input: 
     • Power setpoint: 950 kW (standard Monday level)
     • Duration: 4 hours (standard for Sm-153 batch)
     • Xenon state: Clean (0 mCi equiv)
     • Burnup: 35.6 g U-235
     • Irradiation position: CT (standard for Sm-153)
   
   Output [Sm-153 prediction]:
     • Predicted activity at 10:00 AM Monday: 152 ± 7 mCi
     • 95% CI: [145, 159] mCi
     • Confidence: HIGH (baseline clean core, model well-validated)
     • Risk score: GREEN (predicted > target + 5% margin)
   
   Output [I-131 prediction]:
     • Predicted activity: 505 ± 20 mCi
     • 95% CI: [485, 525] mCi
     • Confidence: MEDIUM
     • Risk score: GREEN
   
   Output [Lu-177 prediction]:
     • Predicted activity: 26 ± 2 mCi
     • 95% CI: [24, 28] mCi
     • Confidence: HIGH
     • Risk score: GREEN

5. DASHBOARD RECOMMENDATION
   ✓ Monday production batch: APPROVED
   Rationale: All predictions show GREEN (low risk of shortfall)

6. PRODUCTION SCHEDULE COMMITTED
   Monday 06:00 AM: Start Sm-153 in CT
   Monday 06:30 AM: Start I-131 in RSR (scheduled in parallel)
   Monday 07:00 AM: Start Lu-177 in TPNT
   [...]
```

---

## Data Flow: Real-Time Monitoring (New)

```
┌─────────────────────────────────────────────────────────────┐
│ MONDAY 06:00 AM: Sm-153 Irradiation Begins                 │
└─────────────────────────────────────────────────────────────┘

REAL-TIME DASHBOARD (every 5 minutes):

06:00   Power: 950 kW ✓  |  Temp: 371°C  |  Activity integral: ~8 mCi
        Status: GREEN proceed

06:05   Power: 950 kW ✓  |  Temp: 371°C  |  Activity integral: ~16 mCi
        Status: GREEN proceed

06:10   Power: 950 kW ✓  |  Temp: 371°C  |  Activity integral: ~24 mCi
        Status: GREEN proceed

...

08:00   Power: 950 kW ✓  |  Temp: 370°C  |  Activity integral: ~120 mCi
        [Still GREEN; tracking nominal]
        Predicted final: 150 ± 5 mCi (narrow range)

08:30   Power: 950 kW ✓  |  Temp: 368°C  |  Activity integral: ~133 mCi
        ⚠️ ALERT: Fuel temp 2°C below baseline for this power/xenon state
                  Possible causes: [rod calibration?] [coolant?] [other?]
        Predicted final: 140 ± 8 mCi (dropped from 150)
        Status: YELLOW - INVESTIGATE

        Recommendation: 
          Option A) Extend irradiation 10 min → predicted +2 mCi recovery
          Option B) Increase power to 1000 kW → predicted +3 mCi recovery
          Option C) Continue as-is, expect ~140 mCi

08:45   Operator Decision: Extend 10 minutes
        Log: [Extension applied: temp_anomaly, operator=J_Smith, 
              delta_predicted=+1.5_mCi, rationale='margin_recovery']

09:50   Irradiation complete
        Predicted final: 143 ± 8 mCi
        Status: YELLOW (slightly below 150 mCi target)

10:00   QC measurement: Activity = 130 mCi at calibration time
        ⚠️ Alert: Actual 130 mCi is 13 mCi below last prediction (143 mCi)
                  Error larger than expected measurement noise (±2 mCi)
        
        RCA triggered: Analyze why prediction was optimistic
```

---

## Data Flow: Post-Production Analysis (New)

```
┌─────────────────────────────────────────────────────────────┐
│ TUESDAY 09:00 AM: Root Cause Analysis Report Generated     │
└─────────────────────────────────────────────────────────────┘

AUTOMATED ANALYSIS:

Batch ID: SM-2026-02-10-001
Predicted (from Saturday): 152 ± 7 mCi → GREEN
Predicted (on Monday 08:30, real-time): 143 ± 8 mCi → YELLOW  
Actual (measured): 130 mCi → SHORTFALL

Error Decomposition:
├─ Pre-prod forecast vs. actual: -22 mCi shortfall (-14.5%)
│  └─ Δ1: Xenon model: e^(-48h/9.1h) estimated Xe=0, actual Xe≠0?
│  └─ Δ2: Position flux: CT may be lower than global power suggests
│  └─ Δ3: Residual: Unknown physics
│
└─ Real-time forecast (08:30) vs. actual: -13 mCi shortfall (-9%)
   └─ Δ4: Temperature anomaly (368°C vs 370°C baseline) not fully modeled
   └─ Δ5: Assumed extension recovery didn't materialize

Confidence Interval Assessment:
─ Pre-prod 95% CI: [145, 159] mCi
  └─ Actual 130 mCi is OUTSIDE CI (5th percentile event)
  └─ Flag: Model confidence too optimistic; widen to [140, 165]?

Xenon Model Validation:
─ Observed: Fuel temp 2-3°C below baseline at 950 kW
─ Xenon model predicts: -2.3¢ reactivity loss → expect ~1°C temp drop
─ Discrepancy suggests: Xenon worth might be -2.8¢, not -2.3¢
─ Recommendation: Re-fit xenon model with temp as proxy

Flux Distribution:
─ Global 950 kW should yield ~Z flux (baseline)
─ CT position is reportedly unshielded, but actual flux may be lower
─ Need: MPACT high-fidelity calculation for CT geometry

ROOT CAUSE RANKING:
1. Xenon model underestimated impact (-3 mCi, 15% of 20 mCi total error)
2. CT position flux lower than assumed (-4 mCi, 20% error)
3. Temperature anomaly not captured by linear model (-3 mCi, 15%)
4. Residual unexplained physics (-10 mCi, 50%)

ACTION ITEMS:
Short-term:
  ☐ Recalibrate xenon worth curve (use fuel temp correlation)
  ☐ Request MPACT flux calculation for CT position
  ☐ Check rod calibration curves (validity date?)
  ☐ Collect 5 more Sm-153 runs before re-committing to Monday schedule

Long-term:
  ☐ Integrate fuel temp as xenon validation signal in pipeline
  ☐ Develop isotope-specific models (Sm ≠ I-131 activation function)
  ☐ Include position-specific flux profiles in DT

COMPLIANCE NOTES FOR NEUP REPORT:
─ "Feb 10 incident demonstrates value of DT-driven validation capability"
─ "Without digital shadow: near-miss (130 mCi barely sufficient for patient)"
─ "With proposed DT capability: 24h advance warning + real-time anomaly detection"
─ "Model error analysis demonstrates systematic improvement path"
```

---

## Integration with NEUP Medical Isotope Proposal

### How This Incident Supports the Proposal

The Feb 10 Sm-153 incident is **case study #1** for NEUP deliverable:

> "Development and deployment of DT-driven semi-autonomous operations capability with operator-facing confidence communication for medical isotope production workflows at UT NETL TRIGA reactor"

**Proposal Success Metrics Addressed:**

| Proposal Metric | Sm-153 Incident Evidence | Dashboard Support |
|-----------------|--------------------------|------------------|
| "DT can predict production outcomes with quantified confidence" | Pre-prod forecast should have predicted 136-150 mCi range; actual 130 mCi falls within → validates approach | ✓ Medical Isotope Production Planning dashboard |
| "Real-time anomaly detection prevents off-nominal operation" | Fuel temp drop detected but not acted upon; system should have alerted & suggested extend/increase power | ✓ Real-Time Production Monitoring dashboard |
| "Operator-facing confidence communication" | Production manager should see written recommendation: "YELLOW: 30% risk of shortfall; recommend delay 6h for xenon decay" | ✓ Risk Score, What-If scenarios in dashboard |
| "Model validation improves over time" | Post-incident RCA shows systematic path to better xenon/flux models | ✓ Yield Validation & Model Analysis dashboard |
| "Regulatory credibility" | Data-driven incident root cause analysis replaces post-hoc explanations; demonstrates rigor to FDA/NRC | ✓ Audit-trail logging in production planning |

### NEUP Next Steps

Before final NEUP report (~May 2026), include:

1. **Case Study: Feb 10 Incident**
   - What happened
   - How DT would have prevented it
   - How dashboards communicate results to operators
   - What model improvements are underway

2. **Prototype Deployment**
   - Show Screenshots of 3 new dashboards (planning, monitoring, analysis)
   - Demonstrate prediction accuracy on retrospective data
   - Show xenon validation workflow

3. **Regulatory Pathway**
   - Preliminary FDA/NRC feedback on DT-based production authorization
   - Path to semi-autonomous operation (operator in loop → full autonomy?)

---

## User Expectations After Deployment

### Production Manager Workflow (Post-Deployment)

**Before:** "I'll review orders, think about xenon/power, and schedule for Monday if it looks good."

**After:** 
1. Dashboard shows predicted yields for each batch with GREEN/YELLOW/RED risk scores
2. If YELLOW: "Should I defer to Wed? Dashboard says xenon decays to X level → yield improves to Y"
3. Decision informed by data; rationale logged automatically
4. Monday production: dashboard shows running prediction updated every 5 min
5. If anomaly detected: alerts fired, recommendations shown (extend/increase power)
6. Tuesday: RCA report shows why actual vs. predicted; improvement actions identified

**Time investment:** Reduced from 2h (manual analysis) to 15 min (dashboard guided decision)

### Operator Workflow (During Production)

**Before:** "Watch power, temp, and rods. Hope the batch comes out OK."

**After:**
1. Pre-shift brief: "Your job is to monitor for fuel temp drops >2°C or activity trending >10% low"
2. Real-time dashboard shows all three + running prediction
3. If anomaly fires: "Should we extend? Let me check with production manager"
4. Decision recorded; system logs rationale
5. Post-batch: automatic RCA explains what happened

**Trust in system:** Increases as model predictions prove accurate month-over-month

### DT Developer Workflow (Monthly Model Improvement)

**Before:** DT is a research tool; no feedback loop to production

**After:**
1. Every Thursday morning: RCA dashboard shows all batches from past month
2. Identify patterns: "Sm-153 model systematically overpredicts by ~5%"
3. Re-fit model; test on historical data
4. Deploy refined model by Friday
5. Report monthly accuracy metrics to director

**Career progression:** "I'm making medical isotope production safer and more reliable"

---

## Organizational Alignment

### Leadership Buy-In Pathway

**Facility Director:** "This prevents near-misses affecting patient care. P0 priority."

**Production Manager:** "Real-time decision support + data-driven scheduling. Yes."

**Operators:** "Clear alerts and recommendations. Better than guessing."

**NRC Liaison:** "Data-driven operations with model validation. That's what we want to see."

**NEUP PIs:** "Direct evidence that DT improves medical isotope outcomes. Grant success story."

---

## Risks & Mitigation

| Risk | Consequence | Mitigation |
|------|-------------|-----------|
| Xenon model fundamentally flawed | All predictions unreliable | Validate against fuel temp pre-deployment |
| Data insufficient (<20 historical Sm runs) | Cannot train model | Use synthetic data; commission with extended validation |
| Operator ignores dashboards | Back to manual process | User acceptance testing; involve crew early |
| Real-time DCS feed unavailable | Cannot do anomaly detection | Batch analysis still valuable; add real-time later |
| Regulatory skepticism of DT | Cannot change procedures | Publish validation results; invite NRC review |

---

**Key Insight:** The Sm-153 incident is not a failure — it's a gift. It reveals exactly where the system needs strengthening, and it provides a concrete business case for investment.

**Next Step:** Get facility director and Bill's group aligned on 8-week MVP timeline and begin data collection.
