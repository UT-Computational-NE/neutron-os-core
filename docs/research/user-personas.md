# User Personas

> **Last Updated:** February 2026  
> **Origin:** TRIGA Digital Twin project (generalized for Neutron OS)

---

## Overview

This document defines target user personas for nuclear facility digital twin platforms, their surface-level needs, and the deeper underlying motivations that drive their behavior. While examples reference TRIGA/NETL, the personas apply to research reactors generally.

> **See also:** [Executive PRD](../prd/neutron-os-executive-prd.md) for user categories and module mapping.

---

## Persona 1: Reactor Operator

### Profile
- **Role:** Licensed reactor operator at NETL facility
- **Frequency:** Daily interaction with reactor, occasional portal use
- **Technical Level:** Operational expertise, limited data science background

### Surface Benefit
Review past operations, validate observations

### Why Chain (Underlying Motivation)

| Level | Why? |
|-------|------|
| 1 | Need to confirm what happened during a shift |
| 2 | Because manual logs are incomplete and memory is fallible |
| 3 | Because regulatory compliance requires accurate records |
| 4 | Because license renewal and incident response depend on defensible documentation |

### Root Motivation
> **Risk mitigation & professional accountability** - "I need proof that I did my job correctly"

### Key Features
- Data Browser with date selection
- CSV downloads for offline analysis
- Visualization of operational parameters

### Success Indicator
Operator voluntarily uses portal to verify shift events

---

## Persona 2: Nuclear Engineering Researcher

### Profile
- **Role:** Graduate student or faculty conducting reactor physics research
- **Frequency:** Weekly to monthly, project-driven
- **Technical Level:** High - comfortable with HDF5, SQL, Python

### Surface Benefit
Access simulation results, test hypotheses

### Why Chain (Underlying Motivation)

| Level | Why? |
|-------|------|
| 1 | Need data to validate computational models |
| 2 | Because publications require real-world benchmarks |
| 3 | Because funding agencies demand demonstrated code accuracy |
| 4 | Because inaccurate simulations → bad reactor designs → safety/economic failures |

### Root Motivation
> **Scientific credibility & career advancement** - "I need my models to be trusted by peers and funders"

### Key Features
- MPACT simulation outputs (HDF5)
- TimescaleDB queries
- Measured vs predicted comparisons
- Citable validation datasets

### Success Indicator
Publication or thesis citing TRIGA DT data

---

## Persona 3: Graduate Student (Learning)

### Profile
- **Role:** M E 390G (Nuclear Engineering Laboratory), M E 361E (Reactor Operations), or M E 336P student
- **Frequency:** Semester-based, homework-driven
- **Technical Level:** Developing - learning reactor physics concepts

### Surface Benefit
Learn reactor physics interactively

### Why Chain (Underlying Motivation)

| Level | Why? |
|-------|------|
| 1 | Need to understand how control rods affect reactivity |
| 2 | Because textbook equations don't build intuition |
| 3 | Because hands-on reactor time is scarce and expensive |
| 4 | Because employers expect practical understanding, not just theory |

### Root Motivation
> **Employability & confidence** - "I need to feel competent before I'm responsible for a real reactor"

### Key Features
- Point Kinetics Simulator
- AI Chatbot for Q&A
- Historical operation examples

### Success Indicator
Student reports increased confidence in reactor concepts

---

## Persona 4: Facility Manager

### Profile
- **Role:** NETL facility director or reactor supervisor
- **Frequency:** Monthly reviews, inspection prep
- **Technical Level:** Management focus, not hands-on technical

### Surface Benefit
Operational logs, compliance documentation

### Why Chain (Underlying Motivation)

| Level | Why? |
|-------|------|
| 1 | Need to satisfy NRC inspection requirements |
| 2 | Because violations → fines, shutdowns, license revocation |
| 3 | Because the facility's existence depends on regulatory standing |
| 4 | Because the university's research mission requires an operating reactor |

### Root Motivation
> **Institutional survival** - "I need to keep this facility open and funded"

### Key Features
- Compliance report generation
- Complete historical archives
- Audit trail documentation
- Anomaly detection alerts

### Success Indicator
Inspection preparation time reduced by 50%

---

## Persona 5: MPACT Code Developer

### Profile
- **Role:** Developer on VERA/MPACT team (ORNL, INL, or similar)
- **Frequency:** Occasional, V&V campaign-driven
- **Technical Level:** Expert - deep code knowledge

