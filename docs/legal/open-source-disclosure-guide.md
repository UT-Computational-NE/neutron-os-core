# Open Source Disclosure Guide

> **Status:** Pre-Disclosure  
> **Last Updated:** 2026-03-25  
> **Contact:** Discovery to Impact — businessdevelopment@discoveries.utexas.edu

---

## Overview

This document guides the process of disclosing and releasing two related software projects as MIT open source through UT Austin's Discovery to Impact office.

| Project | Description | Lines of Code | Target Repo |
|---------|-------------|---------------|-------------|
| **axiom** | Generic LLM/data platform framework | ~25,000 | github.com/benboooth/axiom |
| **neutron-os** | Nuclear facility application layer | ~500 nuclear-specific | github.com/UT-Computational-NE/neutron-os |

---

## Key Contacts

| Contact | Purpose | Details |
|---------|---------|---------|
| **Discovery to Impact** | IP disclosure & licensing | businessdevelopment@discoveries.utexas.edu |
| **Disclosure Portal** | Submit disclosures | [Tradespace Portal](https://app.tradespace.io/signin/inventor?account_slug=d74c2a7194a7b03da184) |
| **Traditional Forms** | Software Copyright form | [Box folder](https://utexas.box.com/v/DiscoverytoImpactDisclosures) |
| **Main Website** | General info | [discoverytoimpact.utexas.edu](https://discoverytoimpact.utexas.edu/researchers/disclose-your-technology/) |

---

## Process Timeline

```
PHASE 1: Preparation ← YOU ARE HERE
├── ✅ Code analysis (98% generic, 2% nuclear-specific)
├── ✅ Disclosure narratives drafted
├── ✅ Supporting documentation prepared
├── ⬜ Split codebase into axiom + neutron-os repos
├── ⬜ Verify line counts and file inventory post-split
├── ⬜ Send intro email to Discovery to Impact
└── ⬜ Schedule consultation meeting

PHASE 2: Disclosure
├── ⬜ Submit axiom Software Copyright Disclosure
├── ⬜ Submit neutron-os Software Copyright Disclosure
├── ⬜ Attend meeting to discuss both
└── ⬜ Respond to any follow-up questions

PHASE 3: Approval
├── ⬜ Receive approval for MIT release
├── ⬜ Get official LICENSE text from Discovery to Impact
└── ⬜ Confirm copyright holder language

PHASE 4: Release
├── ⬜ Create axiom repo with MIT LICENSE
├── ⬜ Transfer neutron-os to UT-Computational-NE org
├── ⬜ Update READMEs with UT acknowledgment
└── ⬜ Announce releases
```

---

## Legal Framework

### UT System Rule 90101: Intellectual Property

**Key sections:**

- **§2 Ownership:** "The Board of Regents automatically owns the intellectual property created by individuals subject to this Rule"

- **§4 IP Subject to Rule:** IP developed (a) within scope of employment, (b) on UT time, or (c) using UT facilities is owned by Board of Regents

- **§11.1 Disclosure Required:** "Before intellectual property owned by the Board of Regents is disclosed to any party outside the U.T. System...the creator shall submit a reasonably complete and detailed invention disclosure"

- **§11.2 Release Option:** "If the institution's president elects not to assert the Board of Regents' ownership interest...the creator will be free to obtain and exploit a patent or other intellectual property protection in his or her own right"

- **§1.1 Public Benefit:** "allows for knowledge and technology to be disseminated to benefit the broad public"

**Source:** [Rule 90101](https://www.utsystem.edu/board-of-regents/rules/90101-intellectual-property)

### Discovery to Impact Scope

From their website:
> "This team also oversees patent filing, prosecution, and maintenance as well as **outbound software and copyright licenses, including releasing software under open-source licenses.**"

---

## Disclosure Documents

### Document 1: Intro Email (Send First)

```
Subject: Open Source Software Disclosure Consultation — Two Related Projects

Dear Discovery to Impact Team,

I'm a researcher in UT's Computational Nuclear Engineering group, and I'd 
like to discuss the open source release process for two related software 
projects I've developed:

1. **axiom** — A generic LLM/data platform framework (~25,000 lines)
2. **NeutronOS** — A nuclear facility application layer built on axiom 
   (~500 lines nuclear-specific)

Both were developed using UT resources and should be disclosed. I'm 
requesting MIT open source release for both, as:

- Neither has commercial licensing potential (generic infrastructure + 
  niche academic users)
- Open source enables adoption by other university research reactors
- MIT release aligns with DOE-NE mission and positions UT for future 
  NEUP funding

Before filing formal disclosures, I'd appreciate a brief consultation to 
ensure I'm following the correct process for open source software. I 
understand your team handles "outbound software and copyright licenses, 
including releasing software under open-source licenses."

Would someone be available for a 30-minute call this week or next?

Best regards,
Benjamin Booth
UT Computational Nuclear Engineering
[phone]
[email]
```

---

### Document 2: axiom Disclosure Narrative

**For Software Copyright Disclosure form:**

---

**Title:** axiom — Generic LLM/Data Platform Framework

**Description:**

axiom is a domain-agnostic software framework for building LLM-powered applications. It provides:

- LLM gateway with multi-provider routing and fallback
- RAG (Retrieval Augmented Generation) with pgvector
- CLI framework with extension discovery
- State management with atomic writes and PostgreSQL backend
- Audit logging with HMAC tamper detection
- Human-in-the-loop approval workflows (RACI framework)
- Document publishing pipeline
- Interactive review system

The framework contains no domain-specific knowledge and is designed to be extended for any industry vertical (nuclear, medical, legal, finance, etc.).

**Technical Components:**
- `infra/` — LLM gateway, state management, providers, logging, security
- `rag/` — Embeddings, vector store, chunking, ingestion
- `review/` — Interactive review framework
- `cli/` — Extension-based CLI dispatcher
- `extensions/` — Chat agent, signal extraction, publisher, settings, database, etc.

**Lines of Code:** ~25,000

**Creators:** Benjamin Booth (primary developer)

**Date of Creation:** 2025-2026

**UT Resources Used:**
- Development time as part of research activities
- TACC GitLab hosting (rsicc-gitlab.tacc.utexas.edu)
- TACC vLLM endpoints for development testing
- General computing resources

**Funding Sources:** 
None. Development predates pending NEUP proposals. No federal or sponsored research funds were used.

**Related Disclosures:** 
neutron-os (nuclear application layer) depends on axiom and is being disclosed simultaneously.

**Requested Disposition:** 
Release under MIT open source license

**Justification for MIT Open Source Release:**

1. **No commercial value standalone** — Generic LLM infrastructure competes with established open source projects (LangChain, LlamaIndex, Haystack). No company would pay licensing fees for this when free alternatives exist.

2. **Enables neutron-os adoption** — MIT-licensed axiom is required for neutron-os to be deployable at other institutions. Proprietary axiom would block nuclear community adoption.

3. **Community standard** — MIT license is expected for infrastructure libraries. Proprietary licensing would result in zero adoption.

4. **Attracts contributors** — Open source enables external contributions from the developer community, reducing UT's maintenance burden.

5. **Reputation value** — Positions UT as contributor to the open source AI/LLM ecosystem.

6. **No competing commercial alternative** — UT is not forgoing licensing revenue; this category of software is universally open source.

---

### Document 3: neutron-os Disclosure Narrative

**For Software Copyright Disclosure form:**

---

**Title:** NeutronOS — Nuclear Facility Digital Operations Platform

**Description:**

NeutronOS configures the axiom framework for nuclear facility operations. It is a thin application layer that adds nuclear-specific functionality to the generic axiom platform.

Nuclear-specific components include:
- Export control keyword classification lists (MCNP, SCALE, HEU, 10 CFR 810, etc.)
- Nuclear sensitivity detection prompts for LLM routing
- Research reactor configuration defaults (TRIGA Mark II)
- (Planned) Digital twin hosting, Model Corral physics registry, ROM execution

The nuclear-specific code comprises approximately 100-500 lines. The remaining functionality is provided by the axiom dependency.

**Technical Components:**
- `nuclear/export_control_terms.txt` — Keyword lists for query classification
- `nuclear/router_prompt.toml` — Nuclear classifier prompt
- `nuclear/facility_defaults.toml` — TRIGA configuration defaults
- Integration code to wire nuclear config into axiom

**Lines of Code:** 
~100-500 lines nuclear-specific; depends on axiom (~25,000 lines)

**Creators:** 
Benjamin Booth (primary developer), with guidance from Dr. Kevin Clarno

**Date of Creation:** 2025-2026

**UT Resources Used:**
- Development time as part of research activities
- TACC GitLab hosting (rsicc-gitlab.tacc.utexas.edu)
- TACC vLLM endpoints for development testing
- Domain expertise from UT NETL (Nuclear Engineering Teaching Laboratory) operations
- General computing resources

**Funding Sources:** 
None. Development predates pending NEUP proposals. No federal or sponsored research funds were used.

**Related Disclosures:** 
Depends on axiom (generic platform layer), which is being disclosed simultaneously.

**Requested Disposition:** 
Release under MIT open source license

**Justification for MIT Open Source Release:**

1. **Target users are non-commercial** — The market is approximately 30 US university research reactors. These are educational facilities that will not pay software licensing fees.

2. **DOE-NE mission alignment** — Supports DOE Office of Nuclear Energy goals for advanced reactor operations and digital capabilities. Open source aligns with DOE's preference for broadly accessible research tools.

3. **Enables future NEUP funding** — Open source NeutronOS positions UT to lead multi-institution NEUP proposals. Proprietary licensing would exclude partner institutions (INL, OSU, Penn State).

4. **Community adoption model** — Other university reactors would contribute improvements, bug fixes, and extensions. This distributed development model is only possible with open source.

5. **No viable licensing revenue** — Universities operate on tight budgets and have procurement barriers. The realistic licensing revenue is $0; value is in adoption and reputation.

6. **Safety benefit** — Improved nuclear facility operations software benefits public safety. Open source enables peer review and broad deployment.

7. **Standards setting** — Positions UT as leader in nuclear digital twin and facility operations space.

---

## Supporting Documentation

### Code Analysis Summary

| Category | Lines | Percentage | Examples |
|----------|-------|------------|----------|
| **Generic (axiom)** | ~25,000 | 98% | LLM gateway, RAG, CLI, state management, audit logging |
| **Nuclear (neutron-os)** | ~100-500 | 2% | Export control terms, classifier prompts, TRIGA defaults |

**Nuclear-specific files identified:**
- `src/neutron_os/infra/_export_control_terms_default.txt` — Keyword list (~50 lines)
- `src/neutron_os/infra/router.py` lines 52-62 — Classifier prompt (~10 lines)
- `src/neutron_os/setup/wizard.py` line 517 — Default facility name (~1 line)

### Funding Status

| Source | Status | Notes |
|--------|--------|-------|
| **NEUP 2026** | Pending proposals | Multiple submissions, not yet awarded |
| **CINR** | Pre-application submitted | Awaiting response |
| **DOE-NE IRP** | Concept stage | With INL, deadline June 2026 |
| **Federal grants** | None | No current awards |
| **Industry sponsors** | None | No sponsored research |

**Conclusion:** All development predates any external funding. No Bayh-Dole or sponsor IP obligations exist.

### DOE-NE Mission Alignment

From NEUP proposal materials in `docs/proposals/`:

> NeutronOS supports DOE-NE strategic objectives for:
> - Advanced reactor operations and monitoring
> - Digital twin capabilities for research reactors
> - Workforce development through modern tooling
> - Multi-facility data sharing and collaboration

Open source release directly enables these objectives by allowing deployment at DOE national labs and university research reactors.

---

## Post-Approval Actions

### LICENSE File Template

```
MIT License

Copyright (c) 2026 The Board of Regents of The University of Texas System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**Note:** Confirm exact copyright holder language with Discovery to Impact. May be:
- "The Board of Regents of The University of Texas System"
- "The University of Texas at Austin"
- Other formulation per their standard

### README Acknowledgment Template

```markdown
## Acknowledgments

This software was developed at The University of Texas at Austin, 
Department of Mechanical Engineering, Nuclear and Radiation Engineering Program.

Released as open source under the MIT License with approval from 
UT Austin Discovery to Impact.
```

### Repository Setup Checklist

**For axiom (github.com/benboooth/axiom):**
- [ ] Create repository
- [ ] Add MIT LICENSE (UT copyright)
- [ ] Add README with acknowledgment
- [ ] Add CONTRIBUTING.md
- [ ] Configure branch protection
- [ ] Create initial release tag

**For neutron-os (github.com/UT-Computational-NE/neutron-os):**
- [ ] Transfer from current location
- [ ] Update LICENSE to MIT (UT copyright)
- [ ] Update README with acknowledgment
- [ ] Update pyproject.toml to depend on axiom
- [ ] Configure branch protection
- [ ] Create initial release tag

---

## Talking Points for Discovery to Impact Meeting

1. **"This is two separate but related things"**
   - axiom is generic infrastructure (like Django, Flask)
   - neutron-os is the nuclear application (like a Django app)
   - Both need to be MIT for either to be useful

2. **"No revenue path exists"**
   - Generic: Competes with free alternatives (LangChain)
   - Nuclear: ~30 university reactors won't pay licensing fees

3. **"Open source enables future funding"**
   - NEUP proposals require multi-institution collaboration
   - Proprietary would exclude INL, OSU, Penn State partners
   - MIT release is prerequisite for competitive proposals

4. **"Minimal maintenance burden"**
   - Community contributions reduce UT's ongoing costs
   - Bug reports from other institutions improve quality

5. **"DOE mission alignment"**
   - Cite DOE-NE strategic goals
   - Show CINR/NEUP proposal alignment

6. **"This is standard practice"**
   - Reference other UT open source releases
   - MIT is most common license for infrastructure software

---

## Risk Mitigation

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| **Slow approval process** | Medium | Send intro email early; be responsive to questions |
| **UT wants different license** | Low | Apache 2.0 is acceptable fallback (still open source) |
| **UT asserts commercial interest** | Low | Prepare market analysis showing no revenue potential |
| **Separate approval timelines** | Medium | axiom may approve faster; be prepared for staged release |
| **Questions about funding** | Medium | Document that all development predates any proposals |

---

## Reference Links

- [UT System Rule 90101](https://www.utsystem.edu/board-of-regents/rules/90101-intellectual-property)
- [Discovery to Impact - Disclose Your Technology](https://discoverytoimpact.utexas.edu/researchers/disclose-your-technology/)
- [Tradespace Disclosure Portal](https://app.tradespace.io/signin/inventor?account_slug=d74c2a7194a7b03da184)
- [Traditional Disclosure Forms (Box)](https://utexas.box.com/v/DiscoverytoImpactDisclosures)

---

## Document History

| Date | Change |
|------|--------|
| 2026-03-25 | Initial creation |
