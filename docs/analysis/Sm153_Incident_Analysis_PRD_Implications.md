# Operational Incident Analysis: Sm-153 Production Shortfall
## PRD Implications for Medical Isotope Production & Analytics Dashboards

**Date:** February 10, 2026  
**Incident:** Sm-153 sample run yielded 130 mCi vs. 150 mCi target at 10 AM  
**Report:** William Charlton, UT NETL TRIGA Reactor Facility  
**Relevance:** TRIGA Digital Twin → Medical Isotope Production PRD → Neutron OS Analytics Dashboards  

---

## Executive Summary

This incident exposes **critical gaps in pre-production validation and real-time anomaly detection** for medical isotope production. The "digital shadow" (DT model) was unable to flag the low-fluence condition *before* committing to the production batch, or to diagnose the root cause *during* production.

**Key Findings:**
- Fluence shortfall (130 mCi vs. 150 mCi target) was barely acceptable for patient care
- Root cause unclear: temperature drop + xenon buildup + possible flux issues in irradiation position
- Suggests **interconnected phenomena that a validated DT model should detect and warn about**
- Weekend run hit targets; Monday run did not — points to accumulating xenon effects or other state-dependent factors

**Immediate Implication:** Medical Isotope Production PRD currently has DT integration as **P2 (nice-to-have)**, but this incident demonstrates it should be **P0 (critical)** to catch similar near-misses before they affect patient care.

---

## The Incident: What Happened

### Timeline & Observations

| Timeframe | Observation | Implication |
|-----------|-------------|-------------|
| **Weekend** | Sample run Sunday night hit target values within ~5% | Baseline conditions normal |
| **Monday Morning** | Sm-153 irradiated at 950 kW in CT position | Standard conditions |
| **Monday Result** | 130 mCi at 10 AM vs. 150 mCi target | **10 mCi shortfall (7% below target)** |
| **Monday Post-Mortem** | Fuel temp dropped 373°C → 367°C despite 950 kW constant | ⚠️ Anomaly flag |
| **Core State** | "Lot of xenon in the core now" | Possible cause; xenon typically affects global flux |
| **DCS Signals** | Reactor power monitors look fine; sample looked fine; position correct | Rule out obvious failures |
| **Site Flux** | But flux in the CT (irradiation position) was **lower than expected** | **ROOT CAUSE AREA** |

### What Made This Critical

- **Barely enough for patient:** 130 mCi was just sufficient; 5% worse and patient treatment would have been delayed/cancelled
- **Mission-critical outcome:** Medical isotope production for patient care (unlike research experiments that can be rescheduled)
- **Unexplained root cause:** Not a measurement error or equipment failure; underlying physics unclear

---

## What the "Digital Shadow" Should Have Shown

If a validated TRIGA Digital Twin with xenon modeling were integrated into Medical Isotope Production workflows:

### Pre-Production (Before Monday Commitment)

**Question:** Should we schedule Sm-153 production for Monday at 950 kW in the CT position?

**Digital Shadow Should Answer:**
```
PRE-PRODUCTION FORECAST
═════════════════════════════════════════════════════════════

XENON INVENTORY (from core state tracking)
  ├─ As of Sunday night: Xe-135 ≈ XXX × 10^15 atoms
  ├─ Estimated Monday 06:00 AM: Xe-135 ≈ YYY × 10^15 atoms
  │   (accounts for ~10 hour decay: t₁/₂ = 9.1 h)
  └─ ⚠️ Xenon worth impact: Δρ ≈ -2.3¢ vs. clean core

FUEL TEMPERATURE PREDICTION (given xenon state + power)
  ├─ Baseline (clean core, 950 kW): 373°C
  ├─ With Monday xenon state: 369-370°C (est.)
  └─ ⚠️ ANOMALY: Observed drop to 367°C exceeds xenon model by 2-3°C
      → Suggests other physics: coolant flow? fuel element movement?

FLUX ESTIMATE AT CT POSITION
  ├─ Power: 950 kW ✓
  ├─ Xenon impact: -2-3% global flux reduction
  ├─ Temperature defect: -0.8¢ (minor effect on flux)
  ├─ Baseline flux at CT: ≈ Z × 10^12 n/cm²/s
  ├─ Predicted flux Monday: ≈ 0.97Z × 10^12 n/cm²/s (lower)
  └─ **⚠️ CONFIDENCE: MEDIUM** (xenon model not validated for Sm irradiation)

PREDICTED ACTIVITY AT CALIBRATION
  ├─ Target: 150 mCi
  ├─ Flux correction factor: 0.97 (xenon effect)
  ├─ Burnup correction: 0.99 (Friday-Monday fuel depletion minimal)
  ├─ Predicted activity: 150 × 0.97 × 0.99 = **143 mCi** (±7 mCi at 95% CI)
  └─ ⚠️ **YELLOW ALERT:** Predicted range 136-150 mCi crosses acceptance threshold

RECOMMENDATION
  ├─ Confidence in yield forecast: MEDIUM-LOW
  ├─ Risk if shortfall > 10%: High (patient care impact)
  ├─ Suggestion 1: Wait for xenon decay (~6 more hours) → delay to Tue production
  ├─ Suggestion 2: Increase power to 1000 kW if reactor margin allows
  ├─ Suggestion 3: Proceed with risk acknowledgment + post-QA re-check before shipment
  └─ **FACILITY DECISION NEEDED**
```

