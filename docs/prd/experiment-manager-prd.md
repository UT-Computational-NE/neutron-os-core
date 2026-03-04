Table of Contents

Product Requirements Document: Experiment Manager

Module: Experiment & Sample Tracking + Scheduling   Status: Draft   Last Updated: January 22, 2026   Stakeholder Input: Khiloni Shah, Nick Luciano (Jan 2026)   Related Module:  (shared backend, separate workflow)   Parent: Medical Isotope ProductionExecutive PRD

Executive Summary

The Experiment Manager provides digital tracking of samples from preparation through irradiation, decay, counting, and analysis. It focuses exclusively on experiment lifecycle management — sample metadata, state tracking, chain of custody, and result correlation. The module integrates with the  for reactor time allocation and the  for regulatory requirements, but does not own these cross-cutting concerns.Scheduling SystemCompliance Tracking System

Design Philosophy:

• Minimize data entry through smart defaults, inference from past experiments, and AI assistance

• Focus on experiment data — sample properties, irradiation parameters, results, chain of custody

• Delegate cross-cutting concerns — scheduling, compliance, and notifications handled by dedicated systems

• Multi-facility configurable — core system works for any research reactor; facility-specific dropdowns are configuration

System Boundaries

What Experiment Manager OWNS

What Experiment Manager USES (Not Owns)

Integration Architecture

User Journey Map

Researcher: Planning to Analysis

Sample State Machine

Experiment Data Flow

Stakeholder Insights

Current State (from Khiloni Shah)

"It's a combination of things. Some information – sample type, sample mass, maximum reactor power you might need, irradiation time, facility, in-core/ex-core, etc. are recorded in reactor operations requests. However, depending on the irradiation you're doing, typically you include a variety of things you might do with that ops request so that it can follow cover more than one type of experiment."

"If you're using an ops request for multiple experiments, you're likely keeping track of the experiment details on your own – this can vary widely from person to person – spreadsheet, handwritten, etc."

"During irradiations, each facility location has a binder that allows you to write in some information – date, time, researcher doing experiment, reactor power level, facility, dose rate."

"For post-processing data analysis, this is also researcher dependent and experiment dependent... The way the data is analyzed depends on the researcher, but the most common is probably some type of spreadsheet."

Key Insight from Jim (Reactor Operations)

"We have a schedule of Authorized Experiments. These experiments are authorized by the ROC (Reactor Oversight Committee) after review through NETL Staff (Reactor Manager/HP/Director - Then ROC chair). Routine Experiments are performed as they are covered under an Authorized Experiment."

"We attempted this a while back using MS Access. Again, I believe it would be useful to have a modeler/designer come to the NETL and investigate and review our current system. Then begin."

Experiment Authorization Workflow (from Jim)

Two Authorization Paths:

Request to Operate (RTO) Process:

• Researcher submits RTO form with experiment details

• For Routine Experiments: RM/SSRO reviews against Authorized Experiment list

• For new experiments: Full ROC review (monthly meeting cycle)

• System tracks which Authorized Experiment covers each Routine Experiment

• RTO number (4-digit) links scheduling and ops log entries

Design Implication: The system must maintain a registry of Authorized Experiments and validate that Routine Experiments reference a valid authorization.

User Stories

Primary Users

User Stories: Sample Tracking

• As a researcher, I want to log sample metadata before irradiation so that I don't have to re-enter information for each step.

• As a researcher, I want pre-populated dropdowns for facilities so that I use consistent naming.

• As a reactor operator, I want to see expected sample activities/dose rates so that I can prepare appropriate handling procedures.

• As a PI, I want to track beam time usage across my students/projects so that I can report to sponsors.

• As a compliance officer, I want immutable records of what was irradiated, when, and by whom.

• As a compliance officer, I want to generate NRC evidence packages covering 2 years of experiment records with consistent formatting.

User Stories: Integration with Scheduling

• As a researcher, I want to request reactor time directly from my sample entry so that my experiment data is linked to the scheduled slot.

• As a researcher, I want the system to show me my approved time slots from the Scheduling System when I'm ready to irradiate.

• As a researcher, I want my experiment to automatically transition to "Scheduled" state when the Scheduling System confirms my slot.

Note: Full scheduling capabilities (viewing calendars, managing conflicts, facility displays) are handled by the [Scheduling System](scheduling-system-prd.md).

User Stories: Integration with Compliance

• As a researcher, I want the system to verify my experiment has valid ROC authorization before allowing irradiation.

• As a compliance officer, I want to query all experiments performed under a specific Authorized Experiment number.

• As an auditor, I want to see the complete chain of custody for any sample including all state transitions and who performed them.

Note: Full compliance tracking (ROC approvals, evidence packages, audit reports) is handled by the [Compliance Tracking System](compliance-tracking-prd.md).

