# Five Whys Analysis: Sm-153 Production Shortfall (Feb 10, 2026)
## Draft for Fact-Gathering — Operational Review

**Incident:** Sm-153 batch produced 130 mCi at calibration (10 AM Monday) vs. 150 mCi target  
**Status:** Root cause investigation ongoing  
**Purpose:** Structure discussion with operations team to collect missing data  

---

## Five Whys Framework

### Why #1: Activity Below Target
**Observation:** Final measured activity was ~20 mCi below target (130 mCi measured vs. 150 mCi target). Measurement uncertainty to be confirmed with QC records.

**Possible explanations:**
- Irradiation received less neutron fluence than expected at 950 kW
- Activity measurement error (less likely; measurement procedure validated)
- Decay calculation error (cross-check counting standards with QC officer)

**Questions for team:**
- [ ] Confirm measurement technique and counting standard traceback
- [ ] Were measurement conditions nominal (sample geometry, counting time, detector calibration)?
- [ ] Any deviation from standard QC procedure that day?

---

### Why #2: Fluence Lower Than Expected
**Observation:** Despite 950 kW power setpoint and correct sample position, neutron flux at CT was observed to be lower than baseline.

**Possible explanations:**
- **Core xenon loading** — elevated Xe-135 from prior operation affects core reactivity (requires increased rod withdrawal to maintain power); may also affect local flux distribution depending on spatial Xe distribution
- **Fuel temperature observation** — instrumented fuel element (IFE) temperature reportedly dropped from ~373°C to ~367°C at constant 950 kW; if confirmed, this may indicate local power redistribution or other core state change
- **Position-specific flux distribution** — CT position may have inherently lower flux (shading, burnup, geometry)
- **Control rod miscalibration** — rod positions were correct numerically but reactivity worth changed?
- **Coolant flow anomaly** — unexpected reduction in pool circulation affecting local flux?

**Questions for team:**
- [ ] What was xenon inventory estimate for Friday end-of-day? Saturday evening? Sunday morning (pre-run)? Sunday evening (post-run shutdown)?
- [ ] What was the shutdown time Sunday? (Critical: Xe-135 peaks ~10-11h post-shutdown, then decays with τ½ ≈ 9.1h)
- [ ] Confirm IFE temperature reading: Was 367°C observed at 950 kW Monday? What is typical IFE temperature at 950 kW under low-xenon conditions? (Establish baseline for comparison)
- [ ] Was coolant flow rate monitored? Any anomalies reported?
- [ ] When was rod calibration last verified? (Within this cycle? Last cycle?)
- [ ] Does CT position have known lower flux vs. RSR or TPNT? Check design documents or previous runs.

---

### Why #3: Why Did Xenon Levels Accumulate Unexpectedly?

**Scenario:** If xenon is a contributing factor, timeline matters.

**I-135 → Xe-135 production chain (standard reactor physics):**
- I-135 half-life ≈ 6.57 hours; decays via β⁻ predominantly to Xe-135
- Xe-135 half-life ≈ 9.14 hours; exceptionally high thermal neutron capture cross-section (~2.65 × 10⁶ barns at 0.0253 eV)
- At reactor power: Xe-135 reaches equilibrium where production (from I-135 decay + direct fission yield) balances destruction (neutron capture + radioactive decay)
- After shutdown: neutron capture ceases, but I-135 continues decaying to Xe-135 → **Xe-135 concentration increases** and peaks approximately 10-11 hours post-shutdown before decaying

**Possible timeline (to be verified against ops log):**
- Friday end-of-week: xenon decaying toward negligible levels if reactor was shutdown
- Saturday: possibly no reactor operation? (Confirm)
- Sunday: reactor operated at power; I-135 and Xe-135 built toward equilibrium
- **Sunday shutdown** (exact time to be confirmed from ops log)
  - At shutdown: I-135 & Xe-135 at equilibrium concentrations for that power level
  - Post-shutdown: Xe-135 **increases** as I-135 decay continues but neutron burnout stops
  - Xe-135 typically **peaks ~10-11 hours after shutdown** (the post-shutdown xenon transient)
- Monday 06:00: If shutdown was Sunday evening (~20:00), Monday 06:00 is ~10 hours post-shutdown
  - This timing corresponds to **near-peak xenon concentration** — the worst case for reactivity
  - After peak, Xe-135 decays with τ½ ≈ 9.1h; full recovery to pre-transient levels requires ~40-50 hours

**Note:** The above timeline is speculative. Actual xenon transient depends on: (1) power level and duration of Sunday run, (2) exact shutdown time, (3) any prior operating history affecting I-135 inventory. Ops log data required to quantify.

**Questions for team:**
- [ ] What time did reactor shutdown Sunday? (Check ops log)
- [ ] Saturday: Was reactor operating? If so, power level and duration?
- [ ] What was power level during Sunday run? What duration at power? (Affects I-135/Xe-135 equilibrium inventory at shutdown)
- [ ] Were any power changes made Sunday evening before shutdown?
- [ ] Approximate I-135/Xe-135 concentration baseline from prior week (if measured)?

---

### Why #4: Why Wasn't This Fluence Reduction Detected **Before** Committing to Monday Production?

**Observation:** If xenon/temperature was problematic Sunday, could production manager have delayed batch Monday morning?

**Current workflow:** Manual assessment based on reactor status, power monitors "look fine," sample position "looks fine."