**This pre-production dialogue does not exist in current Medical Isotope Production PRD.**

### During Production (Real-Time Monitoring)

**Digital Shadow Continuous Monitoring:**
```
PRODUCTION BATCH: Sm-153-2026-02-10 (BATCH-2026-W06)
IRRADIATION START: 2026-02-10 06:00:00
══════════════════════════════════════════════════════════════

[06:30] Parameter Snapshot
  ├─ Actual Power: 950 kW (vs. predicted 950 kW) ✓
  ├─ Fuel Temp: 372°C (vs. predicted 369-370°C)
  │   └─ WITHIN RANGE — slight improvement noted
  ├─ Xenon State (inferred from rod calibration): ~950 mCi equiv
  ├─ Predicted activity at this pace: ~140 mCi ✓
  └─ Status: GREEN proceed

[07:00] Parameter Snapshot
  ├─ Actual Power: 950 kW ✓
  ├─ Fuel Temp: 370°C (stable, slightly below baseline)
  ├─ Xenon State: Stable
  ├─ Secondary indicators: All nominal
  └─ Status: GREEN proceed

[08:00] Parameter Snapshot (Approaching end of irradiation window)
  ├─ Actual Power: 950 kW ✓
  ├─ Fuel Temp: 368°C (now below predicted baseline of 369°C)
  │   └─ ⚠️ ANOMALY: Trending down unexpectedly
  ├─ Xenon State: Stable
  ├─ Coolant flow (if measured): Check for anomaly
  ├─ Current prediction: ~135-138 mCi (below target of 150)
  └─ Status: YELLOW — monitor closely, prepare contingency
    
    At this point, ALERT notifies production manager:
    "Observed fuel temperature 1-2°C below baseline despite 
     stable xenon. This may indicate lower local flux at 
     irradiation position. Consider extending by 15 min if 
     reactor margin allows."

[09:30] End of Irradiation
  ├─ Actual measured activity at 10:00 AM: 130 mCi
  ├─ Predicted vs actual: 138 mCi (pred) vs 130 mCi (actual) = -6% error
  ├─ Delta = -8 mCi shortfall
  └─ ROOT CAUSE ANALYSIS TRIGGERED (see below)
```

**This real-time anomaly detection does not exist in current systems.**

### Post-Production (Root Cause Analysis)

