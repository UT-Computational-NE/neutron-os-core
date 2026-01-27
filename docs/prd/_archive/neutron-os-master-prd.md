# Neutron OS Product Requirements Document

**Nuclear Energy Unified Technology for Research, Operations & Networks**

---

> ⚠️ **DRAFT - FOR INTERNAL REVIEW ONLY** ⚠️
>
> Version 0.1 | Generated: January 15, 2026 | Status: Draft for Colleague Review

---

| Property | Value |
|----------|-------|
| Document Type | Product Requirements Document (PRD) |
| Version | 0.1 DRAFT |
| Last Updated | 2026-01-15 |
| Status | Draft - Pending Review |
| Product Owner | [TBD] |
| Stakeholders | UT Computational NE Team, Nick Luciano, [Others TBD] |

---

## Table of Contents

1. [Vision & Goals](#1-vision--goals)
2. [User Personas](#2-user-personas)
3. [Problem Statement](#3-problem-statement)
4. [Solution Overview](#4-solution-overview)
5. [Feature Requirements](#5-feature-requirements)
6. [User Journeys](#6-user-journeys)
7. [Success Metrics](#7-success-metrics)
8. [Roadmap](#8-roadmap)
9. [Dependencies & Risks](#9-dependencies--risks)
10. [Appendices](#10-appendices)

---

## 1. Vision & Goals

### 1.1 Vision Statement

Neutron OS is a **digital twin data platform** that provides the infrastructure for nuclear reactor digital twins across multiple use cases—from real-time state estimation to fuel management to experiment planning.

> **Key Insight:** Digital twins serve multiple critical purposes in reactor operations. While real-time state estimation (predict faster than sensors) is technically demanding, the broader value spans fuel optimization, predictive maintenance, safety analysis, and research validation.

### 1.2 Digital Twin Use Cases

Digital twins powered by Neutron OS serve five primary categories:

| Use Case | Description | Key Capabilities |
|----------|-------------|------------------|
| **Real-Time State Estimation** | Predict reactor state faster than sensors (~10ms vs ~100ms) | Continuous state visibility, fill gaps between readings, estimate unmeasurable quantities |
| **Fuel Management** | Optimize fuel utilization and identify issues | Burnup tracking, hot spot identification, anomalous rod detection, reload optimization |
| **Predictive Maintenance** | Anticipate component degradation | Thermal cycling stress, control rod wear, scheduled maintenance windows |
| **Experiment Planning** | Simulate before execution | Irradiation planning, activation prediction, safety margin analysis |
| **Research & Validation** | Compare models to reality | Physics code validation, ML training data, academic publications |

### 1.3 Strategic Goals

- **🎯 Multi-Purpose Digital Twins:** Enable digital twin simulations across all five use case categories, with data infrastructure that supports both real-time and analytical workloads.

- **Unified Data Foundation:** Consolidate reactor operational data, simulation outputs, and research data into a single, queryable lakehouse with time-travel capabilities—serving as the training data and validation source for digital twin models.

- **ML Model Training Pipeline:** Provide the data infrastructure for training physics-informed machine learning models that power digital twin predictions across all use cases.

- **Fuel Management Intelligence:** Track burnup distribution, identify hot spots, detect anomalous fuel rod behavior, and optimize core reload patterns.

- **Prediction Validation Loop:** Compare digital twin predictions against actual sensor readings to continuously validate and improve model accuracy.

- **Regulatory Compliance:** Provide immutable audit trails via blockchain technology, enabling facilities to demonstrate data integrity to regulators with cryptographic proof.

- **Intelligent Operations:** Automate routine tasks like meeting documentation, requirements tracking, and report generation using AI/LLM capabilities.

- **Cross-Facility Collaboration:** Enable multiple nuclear facilities to share data and insights while maintaining security and audit separation.

- **Commercialization Pathway:** Build a platform that can be licensed to other reactors and nuclear facilities.

### 1.4 Strategic Partnerships & Integration Opportunities

#### Multi-Organization Design

Neutron OS is architected to support **multi-tenant deployments**, enabling multiple organizations to share infrastructure while maintaining strict data isolation. This design choice opens future collaboration opportunities, though our current focus is UT Austin's NETL facility.

**Design Principles:**
- Row-level security (RLS) enables tenant isolation
- Common schemas allow cross-facility benchmarking (with explicit consent)
- Federated deployment options support air-gapped or hybrid scenarios

#### Potential Future Partners

| Partner | Opportunity | Status |
|---------|-------------|--------|
| MIT NRL | MITR digital twin, Irradiation Loop DT tools | Active collaboration |
| Penn State RSEC | Breazeale TRIGA, NRC inspection innovation | Potential |
| UT Austin NETL | Primary implementation site | Current |
| Texas A&M NSC | AGN-201 digital twin | Potential |

---

## 2. User Personas

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              USER PERSONA MAP                                            │
│                              [DRAFT v0.1]                                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│   PRIMARY USERS                                                                          │
│   ─────────────                                                                          │
│                                                                                          │
│   ┌─────────────────────────────┐    ┌─────────────────────────────┐                    │
│   │        OPERATOR             │    │       RESEARCHER            │                    │
│   │        "Alex"               │    │        "Dana"               │                    │
│   │                             │    │                             │                    │
│   │ Role: Reactor Operator      │    │ Role: Graduate Researcher   │                    │
│   │                             │    │                             │                    │
│   │ Goals:                      │    │ Goals:                      │                    │
│   │ • Monitor reactor status    │    │ • Analyze experimental      │                    │
│   │ • Log operations accurately │    │   results                   │                    │
│   │ • Respond to anomalies      │    │ • Correlate simulations     │                    │
│   │                             │    │   with measurements         │                    │
│   │ Pain Points:                │    │                             │                    │
│   │ • Manual logbook entry      │    │ Pain Points:                │                    │
│   │ • Data scattered across     │    │ • Data in many formats      │                    │
│   │   systems                   │    │ • Manual data prep          │                    │
│   │ • Audit prep is tedious     │    │ • Hard to reproduce work    │                    │
│   └─────────────────────────────┘    └─────────────────────────────┘                    │
│                                                                                          │
│   ┌─────────────────────────────┐    ┌─────────────────────────────┐                    │
│   │     FACILITY MANAGER        │    │        INSPECTOR            │                    │
│   │        "Jordan"             │    │        "Morgan"             │                    │
│   │                             │    │                             │                    │
│   │ Role: Reactor Director      │    │ Role: NRC Inspector         │                    │
│   │                             │    │                             │                    │
│   │ Goals:                      │    │ Goals:                      │                    │
│   │ • Ensure compliance         │    │ • Verify data integrity     │                    │
│   │ • Track utilization         │    │ • Review operations logs    │                    │
│   │ • Plan experiments          │    │ • Audit trail completeness  │                    │
│   │                             │    │                             │                    │
│   │ Pain Points:                │    │ Pain Points:                │                    │
│   │ • Manual report generation  │    │ • Verifying unaltered       │                    │
│   │ • Coordinating schedules    │    │   records is difficult      │                    │
│   │ • Audit preparation burden  │    │ • Paper-based audits slow   │                    │
│   └─────────────────────────────┘    └─────────────────────────────┘                    │
│                                                                                          │
│   ┌─────────────────────────────┐    ┌─────────────────────────────┐                    │
│   │    DT RESEARCHER            │    │    DEPARTMENT HEAD          │                    │
│   │       "Chris"               │    │       "William"             │                    │
│   │                             │    │                             │                    │
│   │ Role: Digital Twin Dev      │    │ Role: Dept Head/Director    │                    │
│   │                             │    │                             │                    │
│   │ Goals:                      │    │ Goals:                      │                    │
│   │ • Log DT simulation runs    │    │ • Cross-team visibility     │                    │
│   │ • Validate predictions vs   │    │ • Access both ops & DT logs │                    │
│   │   measured data             │    │ • Audit oversight           │                    │
│   │ • Keep DT activity separate │    │                             │                    │
│   │   from ops log              │    │ Pain Points:                │                    │
│   │                             │    │ • Siloed information        │                    │
│   │ Pain Points:                │    │ • No unified view           │                    │
│   │ • No structured DT log      │    │                             │                    │
│   │ • Hard to correlate with    │    │                             │                    │
│   │   reactor conditions        │    │                             │                    │
│   └─────────────────────────────┘    └─────────────────────────────┘                    │
│                                                                                          │
│   SECONDARY USERS                                                                        │
│   ───────────────                                                                        │
│                                                                                          │
│   ┌─────────────────────────────┐    ┌─────────────────────────────┐                    │
│   │      DEVELOPER              │    │    EXTERNAL RESEARCHER      │                    │
│   │       "Sam"                 │    │        "Riley"              │                    │
│   │                             │    │                             │                    │
│   │ Role: Software Developer    │    │ Role: Visiting Scientist    │                    │
│   │                             │    │                             │                    │
│   │ Goals:                      │    │ Goals:                      │                    │
│   │ • Build data pipelines      │    │ • Access relevant data      │                    │
│   │ • Integrate simulations     │    │ • Collaborate on analysis   │                    │
│   │ • Extend platform           │    │                             │                    │
│   └─────────────────────────────┘    └─────────────────────────────┘                    │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Problem Statement

### 3.1 The Core Challenge: Sensor-Limited Operations

**The fundamental problem:** Physical sensors and processors have ~100ms latency to assess reactor state. During this time, the internal state of the reactor is essentially unknown. Critical transients can develop in <50ms.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                THE SENSOR LATENCY PROBLEM                                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│   Timeline: ─────────────────────────────────────────────────────────────────────────►  │
│                                                                                          │
│             t=0ms        t=50ms       t=100ms      t=150ms      t=200ms                 │
│               │            │            │            │            │                     │
│               ▼            ▼            ▼            ▼            ▼                     │
│           ┌──────┐                  ┌──────┐                  ┌──────┐                  │
│           │Sensor│                  │Sensor│                  │Sensor│                  │
│           │Read  │                  │Read  │                  │Read  │                  │
│           └──────┘                  └──────┘                  └──────┘                  │
│               │                        │                        │                       │
│               │    UNKNOWN STATE       │    UNKNOWN STATE       │                       │
│               │◄──────────────────────►│◄──────────────────────►│                       │
│                                                                                          │
│   CONSEQUENCE:                                                                           │
│   • Safety margins must be conservative to account for uncertainty                       │
│   • Cannot safely operate near optimal capacity                                          │
│   • Transients may not be detected until after they've progressed                        │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

**Why this matters:** If we can predict reactor state in ~10ms (via digital twin simulation), we gain continuous visibility into reactor behavior between sensor readings. This enables:
- Predictive safety margins (act before anomalies manifest)
- Higher capacity utilization (tighter operating envelopes)  
- Eventually: closed-loop simulation-driven control

### 3.2 Supporting Challenges

#### 3.2.1 Data Fragmentation

Reactor data, simulation outputs, and research results are stored in disparate systems (CSV files, HDF5, databases, spreadsheets) with no unified access layer. **This prevents effective ML model training for digital twins.**

#### 3.2.2 Manual Audit Burden

Preparing for NRC inspections requires significant manual effort to compile records and demonstrate their integrity. **This is critical for eventual closed-loop control approval.**

#### 3.2.3 Meeting Documentation Gap

Requirements and decisions made in meetings are not systematically captured and linked to project artifacts.

#### 3.2.4 Limited Time-Travel

Cannot easily query historical data states or understand how data has changed over time. **This limits ability to train models on specific historical scenarios.**

#### 3.2.5 Siloed Digital Twins

Each digital twin project (TRIGA, MSR, MIT Loop, OffGas) maintains separate tooling with duplicated effort.

---

## 4. Solution Overview

### 4.1 The Core Solution: Simulate-to-Operate

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│               NEUTRON OS: SIMULATE-TO-OPERATE SOLUTION                                   │
│                              [DRAFT v0.2]                                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│   THE CORE LOOP:                                                                         │
│                                                                                          │
│   ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                                                                 │   │
│   │     PHYSICAL REACTOR          NEUTRON OS           DIGITAL TWIN                │   │
│   │     ────────────────          ──────────           ────────────                │   │
│   │                                                                                 │   │
│   │     ┌──────────────┐         ┌──────────────┐     ┌──────────────┐             │   │
│   │     │              │  Sensor │              │ ML  │              │             │   │
│   │     │   Sensors    │─────────│ Data Ingest  │────▶│  Simulation  │             │   │
│   │     │   (~100ms)   │  Data   │ (Bronze)     │Train│  (~10ms)     │             │   │
│   │     │              │         │              │     │              │             │   │
│   │     └──────────────┘         └──────────────┘     └──────┬───────┘             │   │
│   │            │                                             │                      │   │
│   │            │                                             │ Predictions          │   │
│   │            │                 ┌──────────────┐             │                      │   │
│   │            │     Actual      │              │◄────────────┘                      │   │
│   │            └─────────────────│   Validate   │                                   │   │
│   │                              │   & Improve  │──────▶ Continuous accuracy       │   │
│   │                              │              │        improvement                │   │
│   │                              └──────────────┘                                   │   │
│   │                                                                                 │   │
│   └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                          │
│   VALUE:                                                                                 │
│   • 10x faster state assessment (10ms prediction vs 100ms sensor)                        │
│   • Continuous visibility between sensor readings                                        │
│   • Predictive safety margins                                                            │
│   • Future: Closed-loop simulation-driven control                                        │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Supporting Solutions

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         SUPPORTING CAPABILITIES                                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│   PROBLEM                           SOLUTION                        VALUE                │
│   ───────                           ────────                        ─────                │
│                                                                                          │
│   ┌─────────────────┐              ┌─────────────────┐             ┌─────────────────┐  │
│   │ Data scattered  │────────────▶ │ Unified         │────────────▶│ ML training     │  │
│   │ across systems  │              │ Lakehouse       │             │ data ready      │  │
│   └─────────────────┘              │ (Iceberg)       │             │                 │  │
│                                    └─────────────────┘             │ Query any data  │  │
│                                                                    │ with SQL        │  │
│                                                                    └─────────────────┘  │
│                                                                                          │
│   ┌─────────────────┐              ┌─────────────────┐             ┌─────────────────┐  │
│   │ Audit prep is   │────────────▶ │ Blockchain      │────────────▶│ Closed-loop     │  │
│   │ manual & tedious│              │ Audit Trail     │             │ approval ready  │  │
│   └─────────────────┘              │ (Fabric)        │             │                 │  │
│                                    └─────────────────┘             │ Cryptographic   │  │
│                                                                    │ proof           │  │
│                                                                    └─────────────────┘  │
│                                                                                          │
│   ┌─────────────────┐              ┌─────────────────┐             ┌─────────────────┐  │
│   │ No historical   │────────────▶ │ Time-Travel     │────────────▶│ Train on any    │  │
│   │ data queries    │              │ Queries         │             │ scenario        │  │
│   └─────────────────┘              │ (Iceberg)       │             │                 │  │
│                                    └─────────────────┘             │ Reproduce past  │  │
│                                                                    │ conditions      │  │
│                                                                    └─────────────────┘  │
│                                                                                          │
│   ┌─────────────────┐              ┌─────────────────┐             ┌─────────────────┐  │
│   │ Siloed digital  │────────────▶ │ Shared DT       │────────────▶│ Consistent      │  │
│   │ twins           │              │ Infrastructure  │             │ approach        │  │
│   └─────────────────┘              │                 │             │                 │  │
│                                    └─────────────────┘             │ Transfer        │  │
│                                                                    │ learning        │  │
│                                                                    └─────────────────┘  │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Feature Requirements

### 5.1 Feature Prioritization Matrix

| Feature | Priority | Effort | Value | Status |
|---------|----------|--------|-------|--------|
| Data Lakehouse (Bronze/Silver/Gold) | P0 | Large | Critical | In Progress |
| Superset Dashboards | P0 | Medium | Critical | In Progress |
| Reactor Operations Dashboard | P0 | Medium | High | Designed |
| Performance Analytics Dashboard | P0 | Medium | High | Designed |
| Unified Log System (Ops + DT) | P1 | Large | High | Designed (Jan 2026) |
| Meeting Intake Pipeline | P1 | Medium | Medium | Designed |
| Audit Evidence Generation | P1 | Medium | High | Planned |
| Sample/Experiment Tracking | P2 | Medium | Medium | Schema Designed |
| Measured vs Modeled Data Labels | P0 | Small | Critical | Designed (Jan 2026) |
| Multi-Facility Support | P2 | Large | High | Architecture |
| External Researcher Access | P3 | Medium | Low | Future |

> **Update (Jan 2026):** Per Nick Luciano's review, the Elog system is now a "Unified Log System" with `entry_type` discriminator supporting both Operations logs and Digital Twin activity logs. Access control allows DT researchers to include ops data if needed, while ops staff can be granted DT visibility (typically only department heads like William Charlton would use this).

### 5.2 Detailed Feature Specifications

#### 5.2.1 F1: Data Lakehouse

| Attribute | Specification |
|-----------|---------------|
| Description | Unified storage for all reactor, simulation, and research data |
| Technology | Apache Iceberg + DuckDB + dbt |
| Key Capabilities | Time-travel, schema evolution, SQL access |
| Data Sources | Reactor serial data, MPACT outputs, core configs, elogs |
| Acceptance Criteria | Gold tables available in Superset with < 2s query time |

#### 5.2.2 F2: Superset Dashboards

| Attribute | Specification |
|-----------|---------------|
| Description | Interactive analytics dashboards for reactor operations |
| Technology | Apache Superset |
| Key Dashboards | Ops Dashboard, Performance Analytics, Elog Activity, Audit |
| Data Source | Gold layer tables via DuckDB/Iceberg |
| Acceptance Criteria | Dashboards load < 3s, filters work correctly |

#### 5.2.3 F3: Unified Log System (Ops + DT)

| Attribute | Specification |
|-----------|---------------|
| Description | Unified logbook supporting both Operations and Digital Twin activity with access control |
| Technology | FastAPI + PostgreSQL + Hyperledger Fabric + Alembic migrations |
| Key Capabilities | CRUD operations, blockchain audit, evidence generation, entry_type filtering, role-based access |
| Reference | See detailed Elog PRD (GitLab #295), updated per Nick Luciano review Jan 2026 |
| Acceptance Criteria | Entries verified via blockchain proof, DT researchers can optionally include ops data |

**Entry Types:**
| entry_type | Description | Primary Users | Access |
|------------|-------------|---------------|--------|
| `ops` | Operations log entries (startup, shutdown, maintenance) | Operators, Facility Manager | Ops team, inspectors, dept heads |
| `dt` | Digital twin activity (simulation runs, predictions, validations) | DT Researchers | DT team, dept heads |
| `experiment` | Sample/experiment tracking entries | Researchers | Research team, dept heads |

**Access Control Model:**
- Operations staff: See `ops` entries by default
- DT researchers: See `dt` entries by default, can include `ops` if needed
- Department heads (e.g., William Charlton): See all entry types
- Inspectors: See `ops` entries only (audit scope)

#### 5.2.4 F4: Sample/Experiment Tracking

| Attribute | Specification |
|-----------|---------------|
| Description | Track samples from preparation through irradiation, decay, counting, and analysis |
| Technology | Unified log system with `entry_type='experiment'` + dedicated sample_tracking table |
| Key Capabilities | Unique sample IDs, metadata capture, irradiation location tracking, activity calculation |
| Reference | Requirements from Nick Luciano (Jan 2026), pending validation from Khiloni Shah |
| Acceptance Criteria | Complete sample lifecycle tracked, prepopulated dropdowns for locations/facilities |

**Sample Metadata Fields (per Nick Luciano):**
- Sample Name (unique), Sample ID (auto-assigned)
- Chemical Composition, Isotopic Composition, Density, Mass
- Irradiation Location (central thimble, lazy susan, etc.)
- Irradiation Facility (cadmium covered, bare, etc.)
- Datetime of insertion/removal, Decay time
- Count live time, Total counts, Total activity
- Activity by isotope, Measurement raw data (spectra)

> **[PLACEHOLDER: Additional Feature Specifications]**
> → Add detailed specs for remaining features as designed

---

## 6. User Journeys

### 6.1 Operator Daily Workflow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         OPERATOR DAILY JOURNEY - "ALEX"                                  │
│                              [DRAFT v0.1]                                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│   TIME        ACTION                              NEUTRON OS INTERACTION                 │
│   ────        ──────                              ──────────────────────                 │
│                                                                                          │
│   7:00 AM     Start shift                         Open Ops Dashboard                     │
│               ──────────                          ──────────────────────                 │
│               │                                   │                                      │
│               │                                   ▼                                      │
│               │                                   ┌────────────────────────┐             │
│               │                                   │ • View overnight power │             │
│               │                                   │ • Check any anomalies  │             │
│               │                                   │ • Review rod positions │             │
│               │                                   └────────────────────────┘             │
│                                                                                          │
│   7:30 AM     Log shift start                     Create Elog entry                      │
│               ───────────────                     ─────────────────────                  │
│               │                                   │                                      │
│               │                                   ▼                                      │
│               │                                   ┌────────────────────────┐             │
│               │                                   │ • Enter shift start    │             │
│               │                                   │ • Note any handoff     │             │
│               │                                   │   issues               │             │
│               │                                   │ • Auto-hash to chain   │             │
│               │                                   └────────────────────────┘             │
│                                                                                          │
│   9:00 AM     Monitor startup                     Real-time dashboard                    │
│               ───────────────                     ────────────────────                   │
│               │                                   │                                      │
│               │                                   ▼                                      │
│               │                                   ┌────────────────────────┐             │
│               │                                   │ • Watch power ramp     │             │
│               │                                   │ • Monitor temps        │             │
│               │                                   │ • Track rod movement   │             │
│               │                                   └────────────────────────┘             │
│                                                                                          │
│   12:00 PM    Log observation                     Quick elog entry                       │
│               ───────────────                     ────────────────────                   │
│               │                                   │                                      │
│               │                                   ▼                                      │
│               │                                   ┌────────────────────────┐             │
│               │                                   │ • Note rod calibration │             │
│               │                                   │ • Attach data ref      │             │
│               │                                   │ • Blockchain commit    │             │
│               │                                   └────────────────────────┘             │
│                                                                                          │
│   3:00 PM     End shift                           Close elog + handoff                   │
│               ─────────                           ─────────────────────                  │
│               │                                   │                                      │
│               │                                   ▼                                      │
│               │                                   ┌────────────────────────┐             │
│               │                                   │ • Summary entry        │             │
│               │                                   │ • Shift metrics auto   │             │
│               │                                   │ • Handoff notes        │             │
│               │                                   └────────────────────────┘             │
│                                                                                          │
│   VALUE: Reduced manual logging, verified audit trail, real-time visibility              │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Inspector Audit Workflow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         INSPECTOR AUDIT JOURNEY - "MORGAN"                               │
│                              [DRAFT v0.1]                                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│   STEP        ACTION                              NEUTRON OS INTERACTION                 │
│   ────        ──────                              ──────────────────────                 │
│                                                                                          │
│   1           Request audit scope                 Facility provides access               │
│               ────────────────────                ──────────────────────                 │
│               │                                   │                                      │
│               │                                   ▼                                      │
│               │                                   ┌────────────────────────┐             │
│               │                                   │ • Inspector account    │             │
│               │                                   │   created              │             │
│               │                                   │ • Date range scoped    │             │
│               │                                   │ • Read-only access     │             │
│               │                                   └────────────────────────┘             │
│                                                                                          │
│   2           Query operations logs               Audit Dashboard                        │
│               ────────────────────                ───────────────────                    │
│               │                                   │                                      │
│               │                                   ▼                                      │
│               │                                   ┌────────────────────────┐             │
│               │                                   │ • Filter by date       │             │
│               │                                   │ • Search keywords      │             │
│               │                                   │ • View entry details   │             │
│               │                                   └────────────────────────┘             │
│                                                                                          │
│   3           Verify data integrity               Blockchain verification                │
│               ────────────────────                ──────────────────────                 │
│               │                                   │                                      │
│               │                                   ▼                                      │
│               │                                   ┌────────────────────────┐             │
│               │                                   │ • Select records       │             │
│               │                                   │ • Click "Verify"       │             │
│               │                                   │ • View Merkle proof    │             │
│               │                                   │ • Confirmation shown   │             │
│               │                                   └────────────────────────┘             │
│                                                                                          │
│   4           Generate evidence package           Export to PDF/ZIP                      │
│               ────────────────────────            ────────────────────                   │
│               │                                   │                                      │
│               │                                   ▼                                      │
│               │                                   ┌────────────────────────┐             │
│               │                                   │ • Select scope         │             │
│               │                                   │ • Generate package     │             │
│               │                                   │ • Includes:            │             │
│               │                                   │   - Data records       │             │
│               │                                   │   - Blockchain proofs  │             │
│               │                                   │   - Audit log          │             │
│               │                                   └────────────────────────┘             │
│                                                                                          │
│   VALUE: Self-service audit, cryptographic proof, reduced facility burden                │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Success Metrics

### 7.1 Key Performance Indicators

| Metric | Current State | Target (6 mo) | Target (12 mo) |
|--------|---------------|---------------|----------------|
| Audit prep time | 2 weeks | 2 days | < 1 day |
| Data query time | Hours (manual) | < 5 seconds | < 2 seconds |
| Meeting→GitLab latency | Days (manual) | < 1 hour | < 15 minutes |
| Data source coverage | 20% | 60% | 90% |
| Dashboard adoption | 0 users | 10 users | 50+ users |
| Blockchain-verified records | 0% | 80% | 100% |

### 7.2 User Satisfaction Targets

| Persona | Satisfaction Metric | Target |
|---------|---------------------|--------|
| Operator | Elog entry time | < 2 minutes per entry |
| Researcher | Data access ease (1-5) | ≥ 4.0 |
| Facility Manager | Audit confidence (1-5) | ≥ 4.5 |
| Inspector | Verification time | < 30 minutes |

---

## 8. Roadmap

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              NEUTRON OS ROADMAP                                          │
│                              [DRAFT v0.1]                                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│   Q1 2026                Q2 2026                Q3 2026                Q4 2026           │
│   ───────                ───────                ───────                ───────           │
│                                                                                          │
│   ┌─────────────┐       ┌─────────────┐       ┌─────────────┐       ┌─────────────┐    │
│   │ FOUNDATION  │       │  ANALYTICS  │       │   AUDIT     │       │   SCALE     │    │
│   │             │       │             │       │             │       │             │    │
│   │ □ Lakehouse │       │ □ Ops Dash  │       │ □ Elog v1   │       │ □ Multi-    │    │
│   │   setup     │       │   MVP       │       │             │       │   facility  │    │
│   │             │       │             │       │ □ Blockchain│       │             │    │
│   │ □ Bronze    │       │ □ Perf      │       │   integration       │ □ External  │    │
│   │   ingestion │       │   Analytics │       │             │       │   access    │    │
│   │             │       │             │       │ □ Evidence  │       │             │    │
│   │ □ dbt       │       │ □ Gold      │       │   generation│       │ □ Additional│    │
│   │   models    │       │   tables    │       │             │       │   projects  │    │
│   │             │       │             │       │ □ Meeting   │       │             │    │
│   │ □ Superset  │       │ □ Elog      │       │   intake    │       │ □ Commercial│    │
│   │   setup     │       │   design    │       │   MVP       │       │   pilot     │    │
│   │             │       │             │       │             │       │             │    │
│   └─────────────┘       └─────────────┘       └─────────────┘       └─────────────┘    │
│         │                     │                     │                     │            │
│         ▼                     ▼                     ▼                     ▼            │
│   ┌─────────────┐       ┌─────────────┐       ┌─────────────┐       ┌─────────────┐    │
│   │ MILESTONE:  │       │ MILESTONE:  │       │ MILESTONE:  │       │ MILESTONE:  │    │
│   │ Data        │       │ Dashboards  │       │ Audit-ready │       │ Production  │    │
│   │ queryable   │       │ in use      │       │ elog        │       │ multi-site  │    │
│   └─────────────┘       └─────────────┘       └─────────────┘       └─────────────┘    │
│                                                                                          │
│   ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                          │
│   DEPENDENCIES:                                                                          │
│   • Q1: Infrastructure hosting decision needed                                           │
│   • Q2: Nick's Superset scenario input needed                                           │
│   • Q3: NRC feedback on blockchain audit approach                                       │
│   • Q4: Partner facility identified for multi-site pilot                                │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Dependencies & Risks

### 9.1 Critical Dependencies

| Dependency | Owner | Status | Mitigation |
|------------|-------|--------|------------|
| Infrastructure hosting decision | Team | Pending | K3D for local dev |
| Superset scenario requirements | Nick Luciano | In Progress | Draft scenarios created |
| GitLab API access | IT | Available | N/A |
| MPACT output format documentation | Simulation team | Needed | Reverse engineer |
| NRC audit requirements clarity | Facility | Ongoing | Conservative approach |

### 9.2 Risk Register

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| Hosting delays | Medium | High | Local K3D development continues |
| Scope creep | High | Medium | Strict prioritization, MVP focus |
| Data quality issues | Medium | Medium | dbt tests, quality gates |
| Adoption resistance | Medium | Medium | Early user involvement, training |
| Blockchain complexity | Medium | Medium | Immudb fallback for dev |

---

## 10. Appendices

### A. Related Documents

- Neutron OS Technical Specification (companion document)
- Elog PRD (GitLab #295)
- Data Platform PRD
- Superset Scenarios for Review
- Architecture Decision Records (ADRs)

### B. Stakeholder Sign-off

| Stakeholder | Role | Date | Signature |
|-------------|------|------|-----------|
| [TBD] | Product Owner | | |
| [TBD] | Technical Lead | | |
| Nick Luciano | Domain Expert | | |
| [TBD] | Facility Representative | | |

### C. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-01-15 | Auto-generated | Initial draft for review |

---

*Document generated: January 15, 2026*