### Surface Benefit
Real-world validation data for code V&V

### Why Chain (Underlying Motivation)

| Level | Why? |
|-------|------|
| 1 | Need measured data to compare against predictions |
| 2 | Because V&V is required for NQA-1 qualification |
| 3 | Because unqualified codes can't be used for licensing calculations |
| 4 | Because DOE/NRC won't fund or approve tools they can't trust |

### Root Motivation
> **Market access & regulatory acceptance** - "I need my code to be licensable so it gets adopted"

### Key Features
- Standardized validation datasets
- Uncertainty quantification
- Measured vs predicted with documented conditions
- Reproducible simulation inputs

### Success Indicator
MPACT team references TRIGA DT in V&V documentation

---

## Persona 6: Medical Isotope Coordinator

### Profile
- **Role:** Hospital/clinic radiation oncology staff, nuclear pharmacy, or facility director fielding isotope requests
- **Frequency:** On-demand, urgent, time-critical (isotope half-lives measured in hours/days)
- **Technical Level:** Medical/clinical - not reactor physics experts

### Surface Benefit
Rapid, reliable medical isotope production scheduling

### Why Chain (Underlying Motivation)

| Level | Why? |
|-------|------|
| 1 | Need specific isotopes for patient treatment or diagnostic imaging |
| 2 | Because isotope half-lives are short - delays mean unusable product |
| 3 | Because patients are scheduled for procedures that can't wait |
| 4 | Because cancer treatment outcomes depend on timely access to radiopharmaceuticals |

### Root Motivation
> **Patient outcomes & clinical reliability** - "I need isotopes delivered on-schedule so my patients get treated"

### Key Features (Current State → Ideal State)
| Current | Ideal |
|---------|-------|
| Phone call to Dr. Charlton | Self-service request portal |
| Manual Word doc with criticality data | Automated simulation + ops package |
| Ad-hoc student/staff assignment | Streamlined workflow with SLAs |
| No visibility into reactor schedule | Real-time availability calendar |

### Success Indicator
Isotope request-to-delivery time reduced by 50%; SLA tracking implemented

---

## Persona 7: Isotope Production Operator

### Profile
- **Role:** Reactor operator or staff member executing isotope irradiation runs
- **Frequency:** As-needed based on medical orders
- **Technical Level:** High - licensed operator with physics background

### Surface Benefit
Clear, reliable production parameters without manual coordination

### Why Chain (Underlying Motivation)

| Level | Why? |
|-------|------|
| 1 | Need accurate criticality data and irradiation parameters |
| 2 | Because incorrect parameters → wrong isotope activity or failed production |
| 3 | Because failed production means patient treatment delayed |
| 4 | Because lives depend on reliable isotope supply |

### Root Motivation
> **Operational confidence & patient safety** - "I need to know exactly what to do so I don't fail a production run"

### Key Features
- Automated simulation package generation
- Pre-calculated criticality configurations
- Production checklist and procedures
- Real-time monitoring during irradiation

### Success Indicator
Zero failed production runs due to incorrect parameters

---

## User Priority Matrix

| Persona | Impact | Effort to Serve | Priority |
|---------|--------|-----------------|----------|
| Reactor Operator | High | Medium | **P1** |
| Researcher | High | Low (existing features) | **P1** |
| **Medical Isotope Coordinator** | **Very High** | **High (new features)** | **P1** |
| Student (Learning) | Medium | Low | **P2** |
| Facility Manager | High | High (new features) | **P2** |
| Code Developer | Medium | Medium | **P3** |
| Isotope Production Operator | High | Medium | **P2** |

---

## Jobs to Be Done (JTBD)

| When... | I want to... | So I can... |
|---------|--------------|-------------|
| After a shift | Review what happened | Verify my observations and log accurately |
| Writing a paper | Access validation data | Support my claims with real measurements |
| Studying for exam | Practice with simulator | Build intuition for reactor behavior |
| Preparing for inspection | Generate compliance reports | Demonstrate regulatory adherence |
| Developing MPACT | Compare predictions | Quantify and improve code accuracy |
| **Receiving isotope order** | **Quickly schedule production & generate ops package** | **Deliver isotopes before they decay** |
| **Running isotope production** | **Have pre-validated criticality parameters** | **Execute production confidently and correctly** |
