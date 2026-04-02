# RAG Community Corpus & Federated Knowledge — Neutron OS Nuclear Extensions

> The core specification is provided by the Axiom platform. This document defines nuclear-domain extensions only.

**Upstream:** [Axiom RAG Community Corpus Spec](https://github.com/…/axiom/docs/tech-specs/spec-rag-community.md)

---

## Nuclear Extensions

### Founding Federation Members

The three founding federation members are nuclear research reactor facilities:

- **UT-Austin NETL** (TRIGA Mark II)
- **OSU TRIGA** (TRIGA Mark II)
- **INL NRAD** (TRIGA Mark II)

### Nuclear Domain Packs

| Pack | Default `access_tier` | Primary content sources |
|------|---|---|
| `procedures` | `public` / `restricted` | NRC regulations, DOE standards, IAEA safety guides, facility procedures |
| `simulation-codes` | `public` / `classified` | MCNP6, SCALE, OpenMC documentation; classified content via RED path only |
| `nuclear-data` | `public` | ENDF/JEFF cross-section libraries |
| `reduced-order-models` | `public` / `classified` | ROM cards, validation datasets |
| `research` | `public` | Published papers, experiment reports |
| `medical-isotope` | `public` | Radioisotope production procedures, QA/QC |
| `training` | `public` | Training reactor operations, lab procedures |
| `regulation-compliance` | `public` | 10 CFR parts, DOE orders, facility license conditions |

### Nuclear-Specific Domain Tags

Federation fact propositions use nuclear domain tags such as `reactor_operations` (vs. Axiom's generic `system_operations`).

### Federation Knowledge Flow

> **Implementation Status (2026-04-02):** Material definitions and model metadata flow between federation nodes via .axiompack share/receive (implemented). FederationPackSource (priority 75) loads materials from received packs. EC safety guard blocks export-controlled content on receive. Push-based real-time fact propagation (WebSocket events) and auto-discovery from federation peers are not yet built. Material authority chain works locally (CoreForge priority 200 > user YAML 50 > federation 75 > builtin 0); real-time federation sync of materials is planned.

Facts cross federation boundaries; raw data never does. The community corpus federation operates on extracted knowledge propositions, not source documents or raw chunks.

#### What Flows Between Nodes

| Content type | Crosses federation boundary? | Notes |
|---|---|---|
| **Facts** (extracted propositions) | Yes | Core federation unit; includes confidence, provenance, maturity level |
| **Raw chunks** | Never | Source text stays at originating node |
| **Material definitions** | Yes | Shared via facility packs or explicit push |
| **Model metadata** | Yes | Discovery events propagate; full manifests pulled on demand |
| **Input decks** | Pull only | Requesting node must have appropriate access tier |
| **Operating parameters** | Depends | Public parameters flow; facility-specific require trust level |
| **CoreForge configs** | Org-only | Never cross organizational boundaries |

#### Trust Gradient

Incoming federation facts are classified by a trust gradient before integration:

| Grade | Criteria | Resolution |
|---|---|---|
| **GREEN** | Confidence >= 0.85, corroborated by >= 2 sites | Auto-promote to community corpus |
| **YELLOW** | Confidence >= 0.60 but below GREEN threshold, or single-site | EVE resolves: cross-references against existing corpus, flags contradictions |
| **RED** | Confidence < 0.60, contradicts existing facts, or from untrusted source | Human review required via `axi rag review` |

#### Multi-Site Corroboration

When the same fact is independently extracted at multiple federation sites, its knowledge maturity level increases. A fact corroborated by N >= 2 independent sites is promoted one maturity level (up to the maximum for its content type). This is the primary mechanism by which federation improves corpus quality.

#### Event-Driven Propagation

Fact extraction triggers a federation push — not polling. When EVE extracts a new fact at any node, the node pushes a lightweight fact proposition (claim, confidence, domain tags, provenance hash) to all trusted peers. Peers evaluate the incoming fact against their local trust gradient and either auto-promote, queue for EVE resolution, or flag for human review.

### Relationship to INL Federated Learning LDRD

The INL multi-site LDRD trains ML models across UT-Austin TRIGA, OSU TRIGA, and INL NRAD reactors using Flower AI. NeutronOS community corpus federation is the knowledge-layer complement. See upstream spec section 11 for the full comparison table.
