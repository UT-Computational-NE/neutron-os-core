# Commercialization Roadmap

> **Last Updated:** February 2026  
> **Status:** Early exploration – Strategic vision requires stakeholder validation

---

## Neutron OS Vision (DRAFT – NOT YET VALIDATED)

> ⚠️ **INTERNAL DRAFT:** This section captures a potential commercialization vision that has **not yet been reviewed** by Dr. Kevin Clarno, department leadership, or peers. It requires formal stakeholder alignment before driving major decisions.

### The Big Picture

The TRIGA Digital Twin is the **first implementation** of **Neutron OS**—a configurable, licensable platform that provides end-to-end digital infrastructure for reactor operations, compliance, research, and training.

**NROS = The "iOS for nuclear reactors"**
- Modular, reactor-agnostic core
- Plugin architecture for reactor-specific physics
- Persona-driven UI (operators, researchers, managers, students)
- AI copilot for operations, research, and learning
- Compliance automation framework
- Commercially licensable by UT

### Strategic Evolution

| Phase | Focus | Revenue Model |
|-------|-------|---------------|
| **Now** | TRIGA DT at NETL | None (research) |
| **Near-term** | Validate with 2nd reactor (MSR initiative?) | Grant funding |
| **Medium-term** | Package as licensable platform | License + consulting |
| **Long-term** | Neutron OS deployed at Natura MSR + other facilities | License fees + support contracts |

### Natura Resources Opportunity

| Dimension | Details |
|-----------|---------|
| **Relationship** | UT collaboration on MSR initiative |
| **Their Need** | Operations platform for commercial MSR |
| **Our Offer** | License Neutron OS + UT faculty consulting |
| **Revenue** | License fee + per-facility consulting |
| **Timeline** | Aligned with Natura's reactor deployment schedule (TBD) |

### Stakeholder Validation Required

| # | Assumption | Validation Method | Owner | Status |
|---|------------|-------------------|-------|--------|
| S1 | Dr. Clarno supports commercialization path | Meeting with dept head | Ben | ❓ Not started |
| S2 | UT Office of Technology Commercialization interested | OTC meeting | Ben | ❓ Not started |
| S3 | Natura Resources interested in licensing vs. build-your-own | Natura discussion | Ben | ❓ Not started |
| S4 | Faculty/researchers willing to consult on installations | Informal faculty conversations | Ben | ❓ Not started |
| S5 | No conflict with existing DOE/NRC IP agreements | Legal review | OTC | ❓ Not started |
| S6 | Peer researchers see value in generalizable platform | Peer review of vision doc | Ben | ❓ Not started |

**Decision Point:** If validation fails, continue as research tool without commercialization overhead.

---

## Market Opportunity

### Research Reactor Landscape
- ~30 operating research reactors in the United States
- ~220 research reactors worldwide
- Many face similar challenges: aging documentation systems, compliance burden, limited digital infrastructure

### Medical Isotope Production Opportunity
**This may be the highest-impact commercialization path.**

Current state of isotope supply chain:
- Houston cancer clinics call Dr. Charlton (NETL Director) directly to request isotopes
- Manual coordination: professor assigns student, student runs simulations, writes Word doc
- Results delivered by phone to operators the next morning
- No SLAs, no tracking, entirely relationship-dependent

**Why this matters:**
- Research reactors *could* produce medical isotopes but coordination overhead makes it impractical
- Major US isotope supply comes from aging Canadian reactor (NRU - shut down) and limited domestic capacity
- Digital twin automation could turn any equipped research reactor into reliable isotope producer
- Real revenue from hospital contracts, not just academic funding

**Market size indicators:**
- US medical isotope market: ~$4B annually
- Mo-99 (used in ~40M diagnostic procedures/year) chronically supply-constrained
- Research reactors with isotope capability: 10-15 in US currently underutilized

### Pain Points by Segment

