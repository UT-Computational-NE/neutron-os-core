# Agent Platform — Neutron OS

> This capability is provided by the Axiom platform. See the canonical specification below.

**Upstream:** [Axiom Agent Platform](https://github.com/…/axiom/docs/requirements/prd-agents.md)
**Nuclear Extensions:** None — Axiom's domain-agnostic implementation applies directly. Nuclear domain agent capabilities (regulatory intelligence, operational workflow, research support, training) are implemented as facility-specific extensions, not modifications to the core agent platform.

---

## REPL Agent Roster

NeutronOS inherits the Axiom agent roster and applies the **REPL framework** — Read, Eval, Print, Loop — mapping each agent to a role in the interactive intelligence cycle:

| Agent | NeutronOS Name | REPL Role | Description | Status |
|-------|---------------|-----------|-------------|--------|
| **WALL-E** | **Neut (WALL-E)** | **Loop** | Chat agent — orchestrates, routes commands, coordinates agents. Branded as "Neut" in NeutronOS | ✅ Shipped |
| **EVE** | EVE | **Read** | Signal scanner — scans for actionable signals from voice, documents, data streams, Git | ✅ Shipped |
| **CURI-O** | CURI-O | **Eval** | Autonomous research engine — discovers, synthesizes, validates knowledge | 🔲 Spec'd |
| **PR-T** | PR-T | **Print** | Publisher + content gate — document lifecycle, .md to polished .docx. Absorbed Mirror | ✅ Shipped |
| **M-O** | M-O | Infrastructure | Resource steward, system hygiene | ✅ Shipped |
| **D-FIB** | D-FIB | Diagnostics + Security | Platform health, content verification, anomaly detection. Absorbed SECUR-T | ✅ Shipped |
| **BURN-E** | BURN-E | CI/CD | Release/CI agent — build validation, deployment automation | 🔲 Spec'd |
| **SECUR-T** | — | — | Retired — absorbed by D-FIB | Retired |
| **Mirror** | — | — | Retired — absorbed by PR-T + D-FIB | Retired |

### The REPL Model

```
Read(EVE) → Eval(CURI-O) → Print(PR-T) → Loop(WALL-E/Neut)
```

EVE reads signals from the environment. CURI-O evaluates and researches them autonomously. PR-T prints (publishes) results through content gates. Neut (WALL-E) loops — orchestrating the cycle, routing user intent, and iterating. M-O, D-FIB, and BURN-E provide supporting infrastructure, diagnostics, and CI/CD outside the core REPL cycle.

### RACI Note

`raci.neut` in settings maps to WALL-E. All RACI configuration for the chat/orchestrator agent uses this key.
