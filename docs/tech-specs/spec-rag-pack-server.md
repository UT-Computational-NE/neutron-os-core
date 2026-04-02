# RAG Pack Server & Generation Pipeline — Neutron OS Nuclear Extensions

> The core specification is provided by the Axiom platform. This document defines nuclear-domain extensions only.

**Upstream:** [Axiom RAG Pack Server Spec](https://github.com/…/axiom/docs/tech-specs/spec-rag-pack-server.md)

---

## Nuclear Extensions

### Deployment Profiles

NeutronOS instantiates the three Axiom deployment profiles with nuclear-specific infrastructure:

| Axiom Profile | NeutronOS Instance | Infrastructure |
|--------------|-------------------|---------------|
| Private-Server (restricted) | **Rascal** | UT Austin physical server, VPN-gated, k3d cluster |
| PrivateCloud (export-controlled) | **TACC** | Texas Advanced Computing Center HPC allocation, EAR/10 CFR 810 controls |
| Community CDN (future) | Same | S3/R2, public domain packs from `community_facts` |

### Pack Format

> **Implementation Status (2026-04-02):** `.axiompack` format is implemented for model/material sharing between federation nodes (share/receive CLI). `.facilitypack` archive format with SHA256SUMS is implemented for facility pack distribution (3 builtin packs: NETL-TRIGA, MSRE, PWR-generic). The `.neutpack` RAG-specific pack format is not yet built.

NeutronOS uses `.neutpack` as the pack file extension for RAG corpus packs (vs. Axiom's `.axiompack` for model/material sharing). Facility packs use `.facilitypack`.

### First Pack

The first generated packs are the 3 builtin facility packs: `NETL-TRIGA`, `MSRE`, and `PWR-generic` (each with materials and parameters). The RAG corpus pack `netl-triga` (facility procedures, safety analysis, operational history) is planned.

### Helm Values Files

- `values-rascal.yaml` — Rascal k3d SeaweedFS configuration (bucket: `neut-packs`)
- `values-tacc.yaml` — TACC allocation SeaweedFS (200Gi persistence for EC corpora)