| Segment | Pain Point | Willingness to Pay For |
|---------|------------|------------------------|
| **Operators** | Defensible records that protect them personally | Automated audit trails, tamper-proof logs |
| **Researchers** | Credible benchmarks that get papers published | Curated, citable validation datasets |
| **Students** | Confidence before high-stakes responsibility | Safe practice environments with realistic feedback |
| **Facility Mgmt** | Regulatory survival | Compliance automation, inspection-ready reports |
| **Code Developers** | Licensability of their software | V&V data packages with uncertainty quantification |

---

## Value Proposition Candidates

### For Research Reactors
> "Automated compliance documentation that survives NRC scrutiny"

**Value drivers:**
- Reduce inspection prep time by 50%+
- Eliminate documentation gaps
- Tamper-evident audit trails
- On-demand report generation

### For Simulation Code Vendors
> "Real-world validation datasets that accelerate NQA-1 qualification"

**Value drivers:**
- Measured vs predicted data with documented conditions
- Uncertainty quantification included
- Citable, reproducible datasets
- Covers operational transients (not just steady-state)

### For Nuclear Engineering Programs
> "A flight simulator for reactor operators - build intuition without risk"

**Value drivers:**
- Safe practice environment
- Real reactor data as examples
- Interactive physics visualization
- Curriculum-ready materials

### For Facility Directors
> "Turn your reactor into a data product - monetize operations that currently just cost money"

**Value drivers:**
- New revenue stream from existing operations
- Enhanced research reputation
- Attract collaborators and funding
- Student recruitment differentiator

### For Medical Isotope Customers (NEW - HIGH PRIORITY)
> "Reliable isotope production without the phone tag - order to delivery tracking"

**Value drivers:**
- Predictable ordering workflow (no more calling the department head)
- Real-time production status tracking
- SLA-backed delivery commitments
- Expanded domestic isotope supply

### For Isotope-Capable Reactors
> "Unlock isotope revenue without hiring a logistics coordinator"

**Value drivers:**
- Automated operations package generation from orders
- Integration with hospital ordering systems
- Compliance documentation auto-generated
- Turn occasional capability into reliable service

---

## Business Model Options

### Model A: SaaS Platform
**Approach:** Hosted digital twin service for research reactors

| Pros | Cons |
|------|------|
| Recurring revenue | High infrastructure cost |
| Centralized updates | Data sovereignty concerns |
| Network effects | Requires sales/support |

**Pricing concept:** $X,000/month based on reactor size + data volume

### Model B: Licensed Software
**Approach:** On-premise deployment with support contract

| Pros | Cons |
|------|------|
| One-time revenue + maintenance | Lower recurring revenue |
| Customer controls data | Deployment complexity |
| Fits government procurement | Version fragmentation |

**Pricing concept:** $XX,000 license + $X,000/year support

### Model C: Data Products
**Approach:** Sell curated validation datasets

| Pros | Cons |
|------|------|
| Low marginal cost | Limited market size |
| High perceived value for V&V | One-time purchase |
| No ongoing support burden | Requires data curation |

**Pricing concept:** $X,000-XX,000 per dataset depending on scope

### Model D: Consulting + Implementation
**Approach:** Custom digital twin deployments for facilities

| Pros | Cons |
|------|------|
| High per-engagement revenue | Doesn't scale |
| Deep customer relationships | Labor intensive |
| Learn from each deployment | Key person risk |

**Pricing concept:** $XXX,000 per implementation

### Model F: NROS Platform License (NEW – STRATEGIC)
**Approach:** License configurable reactor operating system to commercial operators

| Pros | Cons |
|------|------|
| High-value B2B contracts | Requires product maturity |
| Recurring license + support revenue | Long sales cycles |
| Faculty consulting creates upsell | IP/legal complexity |
| Strategic positioning for UT | Requires OTC alignment |
| Scales across reactor types | Multi-year development |

