Table of Contents

Product Requirements Document: Medical Isotope Production

[published] v2.1.3 | February 25, 2026

Module: Medical Isotope Production & Fulfillment

Related Modules: Experiment Manager (shared backend, different workflow)   Parent Document: Neutron OS Executive PRD

Module Type: Optional (configurable on/off per facility mission)

Table of Contents

• Executive Summary

• User Journey Map

• Hospital Customer: Order to Delivery

• Production Manager: Weekly Batch

• Order State Machine

• System Integration

• Current State (to be validated)

• User Stories

• Primary Users

• User Stories: Ordering

• User Stories: Production

• User Stories: Quality & Compliance

• User Stories: Fulfillment & Delivery

• User Stories: Analytics

• Isotope Catalog (Configurable)

• Workflow Stages

• Stage Transitions

• Order Schema

• Production Batch Schema

• QC Record Schema

• UI Mockup Concepts

• Customer Order Portal

• Production Manager Dashboard

• QA/QC Entry Form

• Integration Points

• Shared with Experiment Manager

• Medical Isotope-Specific

• Regulatory Considerations

• NRC Requirements

• FDA Requirements (if applicable)

• DOT Requirements

• Configurability

• Success Metrics

• Open Questions

• Relationship to Experiment Manager

• NEUP Research Addendum

• NEUP Proposal: Medical Isotope Production Optimization

• Optimization Objectives

• New Requirements

• New User Stories

• Digital Twin Integration

Executive Summary

The Medical Isotope Production module manages the end-to-end workflow for producing and delivering medical radioisotopes to healthcare providers. It replaces the current manual process (phone calls, spreadsheets, weekly production schedules) with a digital system that handles ordering, production scheduling, quality assurance, fulfillment, and delivery tracking.

Key Distinction from Experiment Manager:

• Experiment Manager: Researcher-initiated, variable samples,

  research outcomes

• Medical Isotope Production: Customer-initiated orders,

  standardized products, patient care outcomes

Both share technical backend (scheduling, tracking, reactor integration) but serve fundamentally different workflows and stakeholders.

User Journey Map

Hospital Customer: Order to Delivery

!Hospital order-to-delivery workflow

Production Manager: Weekly Batch

!Production manager weekly batch timeline

Order State Machine

System Integration

!System integration diagram showing order → scheduling → production → QA → fulfillment

Current State (to be validated)

Based on typical research reactor medical isotope programs:

• Production cadence: Weekly, typically Mondays

• Ordering process: Phone calls and emails to reactor staff

• Tracking: Spreadsheets, paper records

• Delivery: Courier pickup on production day

• Customers: Hospital nuclear medicine departments, radiopharmacies, research institutions

Pain points (hypothesized):

• No self-service ordering for repeat customers

• Manual coordination between customer requests and production schedule

• Limited visibility into order status

• Paper-based QA/QC records

• Reactive (not proactive) communication about delays

User Stories

Primary Users

User Stories: Ordering

• As a hospital nuclear medicine tech, I want to place a standing

    order for I-131 (same quantity, same day each week) so that I don't     have to call every week.

• As a hospital buyer, I want to see available isotopes and

    current lead times so that I can plan patient treatments.

• As a new customer, I want to request an account and see pricing

    before committing.

• As an existing customer, I want to view my order history and

    reorder with one click.

• As a customer, I want to receive automatic confirmation when my

    order is accepted and updates when it ships.

User Stories: Production

• As a production manager, I want to see all orders for the

    upcoming production cycle so that I can batch similar isotopes     efficiently.

• As a production manager, I want to flag when demand exceeds

    capacity so that I can prioritize or reschedule orders.

• As an operator, I want a production checklist that guides me

    through irradiation steps for each isotope type.

• As a production manager, I want to record actual production

    quantities (may differ from target due to yield variations).

User Stories: Quality & Compliance

• As a QA officer, I want to record quality measurements

    (activity, purity, sterility) against acceptance criteria.

• As a QA officer, I want to generate a Certificate of Analysis

    (COA) for each shipment.

• As a compliance officer, I want immutable records of all

    production and QA activities for FDA/NRC inspection.

• As a QA officer, I want to reject a batch if it doesn't meet

    specifications and notify the customer.

User Stories: Fulfillment & Delivery

• As a shipping coordinator, I want to generate shipping labels

    and DOT-compliant documentation.

• As a courier, I want to know exactly when packages are ready for

    pickup.

• As a customer, I want real-time tracking of my shipment.

• As a customer, I want proof of delivery with timestamp and

    signature.

User Stories: Analytics

• As a facility director, I want to see monthly production volume,

    revenue, and on-time delivery rate.

• As a production manager, I want to see yield trends over time

    (are we getting better or worse at production?).

Isotope Catalog (Configurable)

Example products for a TRIGA facility (actual catalog varies):

Configurable per facility:

• Which isotopes are offered

• Pricing per unit

• Minimum/maximum order quantities

• Lead time requirements

• Available production days

Workflow Stages

!Workflow stages diagram

Stage Transitions

Order Schema

Production Batch Schema

QC Record Schema

UI Mockup Concepts

Customer Order Portal

!Requirements and design diagram

Production Manager Dashboard

!System architecture diagram

QA/QC Entry Form

!Process flow diagram

Integration Points

Shared with Experiment Manager

Medical Isotope-Specific

Regulatory Considerations

NRC Requirements

• 10 CFR Part 30: Specific licenses for byproduct material

• 10 CFR Part 35: Medical use of byproduct material

• Package labeling and shipping documentation

FDA Requirements (if applicable)

• Drug Master Files (DMF) for certain radiopharmaceuticals

• cGMP compliance for radiopharmaceutical production

DOT Requirements

• 49 CFR 173: Packaging requirements

• Proper shipping names, UN numbers

• Activity limits per package

System Support:

• Templates for required documentation

• Validation that activity limits aren't exceeded

• Audit trail for all production and QC activities

Configurability

Module On/Off:

• Facility director can enable/disable entire module

• Facilities without medical isotope programs don't see this module at

  all

• When enabled, appears as separate section in Neutron OS navigation

Success Metrics

Open Questions

• Existing customer list: Who are current medical isotope

    customers? What's order volume?

• Pricing structure: How is pricing determined? Volume discounts?

• Production capacity: What's max weekly production per isotope?

• Shipping logistics: Which carriers? Who schedules pickups?

• Billing integration: What accounting system is used?

• Standing order patterns: What % of orders are recurring vs.

    one-time?

• Regulatory documentation: What COA format is currently used?

Relationship to Experiment Manager

!Quality assurance procedures diagram

Shared code estimate: ~60% of backend logic is reusable between modules.

NEUP Research Addendum

NEUP Proposal: Medical Isotope Production Optimization

Proposal: AI-driven optimization of medical isotope production scheduling and yield prediction.

Supporting PRD Sections:

• Section "Production Batch Schema" (target_quantity, actual_quantity,

  yield_percentage)

• User stories around production scheduling

• Integration with Scheduling System PRD

Gap Addressed: Current PRD relies on manual batch planning by production manager; no optimization or yield prediction.

Optimization Objectives

New Requirements

New User Stories

• As a production manager, I want AI-recommended production

    schedules that minimize decay losses while meeting all customer     deadlines.

• As a production manager, I want yield predictions with

    confidence intervals before committing to a production batch.

• As a production manager, I want to see the impact of reactor

    schedule changes on all pending isotope orders.

Digital Twin Integration

This addendum should be reviewed with medical isotope program leadership when NEUP results are announced.

Document Status: Draft - Needs validation with NETL medical isotope program staff