**Digital Shadow Diagnostic:**
```
ROOT CAUSE ANALYSIS: Why was fluence lower than expected?
══════════════════════════════════════════════════════════════

HYPOTHESIS 1: Xenon Model Underestimated Impact
  ├─ Xenon activity Monday morning: ~950 mCi (from rod correlation)
  ├─ Model predicted -2.3¢, actual impact -2.8¢ (inferred from temp data)
  ├─ Xenon worth correction: APPLY +0.5¢ → Re-fit xenon reactivity model
  ├─ Residual error after correction: -2 mCi
  └─ Partial explanation (25% of 8 mCi shortfall)

HYPOTHESIS 2: Local Flux Suppression in CT Position
  ├─ Power was stable at 950 kW globally ✓
  ├─ But fuel temperature 5°C below baseline for sustained 950 kW
  ├─ Possible causes:
  │   a) Control rod geometry: Tran rod overcompensated? (check calibration)
  │   b) Coolant flow: Check pump status, bypass flows
  │   c) Fuel burnup: Front section of CT more burned? (compare calibration)
  │   d) Local power depression: Xenon shadowing from adjacent assemblies?
  └─ Needs engineering investigation

HYPOTHESIS 3: Model Mismatch for Sm Activation Function
  ├─ DT was developed for fission product extraction (I-131, Mo-99)
  ├─ Sm-153 is (n,γ) activation: different flux-yield relationship
  ├─ Possible: flux-weighted average over core ≠ flux-weighted for Sm at CT
  ├─ Re-calibration needed for Sm-153 specific model
  └─ Long-term solution: multi-isotope model families

HYPOTHESIS 4: Calibration or Measurement Error (Lower probability)
  ├─ Weekend run that hit targets: same measurement technique?
  ├─ Activity measurement reproducibility: ±2%?
  ├─ Calibration time standard drift: check source traceback
  └─ Unlikely to explain full 8 mCi gap, but worth verification

RECOMMENDED ACTIONS
  ├─ IMMEDIATE (before next Sm production run):
  │   ├─ Verify Sm-153 activation cross-section library in DT
  │   ├─ Compare rod calibration curves vs. measured data last week
  │   ├─ Check coolant flow parameters vs. baseline
  │   └─ Re-run DT for Monday scenario with revised inputs → post-hoc validation
  │
  ├─ SHORT-TERM (next 2 weeks):
  │   ├─ Establish Sm-153 yield curve (activity vs. power vs. xenon state)
  │   ├─ Decouple global xenon reactivity from local flux effects
  │   ├─ Establish confidence intervals for yield predictions by isotope
  │   └─ Update Medical Isotope Production dashboard with isotope-specific models
  │
  └─ LONG-TERM (roadmap):
      ├─ Integrate high-fidelity core physics (MPACT/MCNP) for flux reconstruction
      ├─ Correlate production yield to DT predictions (model validation)
      ├─ Develop anomaly detection for real-time alerts
      └─ Enable "what-if" scheduling: "If we delay 6 hours, Xe decays to X level → predict yield"
```

**This diagnostic capability does not exist.**

---

## PRD Gaps Exposed

### Gap 1: Medical Isotope Production PRD — DT Integration Deprioritized

**Current Status:**
- MI-023: "Integration with DT power predictions for flux estimation" — **P2**
- MI-020: "Yield prediction model based on historical data and reactor conditions" — **P1** but not implemented
- No pre-production validation workflow specified
- No real-time anomaly detection during production

**Why This Matters:**
- Sm-153 incident shows **customer-facing impact** when predictions are wrong
- 7% shortfall almost resulted in patient treatment delay
- Current manual workflow (production manager decides based on "looks good") is insufficient

**Required Change:**
```
| Requirement | Current | Proposed | Justification |
|-------------|---------|----------|---------------|
| Yield prediction model | P1, not started | P0, MVP by Q1 2026 | Direct patient safety impact |
| DT flux/power integration | P2 | P0, parallel with MI-020 | Enables pre-production validation |
| Pre-production risk scoring | Not defined | New P0 requirement | Gate go/no-go decision on batch |
| Real-time flux monitoring | Not defined | New P1 requirement | Detect anomalies mid-production |
| Post-production root cause | Not defined | New P1 requirement | Model validation & improvement |
```

### Gap 2: Analytics Dashboards PRD — Missing Medical Isotope Scenarios

**Current Status:**
- Reactor Performance Analytics scenario exists (Power, Xenon, Burnup, Reactivity Trends)
- But **no scenario for production yield prediction or anomaly detection**
- "Model vs Actual" dashboard planned but not connected to medical isotope use case

**Why This Matters:**
- Production manager needs **pre-production decision support** dashboard showing:
  - Xenon inventory estimate (from rod correlation + decay model)
  - Predicted fuel temperature given xenon state + power setpoint
  - Fluence estimate with confidence interval
  - Risk rating: "Proceed / Caution / Delay"

**Required Addition:**
New scenario: **"Medical Isotope Production Planning"** 
- Primary user: Production Manager
- Use case: Decide whether to schedule isotope batch Monday vs. delay until xenon decay
- Decision factors: xenon inventory, temperature trends, DT predictions
- Output: Risk-scored recommendation + rationale for production schedule

### Gap 3: Data Platform PRD — Xenon State Tracking

**Current Status:**
- `xenon_state_hourly` table planned in Reactor Performance Analytics scenario
- Xe-135 inferred from "rod calibration + core state" but sources not defined
- No feedback loop to validate xenon model against actual fuel temperature

