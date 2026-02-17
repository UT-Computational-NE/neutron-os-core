# DeepLynx + Research Reactor Digital Twins
## Discussion Notes — February 2026

**Ben Booth, UT Austin Computational NE**  
*Prepared for conversation with Ryan Stewart, INL*

---

## What We're Building

We're developing digital twin infrastructure for research reactors (TRIGA at NETL, eventually others). Our goals align closely with what you demonstrated in the AGN-201 paper:

- **Real-time anomaly detection** using physics-informed surrogate models
- **ML-based operational monitoring** (we're also looking at similar approaches)
- **Path toward semi-autonomous operation** with operator-in-the-loop

We're looking at DeepLynx carefully—both the codebase and your published work—and want to make sure we understand its capabilities correctly before we reinvent any wheels.

---

## What We Love About DeepLynx

### 1. Ontology-First Design
The ability to define reactor components, relationships, and properties through a formal ontology is exactly right. We don't want to hardcode "what a pump is" into application logic.

**Question:** How mature is the DIAMOND ontology for TRIGAs specifically? Could we adopt or extend it?

### 2. Graph-Based Relationships
Queries like "what components does this detector monitor?" or "what's the containment hierarchy?" are naturally graph problems. GraphQL makes this elegant.

**Question:** In your AGN-201 deployment, how often did you query structural relationships vs. time-series data? Roughly what ratio?

### 3. Ledger Table Pattern (ADR-001)
Denormalizing historical snapshots so audit queries don't require JOINs across evolving schemas is clever. We need this for regulatory compliance.

**Question:** Is this pattern used in production at INL facilities, or still emerging?

### 4. Safety Limits as First-Class Concepts
In the NRAD ontology, I noticed `safety_importance`, voting logic (`2/3`), and TSR references are explicit properties. This seems really useful to us.

**Question:** How do you envision these limits being used at runtime? Are they queryable during operations, or primarily for documentation?

---

## What We're Trying to Understand

### Time-Series Data Flow

From the AGN-201 paper, it looks like:
1. LabVIEW DAS writes CSV files every 10 seconds
2. Jester tails the CSVs and sends to DeepLynx on an interval
3. DeepLynx stores in its tabular/temporal system
4. External Python processes (your Gaussian process SM, Isolation Forest) query the data

**Questions:**
- What's the typical end-to-end latency from sensor → DeepLynx → available for query?
- Is there a path to true streaming (sub-second) ingestion, or is interval-based the design intent?
- We're looking at high-frequency scenarios (100+ Hz sensor data for some experiments). Is that a use case DeepLynx is targeting?

### ML Model Integration

Your surrogate models and anomaly detection run as separate Python processes that query DeepLynx. 

**Questions:**
- Is there interest in tighter integration? (e.g., DeepLynx triggering model retraining when new data arrives)
- How do you handle model versioning and tracking which model produced which predictions?
- For the Isolation Forest, how did you handle the feedback loop when operators confirmed or dismissed anomalies?

### Multi-Reactor / Fleet Scenarios

We're thinking ahead to scenarios with multiple research reactors sharing patterns.

**Questions:**
- Has DeepLynx been deployed across multiple facilities with shared ontologies?
- How would cross-facility anomaly correlation work? (e.g., "this pattern appeared at Facility A last month")

---

## What We Need (Our Wish List)

These are capabilities we're building toward. We'd love to know if DeepLynx supports them today, has them on the roadmap, or if they're outside scope:

| Capability | Our Need | DeepLynx Status? |
|------------|----------|------------------|
| **Streaming ingestion** | Sub-second sensor data for real-time digital twin | ? |
| **Time-travel queries** | "What was the state at t-6 months?" for historical analysis | ? |
| **ML training pipelines** | Scheduled retraining of surrogate models on new data | ? |
| **Uncertainty quantification** | Confidence intervals on predictions | ? |
| **Columnar analytics** | Fast aggregations over millions of rows | DuckDB in v2 ✓ |
| **MCP/AI agent integration** | LLM tools that query reactor state | Early implementation ✓ |

---

## Collaboration Ideas

### Near-Term (If Aligned)
- **Ontology sharing**: Could we adopt or contribute to DIAMOND for TRIGAs?
- **Data format standards**: Common schema for inter-facility data exchange
- **MCP tool interoperability**: Our AI agents could query both systems

### Longer-Term
- **Joint NEUP proposal?** Multi-lab digital twin infrastructure
- **Shared benchmarks**: Red-blue team tests across different DT implementations

---

## Our Architecture Sketch

*(High-level, for context on where we're coming from)*

```
Sensors → Streaming Layer → Time-Series Lake → Analytics/ML → Dashboards
              ↑                    ↑
         Real-time            Historical
         (sub-second)         (Iceberg tables)
```

We're using Python-based tooling (dbt, Dagster, DuckDB) because our team is research-focused and that's where our expertise lies. Not a judgment on C#/.NET—just our reality.

**The question we keep coming back to:** Should structural/ontology data live in DeepLynx while time-series lives in our lakehouse? Or is there a cleaner integration path?

---

## Summary

We're impressed by what DeepLynx does well:
- ✅ Ontology management
- ✅ Relationship graphs  
- ✅ Safety metadata
- ✅ Audit/compliance patterns

We're less clear on:
- ❓ High-frequency streaming use cases
- ❓ ML pipeline orchestration
- ❓ Multi-year historical analytics at scale

**What would a roadmap look like for the capabilities we need? Where does collaboration make sense?**
