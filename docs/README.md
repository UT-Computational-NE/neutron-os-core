# Neutron OS Documentation

This folder contains all documentation for the Neutron OS platform.

## Structure

```
docs/
├── README.md                 # This file
├── adr/                      # Architecture Decision Records
├── prd/                      # Product Requirements Documents
├── specs/                    # Technical Specifications
├── scenarios/                # Analytics & use case scenarios
├── strategy/                 # Business strategy & commercialization
├── standards/                # Reusable frameworks & guides
├── program/                  # Project-specific planning (OKRs, milestones)
├── research/                 # Analysis, assessments, user research
└── _tools/                   # Documentation generator scripts
```

## Folder Descriptions

### [`adr/`](adr/) - Architecture Decision Records

**What goes here:** Significant, hard-to-reverse technical decisions. "One-way doors."

ADRs are immutable once accepted—supersede rather than edit.

**Examples:**
- ✅ "We will use Hyperledger for multi-facility consensus" (ADR-002)
- ✅ "We will use Iceberg + DuckDB for the lakehouse" (ADR-003)
- ❌ Feature designs (→ specs/)
- ❌ Research/analysis (→ specs/research/)

**Naming:** `NNN-short-description.md` (e.g., `001-polyglot-monorepo-bazel.md`)

### [`prd/`](prd/) - Product Requirements Documents

**What goes here:** What we're building and why. User-facing requirements, user journeys, success metrics.

**Document Hierarchy:**
- **[Executive PRD](prd/neutron-os-executive-prd.md):** Platform overview, module relationships, rollout plan
- **Module PRDs:** Detailed requirements for each Neutron OS module

**Current PRDs:**
| Document | Scope |
|----------|-------|
| [Executive PRD](prd/neutron-os-executive-prd.md) | Platform overview |
| [Data Platform PRD](prd/data-platform-prd.md) | Lakehouse, ingestion |
| [Reactor Ops Log PRD](prd/reactor-ops-log-prd.md) | Operations & experiment logging |
| [Experiment Manager PRD](prd/experiment-manager-prd.md) | Sample tracking, scheduling |
| [Analytics Dashboards PRD](prd/analytics-dashboards-prd.md) | Superset visualizations |
| [Medical Isotope PRD](prd/medical-isotope-prd.md) | Production & fulfillment (optional) |

**All PRDs include Mermaid journey maps** for easy visualization and AI-assisted diagram generation.

**Examples:**
- ✅ User journeys with emotional arc
- ✅ State machines for entity lifecycles
- ✅ System integration diagrams
- ❌ How to build it (→ specs/)
- ❌ Technology choices (→ adr/)

### [`specs/`](specs/) - Technical Specifications & Research

**What goes here:** How we'll build things. Implementation details. Research and analysis.

- **Master Tech Spec:** System architecture and component designs
- **Feature Specs:** Detailed technical designs for features
- **API Specs:** OpenAPI/Swagger definitions
- **Research:** Analysis, assessments, external comparisons
- **Proposals:** Grant applications, partnership documents

**Examples:**
- ✅ "Master Tech Spec" - architecture, APIs, data models
- ✅ "DeepLynx Assessment" - research/analysis
- ✅ "CINR Pre-Application" - proposal draft
- ✅ "Hyperledger Use Cases" - research/vision
- ❌ What users need (→ prd/)
- ❌ Irreversible decisions (→ adr/)

### [`scenarios/`](scenarios/) - User Scenarios & Test Cases

**What goes here:** Concrete examples of how users interact with the system. Test-first development.

Dashboard and analytics scenarios organized by tool:
- **superset/**: Apache Superset dashboard scenarios

**Examples:**
- ✅ "Operator views 7-day power trend" - specific scenario
- ✅ "Inspector generates audit evidence package" - user story with steps
- ❌ Generic requirements (→ prd/)
- ❌ Implementation (→ specs/)

### [`strategy/`](strategy/) - Business Strategy

**What goes here:** Commercialization roadmaps, market positioning, business model documents.

**Contents:**
- [commercialization-roadmap.md](strategy/commercialization-roadmap.md) - Neutron OS vision, market opportunity, revenue models

### [`standards/`](standards/) - Reusable Frameworks & Guides

**What goes here:** Templates and methodologies applicable across projects.

**Contents:**
- [metrics-framework.md](standards/metrics-framework.md) - Platform success metrics by category
- [stakeholder-interview-guide.md](standards/stakeholder-interview-guide.md) - How to conduct user research interviews
- [mermaid-diagram-best-practices.md](standards/mermaid-diagram-best-practices.md) - Diagram conventions

### [`program/`](program/) - Project-Specific Planning

**What goes here:** Per-project OKRs, milestones, and roadmaps. Organized by project subfolder.

**Structure:**
- `program/triga/` - TRIGA Digital Twin planning
  - [okrs-2026.md](program/triga/okrs-2026.md) - 2026 Objectives & Key Results

### [`research/`](research/) - Analysis & User Research

**What goes here:** Assessments, comparisons, user personas, grant applications.

**Key documents:**
- [user-personas.md](research/user-personas.md) - Target user "Why Chain" analysis
- [deeplynx-assessment.md](research/deeplynx-assessment.md) - INL DeepLynx evaluation
- [CINR_PreApp_Concept_Draft.md](research/CINR_PreApp_Concept_Draft.md) - CINR grant application

### [`_tools/`](_tools/) - Generator Scripts

Python scripts for generating documentation (Word docs, etc.). Prefixed with `_` to sort last and indicate internal tooling.

## Document Lifecycle

1. **Draft** → Initial creation, circulate for review
2. **In Review** → Gathering stakeholder feedback
3. **Accepted** → Approved and active
4. **Superseded** → Replaced by newer version (for ADRs)

## Conventions

- Use lowercase-kebab-case for folder and file names
- Include `DRAFT` in filename for documents under review
- Keep Word (.docx) and Markdown (.md) versions in sync
- Reference GitLab issues where applicable (e.g., "See #295")

## Quick Links

| Document | Description |
|----------|-------------|
| [Executive PRD](prd/neutron-os-executive-prd.md) | Platform vision, features, roadmap |
| [Master Tech Spec](specs/neutron-os-master-tech-spec.md) | Architecture, data design, components |
| [Reactor Ops Log PRD](prd/reactor-ops-log-prd.md) | Operations & experiment log requirements |
| [Data Platform PRD](prd/data-platform-prd.md) | Lakehouse requirements |
