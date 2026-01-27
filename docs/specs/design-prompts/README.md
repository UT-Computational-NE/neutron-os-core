# Design Prompts

This directory contains **actionable implementation specifications** for Neutron OS components. Each prompt is designed to guide Claude Code (or a developer) through building a specific piece of the system.

## What Are Design Prompts?

Design prompts are detailed specifications that include:
- **Context**: Why this component exists, what it depends on
- **Objective**: What needs to be built, with clear success criteria
- **Structure**: File/module organization
- **Specifications**: Schemas, APIs, data flows
- **Code Examples**: Reference implementations
- **Tests**: What needs to be validated

They're written to be **directly usable** as prompts for AI-assisted development or as specs for human developers.

## Prompt Inventory

**Dual-Track Development:** Phase 1a ("data puddle") delivers dashboards immediately; Phase 1b builds proper foundation.

| Prompt | Phase | Track | Status | Description |
|--------|-------|-------|--------|-------------|
| [Superset Dashboards](prompt-superset-dashboards.md) | **1a** | 🟢 **Puddle MVP** | 📝 Ready | DMSRI-web PostgreSQL → Superset (start now) |
| [Bronze Layer Ingest](prompt-bronze-layer-ingest.md) | 1b | Foundation | 📝 Ready | CSV → Iceberg ingestion pipeline |
| [dbt Silver Models](prompt-dbt-silver-models.md) | 1b-2 | Foundation | 📝 Ready | Data transformation and validation |
| [Dagster Orchestration](prompt-dagster-orchestration.md) | 2 | Foundation | 📝 Ready | Pipeline scheduling and monitoring |
| Meeting Intelligence | 5 | Agentic | ⏳ Planned | LangGraph audio → requirements pipeline |
| Digital Twin Inference | 4 | Real-Time | ⏳ Planned | Surrogate model serving |
| Blockchain Audit | 6 | Compliance | ⏳ Planned | Hyperledger integration |

**Start here:** Jay can use the Superset prompt to stand up dashboards on the existing DMSRI-web PostgreSQL database immediately—no Iceberg or dbt required. The puddle migrates to proper infrastructure (Bronze → dbt → Dagster) in Phase 2.

## How to Use These Prompts

### With Claude Code

```
Read the design prompt at docs/specs/design-prompts/prompt-bronze-layer-ingest.md
and implement the Bronze layer ingestion module following the specifications.
```

### With Human Developers

1. Read the prompt to understand scope and requirements
2. Use the structure section to set up files
3. Implement the core functions as specified
4. Write tests matching the test requirements
5. Validate against success criteria

## Dependency Graph

```
┌────────────────────┐
│  Bronze Ingest     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  dbt Silver Models │
└─────────┬──────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌────────┐  ┌────────────┐
│ Dagster│  │  Superset  │
│  Orch  │  │ Dashboards │
└────────┘  └────────────┘
```

Build in order: Bronze → dbt → Dagster/Superset (parallel).

## Prompt Template

When creating new design prompts, follow this structure:

```markdown
# Design Prompt: [Component Name]

**Component:** [Category]
**Phase:** [1-6]
**Priority:** [P0-P2]
**Estimated Effort:** [X days]
**Depends On:** [Links to dependencies]

---

## Context for Implementation
[Why this exists, prerequisites]

## Objective
[What to build, constraints]

## Project Structure
[Directory layout]

## Specifications
[Detailed requirements, schemas, APIs]

## Testing Requirements
[Test cases, coverage expectations]

## Success Criteria
[Measurable outcomes]

## Usage
[How to run/test the component]

## Follow-Up Components
[What depends on this]
```

---

*These prompts are part of the Neutron OS documentation. See [Executive Summary](../neutron-os-executive-summary.md) for project context.*
