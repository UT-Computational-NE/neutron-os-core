Table of Contents

Product Requirements Document: Reactor Ops Log

Module: Reactor Ops Log   Status: Draft   Last Updated: January 22, 2026   Stakeholder Input: Jim (TJ), Nick Luciano (Jan 2026)   Parent:    Historical Reference: Previously referred to as "elog" in some contextsExecutive PRD

Executive Summary

The Reactor Ops Log captures reactor operations events, mandatory safety checks, and operational notes in a tamper-evident format that satisfies NRC regulatory requirements. It replaces the current paper-based console logbook with a digital system that maintains 10 CFR 50.9 compliance while enabling searchability, correlation with time-series data, and export for inspection.

Ops Log vs. Experiment Log: A Unified System

Background

Historically at NETL, Jim maintains two separate physical logbooks:

• Reactor Ops Log — Console operations, 30-minute checks, startups/shutdowns, anomalies

• Reactor Experiment Log — Experiment activities, sample insertions/removals, research notes

This separation exists due to physical logistics (different binders at different locations), not regulatory mandate. NRC cares about completeness and tamper-evidence, not which binder an entry lives in.

Our Approach: Unified System, Separate Views

Neutron OS combines both logs into a single system with:

• Entry type classification: Each entry is tagged as OPS or EXPERIMENT (or both)

• Filtered views: Users can view Ops-only, Experiment-only, or combined chronological

• Seamless navigation: One-click toggle between views; cross-references visible in both

• Single search: Find any entry regardless of type

• Unified audit trail: All entries share the same tamper-evident infrastructure

Why Combine?

User Stories (Unified System)

• As a reactor operator, I want to quickly toggle between Ops view and All Entries view so I can focus on console operations but still see experiment context when needed.

• As a researcher, I want to filter to Experiment entries for my samples while still seeing relevant Ops entries (startups, power changes) that affected my irradiation.

• As an NRC inspector, I want to export all entries for a date range and filter by type as needed during review.

Entry Type Examples

User Journey Map

Reactor Operator: Daily Shift

Entry Lifecycle

Compliance Flow

Stakeholder Insights

Current State and Challenges (from Jim)

"We have attempted to use the elog software as a training exercise to familiarize ourselves with digital/electronic elog software. We found that it is a steep learning curve for the 'older' ops staff. I believe it would be useful to have a modeler/designer come to the NETL and investigate and review our current system. Perhaps we could have a designer come to the NETL while operating and then design/massage the elog software according to our users' needs."

Note: "elog" here refers to third-party electronic logbook software Jim evaluated, not Neutron OS.

Mandatory Checks Gap

"A gap would mean that the :30 minute check was not performed when operating. When operating at the NETL, we are required to perform a console 'walkdown' every 30 minutes. During this check, we take readings from various instruments and log them in the elog."

Note: "elog" here refers to the reactor operations logbook, now the Reactor Ops Log in Neutron OS.

Regulatory Context

"NRC inspects documents yearly... they normally only look at half of the records, and we don't have to go back past the 2 years of operation in many cases. They prefer electronic documents."

Key Compliance Numbers (from Jim):

• Inspection periodicity: NRC inspects half of records each year (effectively 2-year coverage)

• Evidence package scope: 2 years of operational records

• Preferred format: Electronic (PDF + plain text archive)

• Operator requalification: 4 hours/quarter minimum console time required

Tamper-Proof Requirements

"Supplemental comments. The only way to 'edit' an entry should be a supplement. No deleting an entry—you should simply be able to add a supplement which identifies and corrects the mistake."

Experiment Categories

"We have a schedule of Authorized Experiments. These experiments are authorized by the ROC (Reactor Oversight Committee) after review through NETL Staff (Reactor Manager/HP/Director - Then ROC chair). Routine Experiments are performed as they are covered under an Authorized Experiment."

User Stories

Primary Users

User Stories

• As a reactor operator, I want to log the 30-minute console check with minimal clicks so that I can return attention to the console quickly.

• As a reactor operator, I want a timer/reminder for mandatory checks so that I don't miss the 30-minute window.

• As a SRO, I want to see all entries from my shift in chronological order so that I can review before sign-off.