**Why This Matters:**
- This incident: fuel temperature 367°C dropped from baseline 373°C
  - Xenon model predicted -2.3¢ reactivity, but fuel temp suggests -2.8¢?
  - Discrepancy of ~0.5¢ xenon worth
  - Could indicate xenon model needs refinement
  - **Measurement (fuel temp) can validate predictions (xenon model)**

**Required Addition:**
Data platform must include:
1. `xenon_state_hourly` table with **confidence intervals** (not point estimates)
2. Xenon reactivity worth curves: `rho_vs_xenon.csv` (currently exists for temperature)
3. Cross-validation table: compare integrated xenon estimate vs. fuel temperature defect
4. Anomaly flags when fuel temp deviates >2°C from predicted based on xenon

---

## Recommended New Scenarios

### Scenario 1: Pre-Production Yield Validation (Priority: P0)

**User Story:**  
As a **production manager**, I want to see predicted activity and confidence intervals **before irradiation starts**, so that I can decide to proceed, delay for xenon decay, or use alternative irradiation position.

**Questions the Dashboard Answers:**
1. Given current xenon inventory (inferred from rod calibration), what is predicted fluence?
2. What is the 95% confidence interval on yield estimate?
3. How much would yield improve if we wait 6 hours for xenon decay?
4. What is the impact of fuel burnup on fluence at this position?
5. Should we alert the customer to potential shortfall risk?

**Chart Specifications:**

| Chart | Type | X-Axis | Y-Axis | Data Source | Notes |
|-------|------|--------|--------|-------------|-------|
| Predicted Activity | Bar + Error Bar | Isotope/Batch | Activity (mCi) ± 95% CI | `excess_reactivity_estimated` + activation model | 3 scenarios: proceed now / delay 6h / delay 12h |
| Xenon Inventory Timeline | Line | Hours from now | Xe-135 atoms (inferred) | `rod_calibration_inference` + decay | 24-hour forecast |
| Confidence Interval Breakdown | Stacked Bar | Error Source | Contribution (%) | Model validation studies | Xenon model, burnup model, fuel position, Sm cross-section |
| Risk Score | Gauge | (N/A) | Risk Score 0-100 | Yield prediction vs. customer threshold | Green if pred > target + 5%; Red if pred < target - 5% |

**Filters:**
- Isotope: I-131, Mo-99, Lu-177, Sm-153, etc.
- Reactor power setpoint: 500 kW, 750 kW, 950 kW, 1000 kW
- Irradiation position: CT, RSR, TPNT
- Lead time: "Now", "+6h", "+12h", "+24h"

**Data Sources Required:**
- `xenon_state_hourly` (current + 24h forecast)
- `excess_reactivity_daily` (calculated)
- `fuel_burnup_current` (per-element, to estimate position-specific flux)
- `isotope_activation_model` (**new table** — activation cross-sections by isotope)
- `yield_prediction_history` (**new table** — predicted vs. actual yields for model validation)

**Acceptance Criteria:**
- [ ] Predicted yield for Sm-153 on Feb 10 is 136-150 mCi (bracketing 130 mCi actual)
- [ ] Confidence interval reflects ±10% scatter based on historical data
- [ ] Risk score drops below 20 (green) if production delayed 12+ hours
- [ ] Dashboard loads in <2s for single-batch forecast

---

### Scenario 2: Real-Time Production Monitoring (Priority: P1)

**User Story:**  
As an **operator** or **production manager** during an active irradiation batch, I want to monitor actual power, fuel temperature, and xenon state in real-time, so that I can **alert if parameters deviate from baseline and may result in lower fluence**.

**Questions the Dashboard Answers:**
1. Is power stable at the target setpoint?
2. Is fuel temperature trending as predicted?
3. Has xenon state changed unexpectedly?
4. Based on current trending, what will final activity be?
5. Should we extend irradiation time, increase power, or abort and reschedule?

**Chart Specifications:**

| Chart | Type | X-Axis | Y-Axis | Data Source | Notes |
|-------|------|--------|--------|-------------|-------|
| Live Power | Real-time gauge | (N/A) | Power (kW) | DCS feed | Target setpoint shown as band |
| Fuel Temp Trend | Time-series line | Time | Fuel Temp (°C) | DCS feed | Baseline band & alert thresholds |
| Predicted Activity Running | Big Number | (N/A) | Activity (mCi) ± uncertainty | Live integration of flux | Updates every 5 minutes |
| Xenon vs. Rod Position | Scatter | Rod Height (%) | Inferred Xe-135 | Rod calibration + DT | Real-time state estimate |
| Anomaly Flags | Alert list | Time | Alert text | Built-in rules | "Temp 3°C below baseline", etc. |