**Pricing concept:**
- Base platform license: $XXX,000 - $X,000,000 (depends on reactor scale)
- Annual support/updates: 15-20% of license fee
- Implementation consulting: $XXX/hour (faculty rates)
- Custom module development: Project-based

**Target Customers:**
- Natura Resources (MSR)
- Other advanced reactor vendors (SMR, microreactors)
- International research reactors seeking modernization
- National labs with operational reactors

**Why this could be big:**
1. **First-mover:** No comparable "reactor OS" exists
2. **Trust:** UT/DOE pedigree vs. unknown startup
3. **Consulting moat:** Faculty expertise bundled with software
4. **Policy tailwind:** DOE pushing domestic nuclear, advanced reactors need infrastructure

### Model E: Isotope Production Coordination (NEW - HIGH PRIORITY)
**Approach:** Transaction fee or subscription for isotope order automation

| Pros | Cons |
|------|------|
| **Real recurring revenue** | Regulatory complexity |
| Solves tangible supply chain problem | Multi-party coordination required |
| Network effects across reactors | Hospital procurement cycles slow |
| Saves lives (cancer diagnostics) | Quality/liability stakes high |

**Pricing concept options:**
- Per-order transaction fee: $X00-X,000 per production run
- Hospital subscription: $XX,000/year for priority access
- Reactor subscription: $X,000/month for coordination platform

**Why this model could work:**
1. **Immediate pain point:** Hospitals already calling professors; they'd pay to not do that
2. **Underutilized capacity:** Research reactors running anyway for training/research
3. **Supply constraint:** Mo-99 shortages are ongoing; domestic production is strategic priority
4. **DOE interest:** Domestic isotope production is explicit policy goal (see ARPA-E MEITNER program)

---

## Competitive Landscape

| Competitor Type | Examples | Our Differentiation |
|-----------------|----------|---------------------|
| SCADA vendors | Wonderware, Ignition | Purpose-built for reactor physics, not generic |
| Physics simulation | VERA, Serpent | Integrated data pipeline, not standalone code |
| Compliance software | Generic nuclear QA tools | Research reactor specific, physics-informed |
| DIY solutions | Facility-specific scripts | Production-ready, documented, supported |

---

## Go-to-Market Questions

### Validation Questions
- How much do facilities currently spend on manual documentation and inspection prep?
- What's the cost of a failed NRC inspection? (fines, downtime, reputational)
- How many simulation codes are blocked from licensing due to insufficient V&V data?
- Would universities pay for a shared "reactor data commons" with standardized formats?

### Isotope-Specific Validation Questions (HIGH PRIORITY)
- How many isotope requests does NETL receive monthly? Annually?
- What's the average time from hospital request to isotope delivery today?
- How much does Dr. Charlton spend coordinating isotope orders? (opportunity cost)
- Which Houston hospitals/clinics are regular isotope customers?
- What isotopes does NETL produce? (Mo-99? I-131? Others?)
- Are there requests NETL turns down due to coordination burden?
- What would hospitals pay for guaranteed 24-hour turnaround?

### Customer Discovery Priorities
1. Interview 3+ facility managers about compliance pain (start with Dr. Charlton at NETL)
2. Talk to 2+ MPACT/VERA users about V&V data needs (Dr. Clarno connection to CASL/VERA)
3. Survey NE program instructors on educational tool interest (M E 390G, 361E, 336P at UT)
4. Explore DOE SBIR/STTR funding opportunities
5. **Shadow Dr. Charlton on 2-3 isotope request calls** (understand full workflow)
6. **Interview Houston hospital contacts** (understand buyer pain and willingness to pay)
7. **Research which research reactors have isotope production capability** (expansion potential)

---

## Pilot Strategy

### Ideal Pilot Characteristics
- TRIGA reactor (similar instrumentation)
- University setting (less procurement friction)
- Active research program (data generation)
- Engaged facility management (change appetite)
- Geographic proximity (easier collaboration)