• As a RM, I want to be alerted if mandatory checks are missed so that I can follow up.

• As an NRC inspector, I want to search entries by date range, category, and operator so that I can efficiently review records.

• As any user, I want to add supplemental comments to correct errors without modifying the original entry so that the audit trail is preserved.

• As a reactor manager, I want to track each operator's console hours per quarter so that I can ensure they meet the 4-hour/quarter minimum for requalification.

• As a reactor manager, I want to generate NRC evidence packages covering the most recent 2 years of records so that I can efficiently prepare for inspections.

Entry Types and Categories

Based on stakeholder feedback:

Mandatory Entry Types

Optional Entry Types

Experiment Authorization Categories

From Jim:

Entry Tags (User-Assignable)

From Jim: Categories help with searchability and NRC inspection preparation.

Data Schema

Entry Schema

entry:
  id: uuid (system-generated)
  entry_number: integer (sequential within year, e.g., 2026-001)
  timestamp: datetime (system clock, immutable)
  entry_type: enum (see types above)
  author_id: uuid (logged-in operator)
  author_name: string (display name)
  co_signer_id: uuid (optional, for dual-sign entries)
  
  # Content
  title: string (brief summary)
  body: text (detailed entry)
  
  # Structured data (type-dependent)
  instrument_readings: json (for CONSOLE_CHECK)
  checklist_items: json (for STARTUP/SHUTDOWN)
  
  # Metadata
  reactor_mode: enum (shutdown, startup, steady-state, power-change)
  reactor_power_kw: decimal (auto-populated from time-series)
  
  # Supplements
  supplements: array of supplement objects
  
  # Audit
  created_at: datetime
  ip_address: string (for audit trail)
  signature_hash: string (cryptographic verification)

Supplement Schema

supplement:
  id: uuid
  parent_entry_id: uuid
  timestamp: datetime
  author_id: uuid
  author_name: string
  reason: enum (correction, clarification, addition)
  body: text
  signature_hash: string

Tamper-Evidence Implementation

Per Jim's requirement ("No deleting an entry—you should simply be able to add a supplement"):

Design Principles

• Append-only storage: Entries are INSERT-only. No UPDATE or DELETE operations on entry content.

• Cryptographic signatures: Each entry is hashed with the previous entry's hash (blockchain-style chain), making retroactive modification detectable.

• Supplements for corrections: Any modification is captured as a linked supplement with its own timestamp and author.

• Audit log: All access (read/write) is logged with user ID, timestamp, and IP address.

Example: Correcting an Error

Mandatory Check Timer

Requirements

• Visual countdown timer showing time until next mandatory check

• Audible alert at 25 minutes (5-minute warning) and 30 minutes (deadline)

• Entry form pre-populated when timer triggers

• Dashboard indicator showing "missed checks" count per shift

Gap Detection

From Jim: "A gap would mean that the :30 minute check was not performed when operating."

Detection logic:

Dashboard alert:

Export Requirements

From Jim: "Export to PDF would work, but a simple text file for archive and future proof would also work."

Export Formats

Archive Integrity (from Jim):

"Concerned about software failure/migration. Text archives could be modified."

Design Response:

• PDF exports include cryptographic signatures (verifiable)

• Plain text archives include SHA-256 checksums

• Both formats exported together for redundancy

• Checksums stored in tamper-evident audit trail (Hyperledger)

• Regular automated export to long-term storage (prevents software dependency)

Export Filters

• Date range

• Entry type(s)

• Author(s)

• Keyword search

• Include/exclude supplements

UI Mockup Concepts

Console View (Primary Interface During Operations)