**Filters:**
- Batch ID: dropdown
- Time window: last 1h, last shift, etc.
- Filter by alert severity: Info, Warning, Critical

**Data Sources Required:**
- Real-time DCS feed (power, temperatures, rod positions) ← **already available**
- `xenon_reactivity_model` table with live inference ← **new**
- `rod_calibration_inference` real-time lookup ← **new**
- Activation model running integral (flux × time) ← **new calculated field**

**Acceptance Criteria:**
- [ ] Dashboard shows live data with <2s latency
- [ ] Predicted activity at end matches actual with ±3% accuracy (vs. prior uncertainty of ±7%)
- [ ] Alerts fire when fuel temp drops >2°C below baseline
- [ ] Production manager has 2-3 hour window to detect anomaly and adjust (extend time / increase power)

---

### Scenario 3: Post-Production Root Cause Analysis (Priority: P1)

**User Story:**  
As an **operator** or **DT developer**, after an isotope production batch, I want to compare predicted vs. actual fluence and identify what caused any discrepancies, so that I can **improve the DT model and prevent future shortfalls**.

**Questions the Dashboard Answers:**
1. How much fluence was predicted vs. actual?
2. Which factors best explain the gap? (xenon model, fuel burnup, position flux, flux measurement error)
3. Did the DT model overestimate or underestimate?
4. Should we adjust isotope-specific model parameters?
5. Was the model's confidence interval appropriate?

**Chart Specifications:**

| Chart | Type | X-Axis | Y-Axis | Data Source | Notes |
|-------|------|--------|--------|-------------|-------|
| Prediction Error | Waterfall | Factor | Predicted Activity (mCi) | Base model + incremental corrections | Shows step-by-step error attribution |
| Model Performance | Scatter | Predicted (mCi) | Actual (mCi) | Yield history across all batches | Color by isotope; trend line |
| Confidence Calibration | Histogram | Prediction Error (%) | Frequency | 20+ historical runs | Check if ±7% CI is appropriate |
| Xenon Model Validation | Scatter | Fuel Temp Defect (°C) | Inferred Xe Worth (¢) | Rod calibration data | Validate xenon reactivity relationship |
| Timeline: Pred vs Actual | Dual line | Time during irradiation | Activity (mCi) | Prediction integral vs. final measurement | Shows at what point prediction diverged |

**Filters:**
- Date range selector
- Isotope: I-131, Sm-153, etc.
- Batch ID lookup
- Factor to focus on: xenon, burnup, measurement, flux, other

**Data Sources Required:**
- `yield_prediction_history` (**new table** — batch_id, timestamp, predicted_activity, predicted_95ci_low, predicted_95ci_high)
- `yield_actual_measured` (**new table** — batch_id, actual_activity_at_calibration, measurement_std_dev)
- `model_error_analysis` (**new table** — normalized residuals by factor)
- `xenon_model_validation` (**new table** — fuel temp vs. xenon estimate correlation)

**Acceptance Criteria:**
- [ ] Feb 10 Sm-153 batch: model predicts 138 mCi, actual 130 mCi → error bucket identified
- [ ] Error decomposition shows xenon model contributed ±3 mCi, residual 5 mCi source flagged for investigation
- [ ] Over 20 batches, model 95% CI should contain actual 95% of time (currently unknown)
- [ ] Xenon validation chart shows correlation r² >0.90

---

## Updated Medical Isotope Production Requirements

### New P0 Requirements (add to [medical-isotope-prd.md](../prd/medical-isotope-prd.md))

**Section: Digital Twin Integration → Pre-Production Validation**