### Pilot Candidates to Explore
- [ ] UT Austin NETL (current - continue as reference)
- [ ] Texas A&M NSC
- [ ] Penn State Breazeale
- [ ] UC Davis McClellan
- [ ] Oregon State OSTR

### Pilot Success Criteria
1. Full pipeline operational within 40 hours
2. 90%+ data completeness within 30 days
3. Positive feedback from operators
4. Interest in continued engagement

---

## IP Considerations

### Protectable Elements
- Shadowcaster orchestration framework
- Change point detection algorithms
- Bias correction methodology
- Web interface and visualizations
- **NROS core platform architecture**
- **Reactor-agnostic compliance framework**
| **AI copilot models/prompts** (operations, research, learning)

### NROS IP Strategy (Draft)

| Component | Recommended Approach | Rationale |
|-----------|---------------------|-----------|
| Core platform | UT-owned, proprietary license | Revenue generator |
| Reactor plugins | Open standard, proprietary implementations | Ecosystem + lock-in |
| Data formats | Open standard (Apache 2.0) | Adoption, interoperability |
| UI framework | UT-owned, white-label capable | Branding flexibility |
| AI copilot (ops) | UT-owned, API access only | Protect training investment |
| AI copilot (research) | UT-owned, API access only | High-value differentiator |
| Compliance rules | Configurable, customer-owned | Flexibility, reduce liability |

### Open Questions
- University IP policy for student/staff work
- DOE funding implications on IP
- Open source vs proprietary strategy
- **OTC preferred licensing model** (exclusive, non-exclusive, field-of-use)
- **How to handle faculty consulting revenue** (through UT or personal)
- **Spin-out vs. university licensing** for commercial deployment
- **Natura-specific IP arrangements** if they fund development

---

## Funding Pathways

| Source | Fit | Timeline | Notes |
|--------|-----|----------|-------|
| DOE SBIR/STTR | High | 6-12 months | Nuclear innovation focus |
| NSF I-Corps | High | 2-3 months | Customer discovery funding |
| University venture fund | Medium | 3-6 months | Early stage |
| Industry partnership | Medium | 6-12 months | Needs champion |
| ARPA-E OPEN | Low | 12+ months | Not breakthrough enough |
| **Natura Resources co-development** | **High** | **TBD** | Aligned interests, potential anchor customer |
| **DOE NEUP** | **High** | **6-12 months** | University reactor infrastructure |
| **NRC research grants** | **Medium** | **12+ months** | Compliance/safety focus |

---

## Next Steps

### Near-term (Q1)
1. Document infrastructure costs for pricing models
2. Complete architecture documentation for replicability assessment
3. Identify and contact 2-3 potential pilot facilities
4. Explore NSF I-Corps application
5. **Document current isotope production workflow end-to-end**
6. **Identify Houston hospital contacts for isotope customer discovery**

### Medium-term (Q2-Q3)
1. Conduct formal customer discovery interviews
2. Develop pilot deployment playbook
3. Evaluate DOE SBIR topics
4. Clarify IP ownership with university
5. **Prototype isotope request portal** (even just Google Form + auto-generated ops package)
6. **Interview 3+ isotope customers about pain points**
7. **Research ARPA-E MEITNER and other isotope-focused funding**

### Long-term (Q4+)
1. Execute first external pilot
2. Validate business model assumptions
3. Determine go/no-go on commercial pursuit
4. **Expand isotope coordination to 2nd reactor facility**
5. **Evaluate spin-out vs university licensing for isotope platform**
6. **Present NROS vision to Dr. Clarno and department leadership**
7. **Initiate OTC conversation about commercialization path**
8. **Explore Natura Resources partnership/licensing discussion**

---

## Related Documents

- [Data Platform Roadmap](../specs/data_platform_roadmap.md) – Technical architecture and phased implementation
- [User Personas](02_user_personas.md) – Target users and their motivations
- [OKRs & Goals](04_okrs_goals.md) – Success metrics driving development
- [Metrics Framework](03_metrics_framework.md) – How we measure progress