Sample Metadata Schema

Based on Nick Luciano's initial list, refined with Khiloni's feedback:

Required Fields

Optional Fields

Facility Dropdown Values

From Khiloni's comprehensive list:

Ex-core:

• BP1 - Beam Port 1

• BP2 - Beam Port 2

• BP3 - Beam Port 3

• BP4 - Beam Port 4

• BP5 - Beam Port 5

In-core:

• TPNT - Thermal Pneumatic Facility

• EPNT - Epithermal Pneumatic Facility

• RSR - Rotary Specimen Rack

• CT - Central Thimble

• F3EL - Fast 3-Element Facility

• 3EL_Cd - Cd-lined 3-Element Facility

• 3EL_Pb - Pb-lined 3-Element Facility

Note: Khiloni advises: "you'll probably want someone on the reactor staff to look this over. They'll know better than me."

Workflow Stages

Based on Khiloni's description of typical workflow:

Stage Transitions

Integration Points

Calendar & Scheduling (Core Feature)

From Khiloni:

"The way we schedule reactor time right now is send a calendar request to NETL-Reactor with our name, desired power level, estimated irradiation time, facility, and any details that might be important to the staff."

"I don't think it actually matters to any of us experimenters what the schedule says – we typically write down what happens on the day of for our own purposes."

Design Decision: Calendar shows intent; Experiment Manager tracks what actually happened. Both are important. The system maintains:

• Scheduled Time — When the experiment was planned to occur

• Actual Time — When it actually occurred (may differ due to delays, reactor trips, etc.)

This enables analysis like: "How often do experiments run on schedule?" and "What's our average delay?"

Calendar Integration Options:

Conflict Detection:

• Warn if same facility requested at overlapping times

• Warn if total requested power exceeds license limit

• Suggest alternative times if conflicts exist

Reactor Time-Series

Automatically correlate sample irradiation windows with:

• Actual power levels during irradiation

• Control rod positions

• Temperature readings

This enables post-hoc analysis: "What were the actual reactor conditions during my irradiation?"

Operations Log

Cross-reference Ops Log entries with experiment IDs for complete audit trail.

UI Mockup Concepts

Sample Entry Form

Sample Status Dashboard

Schedule Views

Week View (Reactor Manager)

Pending Requests (3): Shah, K. (EPNT, Jan 27 10:00-12:00) | Chen, M. (CT, Jan 28 08:00-16:00) | Lee, J. (BP3, Jan 29 14:00-17:00)

Facility Entrance Display (Large Screen, Read-Only)

Reactor Status: Operating at 950 kW

Console View (Operator, Next 4 Hours)

MVP Scope (Phase 1)

In Scope

• Sample metadata entry with pre-populated dropdowns

• Basic status tracking (manual state transitions)

• Request scheduling — submit time requests, view pending/approved

• Schedule visualization — day/week/month views

• Facility entrance display — today's schedule on lobby screen

• Correlation with reactor time-series (read-only)

• Export to CSV/Excel for researchers' existing workflows

Phase 2

• External calendar sync (Google, Outlook, iCal)

• Recurring experiment scheduling

• Automated dose calculations (with model integration)

• AI-assisted sample entry (see Forward-Thinking Design)

Out of Scope (For Now)

• Spectrum analysis tools (use existing software)