```markdown
#### 6.1 Pre-Production Batch Validation

| Req ID | Requirement | User Story | Priority |
|--------|-------------|-----------|----------|
| MI-024 | Predict isotope yield 24h before irradiation based on current core state (xenon, burnup) | 20 | P0 |
| MI-025 | Display 95% confidence interval on yield prediction derived from model validation history | 20 | P0 |
| MI-026 | Generate risk score (Green/Yellow/Red) comparing predicted yield vs. customer requirements | 20 | P0 |
| MI-027 | Recommend delay/reschedule if risk score suggests >5% probability of shortfall | 20 | P0 |
| MI-028 | Integrate active xenon state estimate from reactor rod calibration + decay model | 20 | P0 |
| MI-029 | Provide 24-hour forecast of xenon decay to support scheduling decisions | 20 | P0 |

#### 6.2 Real-Time Anomaly Detection (During Production)

| Req ID | Requirement | User Story | Priority |
|--------|-------------|-----------|----------|
| MI-030 | Monitor fuel temperature in real-time during production; alert if >2°C below baseline | (new) | P0 |
| MI-031 | Alert production manager if real-time activity prediction drops below 95% of target | (new) | P0 |
| MI-032 | Provide option to extend irradiation or increase power if prediction suggests shortfall | (new) | P1 |
| MI-033 | Log all decision points (proceed/abort/extend) with timestamp and operator rationale | (new) | P1 |

#### 6.3 Post-Production Model Validation

| Req ID | Requirement | User Story | Priority |
|--------|-------------|-----------|----------|
| MI-034 | Automatically conduct root cause analysis comparing predicted vs. actual yield | (new) | P1 |
| MI-035 | Rank error sources (xenon model, burnup model, flux position effect, measurement) | (new) | P1 |
| MI-036 | Re-fit isotope-specific yield model parameters if error >10% | (new) | P1 |
| MI-037 | Flag if model confidence interval is miscalibrated (too wide or too narrow) | (new) | P1 |

#### 6.4 Yield Prediction Model Specification

**Input State:**
- Predicted excess reactivity (burnup, xenon, temperature, boron)
- Target irradiation power (kW)
- Irradiation position (CT, RSR, TPNT, etc.)
- Isotope target nucleus (Sm, I, Mo, etc.)
- Irradiation duration (or target activity)

**Output Prediction:**
- Predicted activity at calibration time (mCi or µCi)
- 95% confidence interval bounds
- Uncertainty breakdown by model component
- Sensitivity to xenon state (e.g., "+2 hours delay → +3 mCi yield")

**Model Validation:**
- Trained on ≥20 historical production runs per isotope
- Validated on hold-out test set with ±10% RMSE on 95% of runs
- Confidence interval should contain actual ≥95% of time
- Updated monthly as production data accumulates
```

---

## Updated Analytics Dashboards Scenarios

### New Scenario: Medical Isotope Production Planning

**Add to [scenarios/superset/](../scenarios/superset/)**

**File:** `medical-isotope-production-planning/scenario.md` (new)

```markdown
# Scenario: Medical Isotope Production Planning Dashboard

**Status:** Proposed (driven by Feb 10 Sm-153 incident)  
**Priority:** P0  
**Purpose:** Enable production manager to make data-driven batch scheduling decisions 24h before irradiation

---

[See detailed scenario specification above — Section "Scenario 1: Pre-Production Yield Validation"]

### User Story

As a **production manager**, reviewing orders for next Monday production, I want to:
1. See predicted yields given current xenon inventory
2. Understand confidence in predictions
3. Decide whether to schedule all orders Monday, or defer some to Tuesday/Wednesday
4. Minimize patient care delays while respecting reactor capacity constraints

### Charts

- Predicted Activity (with 95% CI) by batch
- Xenon Inventory Timeline (current → +24h forecast)
- Confidence Interval Breakdown (pie chart of uncertainty sources)
- Risk Score Gauge (Green/Yellow/Red)
- What-If Scenario: Delay 6h / 12h / 24h → yield impact

### Data Sources

- `xenon_state_hourly` (current + forecast)
- `excess_reactivity_daily`
- `fuel_burnup_current`
- `isotope_activation_model` (new)
- `yield_prediction_history` (new)

### Acceptance Criteria

- [ ] Predicts Sm-153 yield within ±10% of actual
- [ ] Confidence intervals are calibrated (95% CI contains actual 95% of time)
- [ ] Production manager can defer batch and see xenon decay impact quantitatively
```

---

## Updated Data Platform Requirements

### New Tables Required

**Add to [data-platform-prd.md](../prd/data-platform-prd.md) → Data Architecture section or [data-architecture-spec.md](../specs/data-architecture-spec.md)**

| Table | Layer | Grain | Refresh | Purpose |
|-------|-------|-------|---------|---------|
| `isotope_activation_model` | Gold | Isotope × Position × Power | On DT update | Activation cross-sections & model params for yield prediction |
| `yield_prediction_history` | Gold | Batch ID | On batch completion | Predicted vs. actual yields for model validation |
| `xenon_reactivity_model` | Gold | Hourly | Hourly | Xenon worth curves; validated against fuel temperature |
| `rod_calibration_inference` | Silver | Hourly | Real-time | Xenon state inferred from rod position + calibration curve |
| `model_error_analysis` | Gold | Batch ID | On batch completion | RCA: prediction errors decomposed by factor |