┌─────────────────────────────────────────────────────────────────────┐
│  NETL OPERATIONS LOG                    [2026-01-21]  [Shift: Day] │
│  Operator: J. Smith (RO)        ┌────────────────────────────────┐ │
│  Power: 950 kW                  │  NEXT CHECK IN: 12:45          │ │
│  Status: OPERATING              │  ████████████░░░░░░░░░  [Log]  │ │
│                                 └────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [+ New Entry ▼]  [Console Check]  [Experiment]  [General Note]    │
│                                                                     │
│  ═══════════════════════════════════════════════════════════════   │
│  RECENT ENTRIES                                                     │
│  ═══════════════════════════════════════════════════════════════   │
│                                                                     │
│  14:30 │ CONSOLE_CHECK │ 30-min check. All readings nominal.       │
│        │ J. Smith      │                                  [Detail] │
│  ─────────────────────────────────────────────────────────────────  │
│  14:15 │ EXPERIMENT    │ Sample Au-foil-042 inserted in TPNT.      │
│        │ J. Smith      │ Ops Request 4521.               [Detail] │
│  ─────────────────────────────────────────────────────────────────  │
│  14:00 │ CONSOLE_CHECK │ 30-min check. Power raised to 950 kW.     │
│        │ J. Smith      │                                  [Detail] │
│  ─────────────────────────────────────────────────────────────────  │
│  13:30 │ STARTUP       │ Startup complete. Reaching 500 kW.        │
│        │ J. Smith      │ Co-signed: M. Jones (SRO)        [Detail] │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

Quick Console Check Entry

┌─────────────────────────────────────────────────────────────────────┐
│  30-MINUTE CONSOLE CHECK                               [Cancel] [X]│
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Time: 15:00:00 (auto)          Power: 950 kW (auto from DCS)      │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ INSTRUMENT READINGS (auto-populated where available)        │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ Channel A: [___] %    Channel B: [___] %                    │   │
│  │ Pool Temp: [___] °F   Coolant Temp: [___] °F               │   │
│  │ Rod A: [___] %        Rod B: [___] %                        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Notes: [All readings nominal____________________________]          │
│                                                                     │
│  ☑ I have performed a physical console walkdown                    │
│                                                                     │
│                                                       [Submit]      │
└─────────────────────────────────────────────────────────────────────┘

Entry Detail View (with Supplement)

┌─────────────────────────────────────────────────────────────────────┐
│  ENTRY 2026-042                                        [Back] [PDF]│
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Type: CONSOLE_CHECK                                                │
│  Timestamp: 2026-01-21 14:30:00                                     │
│  Author: J. Smith (RO)                                              │
│  Reactor Power: 950 kW                                              │
│                                                                     │
│  ───────────────────────────────────────────────────────────────    │
│  CONTENT                                                            │
│  ───────────────────────────────────────────────────────────────    │
│  30-minute console check. Power 950 kW. All readings nominal.       │
│  Channel A: 48%, Channel B: 47%                                     │
│                                                                     │
│  ───────────────────────────────────────────────────────────────    │
│  ⚠️ SUPPLEMENT (2026-01-21 14:35:12)                                │
│  ───────────────────────────────────────────────────────────────    │
│  Author: J. Smith (RO)                                              │
│  Reason: Correction                                                 │
│                                                                     │
│  Correction: Power was 850 kW, not 950 kW. Misread instrument.     │
│                                                                     │
│  ───────────────────────────────────────────────────────────────    │
│                                              [Add Supplement]       │
│                                                                     │
│  Signature Hash: a3f8c2...d91e (verified ✓)                        │
└─────────────────────────────────────────────────────────────────────┘

Technical Requirements

Data Freshness & Real-Time Architecture

Design Decision: Streaming-first architecture. Real-time is the default; batch for aggregations and fallback.

See ADR 007

Reactor Ops Log Latency Targets:

UI Pattern: Live is the default. Warnings appear only when streaming is degraded:

Performance

• Entry submission < 1 second (operators cannot wait during operations)

• Search results < 3 seconds for 2-year date range

• Export PDF < 10 seconds for 1-month range

Reliability

• Offline-capable: Must function if network is temporarily unavailable

• Local cache syncs when connectivity restored

• No data loss scenario acceptable

Security

• Authentication required (linked to facility badge/credentials)

• Role-based access: RO can create entries; RM can view all and generate reports

• All access logged for audit

Operational Procedures and Continuity

All operational requirements are defined system-wide in the master technical specification. This section provides Ops Log-specific clarifications and applies those cross-cutting requirements to reactor operations logging.

See: Master Tech Spec § 9: Operational Requirements & Continuity

This includes:

• Day-End Close-Out (§9.1): Entry immutability, supplement allowance, shift boundaries

