# AWS Cost Estimation — Simplified Approach

**To:** Cole, Nick, Max, Jay, Dr. Clarno  
**From:** Ben  
**Date:** February 13, 2026  
**Deadline:** February 27, 2026 (see timeline below)  
**Subject:** Help us estimate NeutronOS Phase 1 infrastructure costs (simplified 6-question approach)

---

## The Ask (TL;DR)

We're estimating AWS infrastructure costs for NeutronOS Phase 1 (2026–2027). Instead of asking 50+ detailed questions, we're focusing on **6 critical questions that drive 80% of the cost**. Everything else, we'll estimate intelligently.

Your personalized form takes **3–6 minutes** to complete. **Two-week timeline** (Feb 13–27) gives us quality response time. Some of you have **earlier deadlines** (Feb 16) because your answers unlock downstream decisions.

---

## Why This Matters

**Timeline:** TRIGA 2026–2027 operating budget finalization  
**Decision needed by:** Feb 27 for Dr. Clarno's approval  
**Budget impact:** ~$1,134/month baseline (varies 2x–3x depending on your answers)

---

## Your Personalized Form & Deadline

| Person | Form | Deadline | Why Earlier? |
|--------|------|----------|---|
| **Max** | [FORM-Max-PiXie.md](FORM-Max-PiXie.md) | **Wed, Feb 16, 5 PM** ⚠️ | PiXie yes/no blocks entire architecture |
| **Jay** | [FORM-Jay-ML.md](FORM-Jay-ML.md) | **Wed, Feb 16, 5 PM** ⚠️ | Claude API usage + training data determine external service budget |
| **Dr. Clarno** | [FORM-Clarno-Compliance.md](FORM-Clarno-Compliance.md) | **Fri, Feb 20, 5 PM** ⚠️ | ITAR + retention rules affect architecture + cost 30–50% |
| **Cole** | [FORM-Cole-Physics.md](FORM-Cole-Physics.md) | **Fri, Feb 20, 5 PM** | Egress + archive volume affect storage + network |
| **Nick** | [FORM-Nick-Operations.md](FORM-Nick-Operations.md) | **Fri, Feb 20, 5 PM** | Operating hours + data volume affect compute + storage |

**For others building systems:** If you're not listed above but are building something that generates/collects data (new sensor integration, validation framework, automation tool, etc.), use the generic form:
- [FORM-Generic-DataBuilder.md](FORM-Generic-DataBuilder.md) | **Fri, Feb 20, 5 PM** | Flexible questions for any data-generating system

---

## The Six Critical Questions

| # | Question | Asker | Impact | Cost Range |
|---|----------|-------|--------|---|
| 1 | Data egress monthly? | Cole, Nick | Network costs 10x variation | $0–500/mo |
| 2 | PiXie Phase 1 yes/no? | Max | Hardware scope decision | $0 or +$200/mo |
| 3 | Operating hours/week? | Nick | Cluster uptime | $170–1,450/mo |
| 4 | Data retention policy? | Dr. Clarno | Storage tiers | $30–210/mo |
| 5 | Claude API calls/day? | Jay | External services | $24–400+/mo |
| 6 | ITAR (GovCloud)? | Dr. Clarno | Region + compliance | +30% cost if yes |

Everything else, we estimate intelligently.

---

## Why Simplified?

**Old approach:** 50+ detailed questions, 3-week timeline, low response rate  
**New approach:** 6 critical questions + intelligent estimates, 2-week timeline, high-value responses

**Key principle:** Don't ask what we can estimate. Ask only what changes the answer.

---

## How It Works

1. **You fill your form** (3–6 minutes)
2. **We load responses** into cost_estimation_tool (Python)
3. **Tool estimates everything else** using baseline assumptions + your answers
4. **Ben generates final deliverables** (Executive Summary, Cost Tables, Justification)
5. **Dr. Clarno approves** for budget submission

---

## Three Cost Scenarios

All costs include 9 AWS services + external services (Redpanda, Claude API):

| Scenario | PiXie | Hours/week | External | Monthly | 2026 (9mo) | Phase 1 Total |
|----------|-------|-----------|----------|---------|-----------|---------------|
| **Minimal** | No | 40 | No RAG | $612 | $5,508 | $12,852 |
| **Recommended** ⭐ | Yes | 40 | Moderate | $1,134 | $10,206 | $23,814 |
| **Full Cloud** | Yes | 168 | Heavy | $2,016 | $18,144 | $42,336 |

