# Elog (Operations Log) PRD

**Product:** Neutron OS Elog System  
**Status:** Draft  
**Last Updated:** 2026-01-14

---

## Overview

The Elog (electronic logbook) is the official record of nuclear reactor operations. It captures operator actions, observations, and reactor state for regulatory compliance, operational continuity, and historical analysis.

## Seed Requirements

Initial requirements captured in GitLab:
- **Issue #295:** [rsicc-gitlab.tacc.utexas.edu/ut-computational-ne/triga_digital_twin/netl_triga_digital_twin/-/issues/295](https://rsicc-gitlab.tacc.utexas.edu/ut-computational-ne/triga_digital_twin/netl_triga_digital_twin/-/issues/295)

The final implementation will significantly exceed these initial requirements.

---

## User Personas

| Persona | Description | Primary Needs |
|---------|-------------|---------------|
| **Reactor Operator** | Licensed operator running the reactor | Fast entry, run tracking, shift handoff |
| **Facility Manager** | Oversees operations, reviews logs | Search, reporting, anomaly detection |
| **Regulatory Inspector** | NRC or equivalent | Tamper-proof records, evidence export |
| **Researcher** | Uses reactor for experiments | Correlate logs with experiment data |

---

## Problem Statement

### Current State
- Elog stored as JSON files per day
- No immutability guarantees
- Basic authentication (plaintext passwords)
- No search across historical logs
- Manual PDF generation for inspections
- No approval/signature workflow

### Future State
- Immutable log entries (Hyperledger Fabric)
- SSO with role-based access (Keycloak)
- Full-text search across all logs
- Automated evidence package generation
- Digital signature workflow
- Real-time reactor state correlation

---

## Requirements

### Epic: Core Elog Functionality

| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| EL-001 | Authenticated operator log entry creation | P0 | Issue #295 |
| EL-002 | Run number tracking and association | P0 | Issue #295 |
| EL-003 | Date/time stamped entries | P0 | Issue #295 |
| EL-004 | Log entry categories (startup, shutdown, observation, maintenance) | P1 | New |
| EL-005 | Attach files/images to entries | P1 | New |
| EL-006 | Shift handoff notes | P1 | New |

### Epic: Immutability & Compliance

| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| EL-010 | Immutable log storage (Hyperledger) | P0 | Architecture |
| EL-011 | Cryptographic proof of entry integrity | P0 | Architecture |
| EL-012 | Entry cannot be deleted, only amended | P0 | Regulatory |
| EL-013 | Amendment history visible | P1 | Regulatory |
| EL-014 | Multi-facility attestation | P2 | Commercialization |

### Epic: Search & Retrieval

| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| EL-020 | Full-text search across all logs | P0 | Issue #295 |
| EL-021 | Filter by date range | P0 | Issue #295 |
| EL-022 | Filter by operator | P1 | New |
| EL-023 | Filter by run number | P0 | Issue #295 |
| EL-024 | Filter by category/tags | P1 | New |
| EL-025 | Export search results to PDF | P1 | Issue #295 |

### Epic: Authentication & Authorization

| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| EL-030 | Keycloak SSO integration | P0 | Architecture |
| EL-031 | Role-based access (operator, supervisor, viewer) | P0 | Architecture |
| EL-032 | Supervisory approval for certain entry types | P2 | New |
| EL-033 | Audit log of who viewed what | P1 | Regulatory |

### Epic: Integration

| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| EL-040 | Correlate log entries with reactor time-series data | P1 | New |
| EL-041 | Link to experiments conducted during run | P2 | New |
| EL-042 | Automatic reactor state snapshot with entry | P2 | New |
| EL-043 | API for programmatic log queries | P1 | New |

### Epic: Audit & Evidence

| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| EL-050 | Generate evidence package for date range | P0 | Regulatory |
| EL-051 | Include Merkle proof in evidence package | P0 | Architecture |
| EL-052 | Evidence package includes related reactor data | P1 | New |
| EL-053 | Evidence package PDF with cryptographic seal | P1 | New |

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Entry creation time | < 30 seconds |
| Search response time | < 2 seconds |
| Evidence package generation | < 5 minutes |
| System availability | 99.9% |
| Verification API latency | < 1 second |

---

## Out of Scope (This Version)

- Voice-to-text entry (future)
- Mobile app (future)
- Real-time collaborative editing (future)
- Integration with external reactor control systems (future)

---

## Technical Dependencies

- Hyperledger Fabric network (ADR-002)
- Keycloak SSO (planned)
- PostgreSQL + pgvector (ADR-003)
- Data lakehouse integration (ADR-003)

---

## Open Questions

1. What entry types require supervisory approval?
2. How long must amendments be traceable? (Regulatory input needed)
3. Should entries be digitally signed by individual operators?
4. What is the maximum acceptable latency for blockchain confirmation?