• Backup & Archive (§9.2): Cloud, local drive, printed archives, retention policy

• Multi-Facility Configuration (§9.3): Customizable forms, facility-specific dropdowns

• Deployment Topology (§9.4): Phased control room deployment, network architecture

• Testing Phase & Operator Confidence (§9.5): Dual-logging procedures, transition plan

• System Resilience & Downtime (§9.6): Offline-first, local cache, hand-log fallbacks

Day-End Close-Out (Ops Log Clarifications)

Requirement: Operators want the log to be "closed out" at the end of the day.

Clarification Needed: Define "closed out" and its implications:

Design Options:

• Automatic Close (Recommended): Log entries automatically become read-only at end-of-shift timestamp (e.g., 16:00 for day shift). Supplements still allowed.

• Manual Close: SRO/Shift Manager explicitly clicks "Close Shift" button; log becomes read-only.

• Time-Locked Close: Entries older than 24 hours become read-only; recent entries remain editable.

Implementation Consideration: Supplement-only model (no deletes, no edits) already enforces immutability if we lock the entry itself post-close.

Backup and Archive Requirements

Requirement: Operators want one or more hard and soft backups for the elog. Initially, this could be printing out hard copies (weekly, monthly) or a hard-drive backup.

Backup Strategy:

Operator Interaction:

• Weekly manual export to PDF + plain text for facility records (operators print/file)

• System automatically syncs to encrypted local drive

• Cloud backup is transparent (automatic daily)

• Operators can request on-demand export anytime

Retention Policy (to be finalized):

• Live system: 2 years (NRC inspection window)

• Offline archive: 7+ years (regulatory requirement, facility-specific)

Data Entry Forms and Customization

Requirement: Operators want to enter data in the format they are accustomed to. They need specific data forms.

Current Facility-Specific Forms:

Design Approach:

• Core console check form is standardized (meets NRC requirements)

• Other entry types allow facility-specific fields via configuration

• Dropdown menus for common values (experiment types, shutdown reasons)

• Pre-fill templates for routine entries

• Ability to save custom templates for "standard NAA irradiation," "standard INAA," etc.

Server Location (Control Room Deployment)

Requirement: Operators need the elog server to be (eventually) located in the control room.

Phased Deployment:

Control Room Deployment Considerations:

• Environment: Control room has strict physical security, temperature control, limited physical space

• Network: Must tie into facility network without compromising reactor control systems

• Redundancy: Dual network paths (primary + backup) to prevent single-point-of-failure

• UPS/Power: Must survive facility power loss for ≥15 minutes (allow graceful shutdown or hand-off to backup system)

• Operator Interface: Console-accessible display (monitor arm, touchscreen, or hardened tablet)

Interim Solution (Phase 1): Cloud-based system with local fiber connection to control room. Operators access via facility workstation in control room annex (5 feet from console).

Testing Phase Procedures

Requirement: Operators need to define their procedures for logging while the elog is in testing phase. Initially, they will likely perform double duty during testing, recording both a hand-log and an electronic log. Once they gain confidence in the elog, they will rely on the elog exclusively.

Testing Phase Plan:

Dual-Logging Workflow (Phase 1):

• Operators make entry in hand-log (as usual)

• Same operators (or cross-shift buddy) enter data into electronic log within 1 hour

• Daily reconciliation: Compare hand-log and electronic log entries for gaps/discrepancies

• Facility manager reviews reconciliation report

• Any discrepancies resolved before shift closes

Confidence Checkpoints:

• Week 2: No missed entries between logs

• Week 4: Operators comfortable with system (no support needed)

• Week 8: Formal sign-off by facility manager and ops staff to proceed with Phase 3

Training Requirements:

• System orientation (1 hour on-shift)

• Hands-on practice (1 shift of parallel logging with support staff present)

• Q&A session post-training

• Written acknowledgment that operator understands system

System Unavailability / Downtime Procedures

Requirement: Operators need to define their procedure for what to do when the elog is inaccessible (revert to hand logs? Send a time-stamped email to somewhere? Have a local elog instance capture the data?).

Availability Tiers and Fallback:

Detailed Fallback Procedures:

• Latency/Brief Outage (Local Cache Mode)

- System detects network issue

- Operator receives on-screen notification: "Network latency detected. Entries are queuing locally and will sync when connection restored."

- Operators continue logging normally (UI is responsive, data is cached)

- No action required; automatic sync happens

• Extended Outage (Hand-Log Fallback)

- System unavailable for >1 hour

- Operator reverts to printed hand-log form (stored at console)

- Each entry includes: Time, operator initials, entry type, content

- At end of shift, operator takes photos/scans of hand-log pages

- Email scans to: elog-backup@facility.edu with subject: "Backup Entries [Shift Date]"

- Include filename: elog-backup-2026-01-21-dayshift.pdf

• Data Recovery Post-Outage

- Facility IT restores system from backup

- Facility manager (or designee) manually re-enters hand-log entries into system

- Timestamp used: Original entry time (from hand-log)

- Note added to each entry: "Re-entered from hand-log backup due to [outage date/reason]"

- Appendix added to shift summary: "XXX entries re-entered from backup on [date]"

Local elog Instance (Future Option)

"Have a local elog instance capture the data?"

Design consideration for Phase 2:

• Ruggedized local server in facility server room (redundant to cloud)

• Runs on facility network only; syncs to cloud when connectivity restored

• Adds complexity and cost; defer to Phase 2 if needed

Preferred: Hybrid Approach (Recommended)

• Hand-log forms + email capture (low cost, reliable, operator-familiar)

• Local network backup drive for sync (added security; no cloud dependency during outage)

• Invest in local elog server only if hand-log procedure proves insufficient

Hand-Log Form Design

Goal: Design a printed form that operators fill during outages, then rapidly OCR + import back into the system post-recovery.

Design Principles for OCR Readiness:

• High contrast: Black text/checkboxes on white background; avoid grays or light colors

• Structured layout: Fixed field positions (same location on every form for machine recognition)

• Clear boundaries: Visible boxes/lines defining each field

• Block letter encouragement: Printed text is more OCR-friendly than cursive

• Avoid free-form: Use dropdowns, checkboxes, and fill-in-blanks instead of open narrative where possible

• Sequential numbering: Entry number printed for tracking and verification

• Barcode/QR: Optional metadata (date, shift, page number) for fast sorting post-scan

Hand-Log Form Layout:

┌──────────────────────────────────────────────────────────────────────┐
│                     NETL REACTOR OPS LOG                             │
│                   EMERGENCY BACKUP ENTRY FORM                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ENTRY #: __________    DATE: __/__/____  SHIFT: □ Day □ Night     │
│                                                 □ Owl                │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ TIME:  __:__ AM/PM   OPERATOR NAME: _____________________    │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ ENTRY TYPE (CHECK ONE):                                      │   │
│  │ □ Console Check     □ Startup      □ Shutdown              │   │
│  │ □ Experiment Log    □ Scram        □ General Note           │   │
│  │ □ Maintenance       □ Radiation Survey    □ Other: ____    │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ REACTOR STATUS:                                              │   │
│  │ Power: __________ kW    Mode: □ Shutdown  □ Operating      │   │
│  │ Pool Temp: __________ °F    Coolant Temp: __________ °F   │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ ENTRY DETAILS:                                               │   │
│  │ ________________________________________________________________ │   │
│  │ ________________________________________________________________ │   │
│  │ ________________________________________________________________ │   │
│  │ ________________________________________________________________ │   │
│  │ ________________________________________________________________ │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ TAGS (IF APPLICABLE):                                        │   │
│  │ □ pnt-sample    □ dose-rate     □ excess-reactivity        │   │
│  │ □ maintenance   □ startup       □ shutdown                  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ SIGNATURE SECTION:                                           │   │
│  │ Co-Signature Required? □ Yes  □ No                          │   │
│  │ Operator Initials: ___   Signature: __________________      │   │
│  │ SRO Name (if req'd): _________________ Signature: _______  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

Form Specifications for OCR:

OCR Workflow (Post-Outage Recovery):

1. SCAN
   └─ Operator scans hand-log pages at end of shift
      (High-res B&W scan, 300 dpi minimum)

2. OCR CONVERSION
   └─ Batch process forms through OCR engine (e.g., Tesseract, AWS Textract)
      Result: Structured data (JSON/CSV)

3. VALIDATION
   └─ Facility manager (or operator) reviews OCR output
      Checks:
      - Handwritten fields flagged for manual correction
      - Numeric fields verified (power, temperature)
      - Checkboxes correctly interpreted
      - Operator names matched to facility directory

4. IMPORT
   └─ Validated data → System import script
      Generates entries with:
      - timestamp = original entry time from hand-log
      - source = "hand-log-backup (outage 2026-01-21)"
      - status = "verified" or "requires_review"

5. AUDIT
   └─ Facility manager spot-checks 10% of imported entries
      Compares hand-log original vs. system entry
      Flags any discrepancies for manual correction

Quality Assurance for OCR:

Estimated Re-Entry Time (with OCR):

Recommended Approach: Use OCR for high-volume catch-up (100+ entries) with sampled manual validation. Operators can review OCR results while facility manager imports validated batches.

MVP Scope (Phase 1)

In Scope

• Basic entry creation (CONSOLE_CHECK, STARTUP, SHUTDOWN, GENERAL_NOTE)

• Supplement addition (no edit/delete of originals)

• 30-minute timer with alerts

• Export to PDF and plain text

• Search by date, type, author

Out of Scope (Future)

• Auto-population from DCS instruments

• Offline mode with sync

• Digital signature (cryptographic)

• Integration with experiment manager

• Mobile interface

Implementation Recommendation

From Jim:

"Perhaps we could have a designer come to the NETL while operating and then design/massage the elog software according to our users' needs."

Proposed approach:

• Deploy minimal prototype (console check only)

• Designer/developer spends 2-3 operating days at NETL console

• Iterate based on real-world usage

• Expand to other entry types after validation

Open Questions

• Instrument readings: Which specific instruments are read during console checks? Can any be auto-populated from DCS?

• Dual signatures: Which entry types require SRO co-signature?

• Existing records: Should historical paper logs be digitized, or start fresh?

• Badge integration: Can we authenticate via existing facility badge system?

• Offline behavior: How long can the console be offline before operations must pause?

• Automatic console check sensing (TBD - Design exploration needed):

- The legacy 1990s console view in the operations room is driven by data we can access

- Question: Can we automatically sense when console checks occur (via data tap) and auto-populate the Ops Log instead of requiring manual entry?

- Rationale: Eliminates dual-entry requirement (console data + ops log entry)

- Scope: Determine feasibility with console software status, data interface availability, and validation requirements

- Next step: Explore UI/UX workflows for auto-sensed vs. manual vs. hybrid entry modes

- Design Document: See  for 4 proposed workflow alternatives and recommendationsConsole Check UI/UX Mockups

Success Metrics

Appendix: 10 CFR 50.9 Compliance Notes

The Operations Log must satisfy NRC requirements for:

• Completeness: All required operating data recorded

• Accuracy: Information is correct; corrections are traceable

• Availability: Records accessible for inspection (2+ year retention)

• Authenticity: Can verify entries were made by authorized personnel at stated times

The supplement-based correction model and cryptographic chaining specifically address the "no modification without trace" requirement.

NEUP Research Addendum

NEUP Proposal: Semi-Autonomous Controls

Proposal: Developing semi-autonomous reactor control systems with human oversight.

Supporting PRD Sections:

• Entry type schema (extensible to new event types)

• Audit trail infrastructure

• SRO signature requirements

Gap Addressed: Current PRD assumes fully manual operations; no specification for autonomy modes or automated actions.

Autonomy Level Specification

New Entry Types for Autonomy

NEUP Proposal: Operator LLM Safety

Proposal: Safety constraints for LLM interactions with reactor operators.

Supporting PRD Sections:

• Audit trail (captures all system interactions)

• User role distinctions (SRO vs Operator permissions)

Gap Addressed: Future AI integration needs ops log entries for LLM interactions.

New Entry Types for LLM Interactions

These entry types enable audit trail for AI-assisted operations while maintaining regulatory compliance.

Document Status: Ready for on-site validation and technical review