**Final recommendation likely: Recommended scenario ($1,134/mo)**, unless your responses shift us toward Minimal or Full Cloud.

---

## Key Dates

| Date | Action | Who | Deadline |
|------|--------|-----|----------|
| **Feb 13** | Send personalized forms | Ben | EOD |
| **Feb 16, 5 PM** | Receive Max + Jay responses ⚠️ | Max, Jay | Hard deadline (blocking gates) |
| **Feb 20, 5 PM** | Receive Cole + Nick + Dr. Clarno ⚠️ | Cole, Nick, Dr. Clarno | Hard deadline |
| **Feb 24** | Load all responses → generate costs | Ben | EOD |
| **Feb 25–26** | Draft final deliverables | Ben | EOD |
| **Feb 27, 5 PM** | Submit to Dr. Clarno | Ben | Final deadline |

---

## Document Organization

**Master index for all cost estimation docs:**
→ [phase1-cost-sizing/](phase1-cost-sizing/) (navigate here for complete overview)

**Simplified approach explained:**
→ [SIMPLIFIED-COST-DRIVERS.md](SIMPLIFIED-COST-DRIVERS.md) (this is the methodology)

**Your personalized forms:**
→ [FORM-Cole-Physics.md](FORM-Cole-Physics.md)  
→ [FORM-Nick-Operations.md](FORM-Nick-Operations.md)  
→ [FORM-Max-PiXie.md](FORM-Max-PiXie.md)  
→ [FORM-Jay-ML.md](FORM-Jay-ML.md)  
→ [FORM-Clarno-Compliance.md](FORM-Clarno-Compliance.md)

**For reference (deep dive, optional):**
→ [aws-cost-estimation-methodology.md](aws-cost-estimation-methodology.md) (complete tool mappings + sourcing)  
→ [aws-comprehensive-utility-usage.md](aws-comprehensive-utility-usage.md) (all 9 services explained)  
→ [COST-ESTIMATION-SOURCES.md](COST-ESTIMATION-SOURCES.md) (where costs come from)

---

## How to Submit Your Response

**Option 1 (Easiest):** Email Ben with your answers filled in  
**Option 2:** Fill out the form directly in the GitHub repo (PR)  
**Option 3:** Schedule a 15-min call to discuss your answers

All are fine—whatever is easiest for you.

---

## FAQ

### Q: I don't know the answer to question X. What should I do?
**A:** Take your best guess. We'll use it as a baseline and refine later. Even "light / moderate / heavy" helps.

### Q: What if my answer changes between now and my deadline?
**A:** Let Ben know ASAP. We have buffer time before final generation (Feb 24).

### Q: Can I see the detailed methodology?
**A:** Yes! See [aws-cost-estimation-methodology.md](aws-cost-estimation-methodology.md). But the short form in your personalized questionnaire is sufficient.

### Q: Will these costs be shared with others?
**A:** Only summary numbers in the final deliverable. Detailed responses stay between you and Ben (or shared with relevant stakeholders if you want).

### Q: What if we're still deciding on PiXie/ITAR/TACC?
**A:** We have assumptions for both outcomes. Your "uncertain" answer tells us we need contingency planning.

---

## Questions or Concerns?

Email Ben or schedule a call. No question is too small—these details matter for accurate budgeting.

---

## Thank You

This cost estimation effort is making NeutronOS Phase 1 funding concrete and defensible. Your 3–6 minute contribution is essential.

**Deadline:** See your personalized form above.  
**Go to:** Your personalized form (links above).

---

## Recognition

Special thanks to:

- **Cole** — for navigating MPACT simulation complexity and archive strategy
- **Nick** — for clarifying TRIGA operating requirements
- **Max** — for the PiXie hardware integration work and timeline clarity
- **Jay** — for pioneering shadowcasting, meeting intake, and RAG systems that drive NeutronOS value
- **Dr. Clarno** — for leadership on Phase 1 scope and compliance clarity

This cost estimate reflects the real infrastructure needed to support your innovations.