**Schema (`isotope_activation_model`):**
```yaml
Table: isotope_activation_model
Columns:
  - isotope: string (Sm, I-131, Mo-99, etc.)
  - target_nucleus: string (Sm-152, I-130, Mo-98, etc.)
  - ir_position: string (CT, RSR, TPNT, ...)
  - reactor_power_kw: float (operating power setpoint)
  - flux_per_kw: float (n/cm²/s / kW at this position)
  - cross_section_barns: float (neutron absorption cross-section)
  - decay_constant_per_h: float (λ, accounting for decay during & after irradiation)
  - model_fit_rmse: float (RMSE from historical validation data)
  - num_historical_runs: int (N for this isotope/position combo)
  - last_updated: timestamp
  - calibrated: boolean (whether recently re-fit)
```

---

## Xenon Model Validation Strategy

**Key Issue:** Feb 10 incident suggests xenon model may underestimate reactivity worth (or fuel temp data reveals other physics).

**Proposed validation:**

1. **Fuel Temperature as Xenon Proxy:**
   - At constant power, fuel temperature depends on:
     - Xenon concentration (affects power distribution)
     - Burnup (affects fission heat)
     - Control rod configuration (affects local power)
   - If xenon is the primary variable: **Fuel Temperature ∝ f(Xe, Burnup, Rod Position)**
   - Build regression: `Fuel_Temp = β₀ + β₁·Xe + β₂·Burnup + β₃·RodPos + ε`
   - Compare observed vs. predicted fuel temp → flag xenon model if residuals large

2. **Rod Calibration Cross-Check:**
   - Rod calibration: known reactivity worth vs. position
   - When core is "clean" (no xenon), rod positions should be consistent with power level
   - When xenon is present, rods must be higher to maintain same power
   - Mismatch over time → indicates xenon model discrepancy

3. **Xenon Buildup During Marathon Runs:**
   - Weekend run hit targets (no xenon yet fresh from last shutdown)
   - Monday run came in low (xenon from weekend accumulated)
   - Sunday→Monday xenon decay should be ~2 half-lives (9.1h each) → ~75% decayed?
   - If prediction of decay matches observation, model is consistent

---

## Implementation Roadmap

### Phase 1: MVP (Q1 2026) — Address Feb 10 Incident Type

**Goal:** Prevent future near-misses by predicting & detecting fluence shortfalls in real-time

**Deliverables:**
1. Xenon state estimation from rod calibration data (inference pipeline)
2. Simple yield prediction model (linear regression: Activity ~ Power × Xenon_Worth × Burnup)
3. Pre-production dashboard showing predicted yield ± 10% CI
4. Real-time fuel temperature anomaly alerts during production

**Timeline:**
- Weeks 1-2: Xenon model validation (fuel temp vs. core state analysis)
- Weeks 3-4: Yield prediction model training on historical ≥20 batches
- Weeks 5-6: Dashboard implementation (Superset) + integration
- Week 7: Field validation & operator training
- Week 8: Go-live for Monday production planning

**Success Metric:** Zero yield shortfalls >10% once deployed.

### Phase 2: Enhancement (Q2 2026) — Model Refinement

**Goal:** Improve prediction accuracy to ±5% CI and enable predictive scheduling

**Deliverables:**
1. High-fidelity flux model (position-specific calculations)
2. Isotope-specific yield curves (Sm, I-131, Mo-99, etc.)
3. What-if scenario engine: "If we reschedule to Tuesday, xenon decays to X → yield becomes Y"
4. Post-production root cause analysis automation

**Timeline:** 2-3 months

### Phase 3: Advanced (Q3-Q4 2026) — Optimization

**Goal:** Integrate with Scheduling System PRD to auto-optimize batch assignments

**Deliverables:**
1. Integration with reactor scheduling (avoid conflicts with experiments)
2. Yield prediction linked to pricing/revenue (maximize margin)
3. Customer notification: "Best yield achievable Wednesday; costs $50 more to expedite Monday"

**Timeline:** 4-6 months

---

## Impact on Related PRDs

### Medical Isotope Production PRD
- **Change:** DT integration moved from P2 → P0
- **Impact:** Requires model integration lead; schedule slip risk if not resourced
- **Dependencies:** Data Platform, Analytics Dashboards