• Web calculators for all detector types (too much scope; Khiloni's concern valid)

Data Freshness & Real-Time Architecture

Design Decision: Streaming-first architecture. Real-time is the default; batch for aggregations and fallback.

See ADR 007

Experiment Manager Latency Targets

UI Freshness Pattern

Live is the default. Warnings appear only when streaming is degraded:

Freshness Indicators:

• 🟢 Green (< 1 min): Live data

• 🟡 Yellow (1-15 min): Near-real-time

• 🟠 Orange (15 min - 1 hr): May be stale

• 🔴 Red (> 1 hr): Likely stale — manual refresh recommended

Streaming-Enabled User Stories (Phase 2+)

• As a researcher, I want to receive an in-app notification when my time request is approved, so I can immediately confirm my availability.

• As a facility manager, I want the entrance display to update in real-time when experiments start/complete, so staff always see accurate status.

• As a researcher, I want to see "Position now available" push notifications when a slot opens up, so I can quickly claim cancelled time.

• As an operator, I want to see live sample status on my console, so I know when researchers expect their samples without checking a separate system.

Forward-Thinking Design

The Problem with Backwards-Looking Requirements

Stakeholder feedback reflects current workflows constrained by current tools. Khiloni tracks experiments in spreadsheets because that's what's available. But if we only digitize existing workflows, we miss transformative opportunities.

Question we must ask: "If these capabilities existed today, what would users actually want?"

Minimizing Data Entry

Principle: Every field the user has to type is friction. Reduce friction through:

Overridable Assumptions

Every smart default should be easily overridden:

User can accept suggestion with one click, or ignore and keep their selection.

AI/LLM Integration (Phase 3+)

Vision: A small, nuclear-domain-tuned LLM integrated into Neutron OS that:

• Understands nuclear terminology — "Put my Au-foil in the rabbit" → recognizes "rabbit" = pneumatic transfer system

• Has facility context via RAG — Continuously updated with:

- This facility's SOPs and safety procedures

- Historical experiments at this facility

- ROC-authorized experiment types

- Current core configuration and flux maps

• Assists with entry — User types natural language, system extracts structured fields:

   ```    User: "I need to irradiate 0.1g of gold foil for NAA, 30 minutes            at 950 kW, probably next Tuesday"

   System extracts:    - Sample: gold foil    - Mass: 0.1g    - Irradiation time: 30 min    - Power: 950 kW    - Suggested date: Tue Jan 28    - Inferred facility: TPNT (NAA standard)    - Inferred purpose: Neutron Activation Analysis

   [Review & Submit] [Edit fields manually]    ```

• Answers questions — "What's the expected activity for this sample?" → LLM queries models, returns estimate

• Suggests safety considerations — "This sample mass + irradiation time will produce ~500 mrem/hr dose rate. Ensure hot cell is available."

Why a domain-specific LLM, not GPT-4?

• Can run on-premise (no sensitive data leaving facility)

• Faster response times (smaller model)

• Tuned for nuclear vocabulary and facility-specific jargon

• RAG keeps it current without retraining

Operational Requirements Integration

Experiment Manager operates within the broader Neutron OS operational framework. Critical operational requirements are defined at the system level rather than per-module to ensure consistency across all systems.

See also: Master Tech Spec § 9: Operational Requirements & Continuity

Relevant Operational Concerns

Key Integration Points:

• Facility configuration is centrally managed; Experiment Manager queries facility master data for dropdowns and workflows

• Testing procedures include running parallel experiments (hand-logged + electronic) with daily reconciliation

• Offline-first design ensures researchers can query experiment records and create new entries even during cloud outages

• Data retention is enforced at the data layer; Experiment Manager submits records to the backup/retention system

Multi-Facility Configurability

Design Principle: Core system is reactor-agnostic. Facility-specific aspects are configuration.

Example: Another TRIGA Facility

If INL's NRAD adopted Neutron OS:

• Facility dropdowns: Different (their pneumatic system has different name)

• License limit: Different (different power rating)

• Approval workflow: Different (different organizational structure)

• Core tracking logic: Same (sample lifecycle is universal)

Example: Non-TRIGA Research Reactor

MIT Reactor or university pool-type reactor:

• Facility types: Mostly similar (beam ports, in-core positions)

• Sample tracking: Same

• Scheduling: Same

• Regulatory requirements: Similar (all under NRC)

Open Questions

• Spectrum file storage: Where should raw spectrum files be stored? Local filesystem? Object storage?

• Access control: Should all researchers see all samples, or only their own?

• Historical data migration: Is there value in digitizing past experiment records from binders?

• Detector integration: Khiloni mentions multiple detector types—should we integrate with detector software or keep that separate?

• LLM hosting: On-premise GPU server? Edge device? Cloud with data anonymization?

• RAG update frequency: How often should the knowledge base refresh? Real-time vs. nightly?

Success Metrics

Sample Tracking

Scheduling

AI/Smart Features (Phase 2+)

Appendix: Full Workflow Example (from Khiloni)

"1. Create an operations request
a. Run models (usually analytical or SCALE) to estimate the sample activities – go for conservative estimates...
b. Convert activities to dose rates – the reactor staff don't usually care about activity, they want to know how much beta and gamma dose they will receive...
c. If you already have an operations request (noted with a 4-digit number), then you can reference that in your calendar request.

2. Create a calendar request – include name, power level, facility, 4-digit ops request, sample, irradiation time. The staff will review and approve.

3. On irradiation day – the staff will insert the appropriate facilities as needed... experimenters will note down anything significant... They also record the dose of the sample when it is finished being irradiated using a yellow frisker.

4. After irradiation, samples are pulled – when they are pulled depends on how hot they are and when they need to be analyzed/sent off.

5. Analysis is heavily experimenter dependent... once you are ready to count your sample you will set it up on a detector and count it. You will do the respective energy and efficiency calibrations for your detectors as well.

6. Analysis is done in a variety of ways – whatever software you prefer for reading spectra.

7. Disposal is done at the behest of the staff – usually when storage locations get too full."

Document Status: Ready for technical review and implementation planning