**Possible information gaps:**
- No explicit xenon level tracking or forecast
- Fuel temperature measured but not integrated into yield prediction
- No comparison between observed temperature and predicted temperature for given xenon state
- Production manager relies on operational intuition, not quantified models

**Questions for team:**
- [ ] Is there a procedure to estimate/track core xenon levels? (Inferred from rod positions + calibration? Measured? Calculated?)
- [ ] Are fuel temperature trends reviewed before production decisions?
- [ ] Were any of these observations available to production manager before 06:00 Monday decision?
- [ ] Would 2-4 hour delay (to ~10:00 AM Monday) have allowed xenon decay to adequate levels?

---

### Why #5: Why Doesn't the System Have Real-Time Anomaly Detection or Pre-Production Validation?

**Observation:** The Feb 10 incident exposed lack of predictive/monitoring capability.

**Possible gaps:**
- **No yield prediction model** — no way to forecast "will this batch hit 150 mCi?" before commitment
- **No live xenon model** — xenon state inferred from rod positions but not formally tracked
- **No real-time anomaly alerts** — operators/manager reportedly unaware of IFE temperature deviation until post-mortem analysis
- **No automated root cause analysis** — only manual retrospective analysis possible after batch completion

**Questions for team:**
- [ ] What would be required to build a xenon tracking system? (Integrate rod calibration data + decay model)
- [ ] Would a yield prediction model be valuable for pre-production decision-making?
- [ ] What alerts should fire during production? (e.g., "Fuel temp 3°C below baseline at this power level")
- [ ] Is real-time DCS data accessible for monitoring and analysis? (Power, fuel temp, rod positions)

---

## Data to Collect (Priority Order)

### Immediate (This Week)
- [ ] Ops log: Exact times for weekend/Sunday reactor operations, shutdown Sunday
- [ ] DCS playback: Power, fuel temperature, rod positions for Friday 00:00 → Monday 12:00
- [ ] Rod calibration: curve date, validity check
- [ ] Coolant flow: normal Monday? Any anomalies?
- [ ] QC records: Counting standard traceback, measurement uncertainty budget

### Secondary (Next Week)
- [ ] Design basis: Expected flux distribution across core positions (CT vs. RSR vs. TPNT)
- [ ] Previous Sm-153 runs: Last 10 batches' power, temperature, final activity (to establish baseline)
- [ ] Xenon reference: Historical core xenon estimates (if available) or design basis curves

### For Model Development (Ongoing)
- [ ] Rod calibration curves + temperature-reactivity relationship (if not already digitized)
- [ ] Fuel element burnup state per ring/position (for burnup-effect analysis)
- [ ] Baseline power-to-fuel-temperature curve at clean core conditions

---

## Open Questions for Bill's Team

**Framed as suppositions (to be confirmed/refuted by data):**

1. **Xenon hypothesis:** Did elevated xenon concentration (from Sunday operation → shutdown → Monday morning) contribute to reduced local flux at the CT position? If so, what fraction of the ~20 mCi shortfall might be attributable to xenon vs. other factors?

2. **Temperature observation:** Is the reported IFE temperature (~367°C vs. typical ~373°C at 950 kW) outside normal operating variability? If confirmed as anomalous, does it correlate with xenon-induced power redistribution, or might other factors (coolant flow, fuel element position, instrumentation drift) contribute?

3. **Position-specific flux:** Is CT position known to have lower flux than power-level alone predicts? Or does this batch represent an outlier?

4. **Detectability:** With a xenon tracking system and pre-production yield prediction, would the shortfall have been forecast Monday morning, allowing rescheduling?

5. **Early warning:** Could operators have detected the fuel temperature anomaly in real-time (by 08:00 AM) if it were being monitored + compared to expected baseline?

---

## Next Steps

- [ ] Collect data from questions above (assign to operations/QC staff)
- [ ] Compile DCS playback + ops log timeline
- [ ] Draft root cause summary once data reviewed
- [ ] Assess: Should we change Monday procedures before next Sm-153 run?
- [ ] **Prepare meeting with Digital Twin team:** How should reactor operations respond? (Process changes, enhanced monitoring, predictive validation, etc.)

---

**Document Status:** Draft for discussion  
**Owner:** Bill Charlton, UT NETL TRIGA Facility  
**Circulation:** Operations team, QA/QC, Digital Twin team  
**Timeline:** Fact-gathering through Feb 12-13; summary by Feb 14

---

## Technical Notes & Caveats

- **Xenon transient physics:** Half-lives cited (I-135 ≈ 6.6h, Xe-135 ≈ 9.1h) are standard values. Actual post-shutdown xenon transient behavior depends on prior power history, operating duration, and core-specific parameters. The ~10-11 hour peak timing is typical but should be verified against facility-specific calculations or measurements.

- **Temperature-flux relationship:** IFE temperature at constant power can vary due to multiple factors including power distribution changes, coolant conditions, and instrumentation effects. Whether a ~6°C deviation is operationally significant depends on historical variability and measurement repeatability at this facility.

- **Flux at irradiation position:** Local neutron flux at CT position depends on global power level, control rod configuration, fuel burnup distribution, and any absorbers (including Xe-135) in the vicinity. Relating global power to local flux requires facility-specific characterization.

- **Measurement uncertainty:** Activity measurements typically carry ±2-5% uncertainty (1σ) depending on technique, geometry, and calibration. A ~20 mCi shortfall on a 150 mCi target (~13%) exceeds typical measurement uncertainty, but the specific uncertainty budget for this measurement should be documented before drawing conclusions.