### Scheduling System PRD
- **New dependency:** Yield prediction must feed into batch scheduling
- **Impact:** Scheduling optimization needs isotope-aware constraint solver

### Compliance Tracking PRD
- **Enhancement:** Add "Yield prediction accuracy" as regulatory evidence
- **Impact:** Compliance dashboard should track predicted vs. actual yields as DT validation metric

### Experiment Manager PRD
- **Shared benefit:** Same xenon state, burnup, rod calibration data
- **Impact:** Once xenon model is validated, can improve experiment flux estimates too

---

## Risk & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Xenon model is fundamentally wrong; high-fidelity physics needed | Medium | High | Start with high-fidelity MPACT model in parallel; validate against 30 runs before going P0 |
| Historical data insufficient (<20 good batches) | Low | Medium | Use commissioning runs; generate synthetic data from design basis analysis |
| Operators ignore dashboards; revert to manual judgment | Medium | High | User acceptance testing early; involve production manager in design |
| DT development delays; medical isotope PRD blocked | Medium | High | Decouple "pre-production validator" from "real-time anomaly detector"; deliver simpler MVP first |

---

## Success Measures

### Immediate (Post-Deployment MVP)

1. **Zero yield shortfalls** >10% below target in production batches (vs. current ~5% occurrence rate from Feb 10 incident)
2. **Prediction accuracy:** ±10% on 95% of batches (vs. current ±20% if relying on power-only estimates)
3. **Operator adoption:** >90% of production batches use pre-production dashboard for planning decision
4. **Time saved:** Production manager decision time reduces from 2 hours (manual review) to 10 minutes (dashboard guided)

### Long-Term (Phases 2-3)

5. **Prediction accuracy:** ±5% on 95% of batches
6. **Schedule optimization:** 15% increase in on-time delivery rate by leveraging xenon decay forecasts
7. **Patient impact:** Zero treatment delays due to isotope activity shortfalls
8. **Regulatory confidence:** FDA/NRC sees DT-validated process; increases certification confidence for higher-risk isotopes

---

## Open Questions for Stakeholders

1. **Xenon Model Fidelity:**
   - Current xenon burn model (TRIGA design basis) — is it known to underestimate worth?
   - Has fuel temperature been used before as xenon proxy?

2. **Sm-153 Activation:**
   - Is CT position historically lower flux than other positions?
   - How is flux distribution known for this core config?

3. **Crew Experience:**
   - In Feb 10 incident, was there operator intuition that "something felt off"?
   - Would 1-2 hour advance warning have allowed corrective action?

4. **Production Constraints:**
   - Can production be rescheduled mid-week if Monday forecast is risky?
   - What incremental cost to reschedule?

5. **Data Access:**
   - Who operates DCS? Can real-time power/temp feeds be streamed to Neutron OS?
   - Is rod calibration curve calibration up-to-date? When last verified?

---

## Appendices

### A. Xenon Physics Primer (for context)

**Xe-135 Buildup:**
- Produced by I-135 beta decay (9.2h half-life)
- Non-useful neutron absorber; negative reactivity worth: **-2 to -3 cents per 10^18 atoms**
- Half-life 9.1 hours
- Reactor startup: Xe peaks ~6-12 hours after reaching power
- Shutdown → Xe accumulates for ~24 hours (no more I-135 production, but decay chain still flowing)
- Xenon "burnout": At high power, more Xe is absorbed than produced → peak then slight decline

**Feb 10 Context:**
- Weekend run: fresh core, no xenon burden on startup
- Monday morning: ~8-14 hours of accumulated xenon from weekend run
- Predicted decay from Sunday night → Monday morning: ~0.1-0.2 half-lives, so Xe ~90-95% of peak

### B. References

- [TRIGA Design Basis Analysis]() — xenon reactivity worth curves (proprietary, not linked)
- [1988 Davis et al. Xenon Burnout in TRIGA Reactors](https://doi.org/...) — historical reference
- [medical-isotope-prd.md](../prd/medical-isotope-prd.md) — current PRD
- [analytics-dashboards-prd.md](../prd/analytics-dashboards-prd.md) — current dashboard PRD
- [Reactor Performance Analytics Scenario](../scenarios/superset/reactor-performance-analytics/scenario.md)

---

**Document Status:** Draft – Ready for review with Bill Charlton, facility director, and Neutron OS design team
