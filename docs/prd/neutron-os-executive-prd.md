Table of Contents

Neutron OS — Executive Product Requirements

Nuclear Energy Unified Technology for Research, Operations & Networks

What is Neutron OS?

Neutron OS is a modular digital platform for nuclear facilities that unifies data management, operations tracking, experiment scheduling, and analytics into a single system. It replaces fragmented workflows (paper logs, spreadsheets, phone calls, email calendars) with integrated digital tools.

Who is it for?

Product Modules

Neutron OS is modular. Facilities enable only what they need.

Core Infrastructure

Application Modules

Future Modules

This swimlane diagram shows how different users interact with Neutron OS throughout a typical week:

Module Architecture

Module Status Legend

Key Value Propositions

For Operations Staff

For Researchers

For Facility Management

Key Design Decisions

Neutron OS architecture embodies several foundational decisions documented in our :Architecture Decision Records

Streaming-First Philosophy

Designed for commercial reactor scale from day one.

As nuclear commercialization accelerates, fleet operators will manage dozens of units generating petabytes of telemetry. Streaming-first architecture enables:

• Fleet-wide anomaly detection — correlate signals across multiple units in real-time

• Instant operating limit propagation — safety parameter changes flow immediately to all systems

• Coordinated load-following — respond to grid demands across a fleet, not just one unit

• Graceful scaling — same architecture handles one research reactor or fifty commercial units

With streaming-first:

• 🟢 Live is the default — users assume data is current

• ⚠️ Stale warnings only appear when streaming is degraded

• Batch processing handles historical aggregations and disaster recovery

Deployment Architecture

Phased Rollout

Data Flow & Integration

⚠️ Diagram rendering failed

Compliance & Safety Framework

Success Metrics (Platform-Wide)

Constituent PRDs

Each module has a detailed PRD with user stories, schemas, and mockups:

Core Infrastructure

• [Data Platform PRD](data-platform-prd.md)

- Lakehouse architecture (Bronze/Silver/Gold)

- Time-series ingestion

- Query layer (DuckDB, Superset)

- Streaming and batch processing

• [Scheduling System PRD](scheduling-system-prd.md) (Cross-Cutting)

- Unified time slot management

- Resource allocation and conflicts

- Multi-module integration

- Calendar synchronization

• [Compliance Tracking PRD](compliance-tracking-prd.md) (Cross-Cutting)

- Regulatory monitoring (NRC, DOE)

- 30-minute check enforcement

- Evidence package generation

- Real-time compliance dashboards

• [Media Library PRD](media-library-prd.md) (Cross-Cutting)

- Recordings, photos, documents, and binary artifacts

- Metadata tagging and semantic search

- Entity linking (experiments, ops log entries, compliance evidence)

- Offline-first with optional S3/MinIO backend

Application Modules

• [Reactor Ops Log PRD](file:///Users/ben/Projects/UT_Computational_NE/Neutron_OS/docs/_tools/generated/reactor-ops-log-prd.docx)

- Console check logging

- Shift handoffs and summaries

- Maintenance tracking

- Tamper-proof audit trail

• [Experiment Manager PRD](file:///Users/ben/Projects/UT_Computational_NE/Neutron_OS/docs/_tools/generated/experiment-manager-prd.docx)

- Sample lifecycle tracking

- Metadata and chain of custody

- Results correlation

- ROC authorization tracking

• [Analytics Dashboards PRD](analytics-dashboards-prd.md)

- Reactor Operations dashboard

- Utilization metrics

- Fuel burnup visualization

- Data quality monitoring

Optional Modules

• [Medical Isotope Production PRD](medical-isotope-prd.md)

- Customer order portal

- Production batching

- QA/QC workflow

- Shipping and delivery tracking

Module Feature Comparison

Module Interdependencies

Technical Foundation

For technical architecture, schemas, and implementation details, see:

• [Neutron OS Master Tech Spec](../specs/neutron-os-master-tech-spec.md) — Full technical specification

• [Executive Technical Summary](../specs/neutron-os-executive-summary.md) — 2-page technical overview

Feedback & Stakeholder Input

This PRD incorporates feedback from:

NEUP Research Addendum

This section maps NEUP 2026 proposals to Neutron OS modules and identifies platform enhancements driven by research needs.

Research-Platform Alignment Matrix

NEUP Proposal: Operator LLM Safety

Proposal: Establishing safety guardrails for LLM use in nuclear operations.

Gap Addressed: Future "Search/AI" module lacks safety specifications for operational contexts.

LLM Safety Framework

New Requirements for Search/AI Module

NEUP Proposal: Cyber-Nuclear Security (Topic 11)

Proposal: Cybersecurity frameworks specifically for nuclear digital twins.

Gap Addressed: Security architecture focuses on auth/authz; lacks cyber-physical threat modeling.

Cyber-Physical Security Layer

NEUP Proposal: Digital Twin Framework IRP

Proposal: Industry-wide standards for nuclear digital twin architectures.

Supporting PRD Element: Modular architecture already uses factory/provider pattern enabling multi-facility deployment.

Recommended Enhancement: Publish ReactorProvider interface as open standard for industry adoption.

Research Collaboration Priorities

Additional NEUP POCs for Related Proposals:

• KANs Reactor Modeling: PI Majdi Radaideh (U Michigan); Collab: Jeongwon Seo (UT), Cole Gentry (UT)

• PINNs Self-Shielding: PI Cole Gentry (UT); Collab: Nicholas Luciano (UT), Yaqi Wang (INL)

• AI XS Library Tuning: PI Cole Gentry (UT); Collab: Yaqi Wang (INL), Jesse Brown (ORNL)

• ML Neutronics Acceleration: PI Cole Gentry (UT); Collab: Cody Permann (INL)

• Nuclear LLM Bench: PI Kevin Clarno (UT); Collab: Derek Booth (UT), Ondrej Chvala (UT)

• Virtual Systems Engineer: PI TBD; Collab: Ron Boring (INL)

• Cherenkov Power Monitoring: PI W. Charlton (UT); Collab: J. Seo (UT), R. Steward (INL)

This addendum establishes the research integration framework for Neutron OS evolution.

Potential Future Partners

Document Status: Active — Updated with stakeholder feedback January 2026