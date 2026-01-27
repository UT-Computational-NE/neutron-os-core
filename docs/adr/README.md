# Architecture Decision Records (ADRs)

This folder contains Architecture Decision Records documenting significant technical decisions for Neutron OS.

## What is an ADR?

An ADR captures an architecturally significant decision along with its context and consequences. ADRs are:

- **Immutable:** Once accepted, don't edit—create a new ADR that supersedes
- **Numbered:** Sequential numbering for easy reference
- **Contextual:** Include the "why" not just the "what"

## Current ADRs

| # | Title | Status |
|---|-------|--------|
| [001](001-polyglot-monorepo-bazel.md) | Build System: Bazel for Polyglot Monorepo | Proposed |
| [002](002-hyperledger-fabric-multi-facility.md) | Blockchain: Hyperledger Fabric for Multi-Facility Audit | Proposed |
| [003](003-lakehouse-iceberg-duckdb-superset.md) | Lakehouse: Apache Iceberg + DuckDB + Superset | Proposed |
| [004](004-infrastructure-terraform-k8s-helm.md) | Infrastructure: Terraform + K8s + Helm | Proposed |
| [005](005-meeting-intake-pipeline.md) | Meeting Intake: LangGraph + Anthropic + pgvector | Proposed |
| [006](006-mcp-server-agentic-access.md) | MCP Server for Agentic Data Access | Proposed |
| [007](007-streaming-first-architecture.md) | Streaming-First Architecture with Batch Fallbacks | Proposed |

## ADR Template

When creating a new ADR, use this structure:

```markdown
# ADR-NNN: Title

## Status
Proposed | Accepted | Deprecated | Superseded by ADR-XXX

## Context
What is the issue that we're seeing that motivates this decision?

## Decision
What is the change that we're proposing and/or doing?

## Consequences
What becomes easier or more difficult because of this change?
```

## Creating a New ADR

1. Determine the next number (current max + 1)
2. Create file: `NNN-short-description.md`
3. Fill in template sections
4. Submit for review via GitLab MR
5. Update this README table when accepted
