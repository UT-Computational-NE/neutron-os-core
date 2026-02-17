# Using the Cost Estimation Tool

**Guide to the Python cost_estimation_tool that automates calculations**

Created: February 12, 2026  
For: Anyone populating cost estimates after Feb 16 data collection

---

## Quick Start (5 minutes)

### 1. Verify Installation

```bash
cd Neutron_OS/cost_estimation_tool
python test_scenarios.py
```

Expected output:
```
✓ All tests passed!
```

### 2. Generate Pre-Defined Scenarios

```bash
# Show all three scenarios in markdown table
python main.py --compare --format markdown

# Show recommended scenario in detailed format
python main.py --scenario recommended --detailed --format markdown

# Export as JSON for data analysis
python main.py --compare --format json --output costs.json
```

### 3. You're Done!

Copy the output into your final approval document. All costs are traced back to AWS pricing pages and assumptions.

---

## How It Works: Four Layers

### Layer 1: Data Models (`data_models.py`)

Defines the **structure** of all cost data:

```python
from cost_estimation_tool import StakeholderResponses, OperationsInputs, CostBreakdown

# Define what stakeholders tell us
responses = StakeholderResponses(
    operations=OperationsInputs(
        operating_hours_per_week=80,  # From Nick's Section B
        will_external_collaborators_access=False,  # From Nick
    ),
    pixie=PiXieInputs(
        phase_1_inclusion=True,  # From Max's Section C
        current_daily_data_volume_gb=0.5,  # From Max
    ),
)

# Output: CostBreakdown object with all 9 services
breakdown = CostBreakdown(
    scenario_name="Recommended",
    compute=ComputeCosts(...),
    storage=StorageCosts(...),
    # ... 9 services total
)
```

**Read the code:** `data_models.py` (700 lines)  
**Reference:** See class definitions for all stakeholder input fields

### Layer 2: Cost Calculator (`cost_calculator.py`)

Implements the **formulas** from aws-comprehensive-utility-usage.md:

```python
from cost_estimation_tool import CostCalculator

calculator = CostCalculator(responses)

# Calculate each service category
compute = calculator.calculate_compute_costs()
storage = calculator.calculate_storage_costs()
database = calculator.calculate_database_costs()
# ... 9 services total

# Or just get everything at once
breakdown = calculator.calculate_full_breakdown("Recommended")
```

**Each method implements:**
- Unit prices from AWS pricing pages (e.g., $0.023/GB for S3)
- Assumptions from stakeholder inputs (e.g., 80 hrs/week → 2–3 nodes)
- Formulas from aws-comprehensive-utility-usage.md Section 10

**Read the code:** `cost_calculator.py` (300 lines)  
**Method mapping:**
| Method | AWS Service | Pricing Source |
|--------|---|---|
| `calculate_compute_costs()` | EKS, Lambda, NAT | https://aws.amazon.com/eks/pricing/ |
| `calculate_storage_costs()` | S3, EBS | https://aws.amazon.com/s3/pricing/ |
| `calculate_database_costs()` | RDS, ElastiCache | https://aws.amazon.com/rds/pricing/ |
| `calculate_networking_costs()` | Data Transfer, NAT | https://aws.amazon.com/ec2/pricing/data-transfer/ |
| `calculate_external_services_costs()` | Redpanda, Claude API | https://redpanda.com/pricing, https://www.anthropic.com/pricing |

### Layer 3: Pre-Defined Scenarios (`scenarios.py`)

Instantiates **three scenarios** from the comprehensive utility analysis:

```python
from cost_estimation_tool import scenario_minimal, scenario_recommended, scenario_full_cloud

# Each returns a complete CostBreakdown
minimal = scenario_minimal()           # $612/mo
recommended = scenario_recommended()   # $1,134/mo
full_cloud = scenario_full_cloud()     # $2,016/mo

# All pre-populated with realistic assumptions
print(f"Recommended monthly cost: ${recommended.total_monthly:.2f}")
print(f"2026 cost (9 months): ${recommended.annual_cost_2026_9mo():,.2f}")
print(f"2027 cost (12 months): ${recommended.annual_cost_2027_12mo():,.2f}")
```

**Read the code:** `scenarios.py` (200 lines)  
**How to modify:** Change cost values in scenario definitions to test sensitivity

### Layer 4: Reporting (`reporter.py`)

Formats **output** for humans:

```python
from cost_estimation_tool import CostReporter

scenarios = [scenario_minimal(), scenario_recommended(), scenario_full_cloud()]

# Generate markdown table for approval document
markdown_report = CostReporter.to_markdown_table(scenarios)
print(markdown_report)

# Generate detailed breakdown for one scenario
detailed = CostReporter.to_detailed_markdown(scenario_recommended())
print(detailed)

# Export as JSON for data pipeline
json_export = CostReporter.to_json(scenarios)
with open("costs.json", "w") as f:
    f.write(json_export)

# Export as CSV for spreadsheet
csv_export = CostReporter.to_csv(scenarios)
with open("costs.csv", "w") as f:
    f.write(csv_export)

# Plain text summary for terminal
summary = CostReporter.to_plain_text_summary(scenario_recommended())
print(summary)
```

**Read the code:** `reporter.py` (400 lines)  
**Output formats:**
- **Markdown:** For approval documents, GitHub wikis
- **JSON:** For programmatic analysis, version control
- **CSV:** For Excel spreadsheets
- **Plain text:** For email, terminal output

---

## Workflow: Feb 16–18 (Using the Tool)

### Feb 16 EOD: Collect Data

Stakeholders return completed:
- Section A (Cole): MPACT frequency, archive size
- Section B (Nick): Operating hours, data volumes
- Section C (Max): PiXie Phase 1 decision, data rates
- Section D (Jay): RAG usage, training frequency
- Section E (Dr. Clarno): ITAR ruling, TACC status

### Feb 17 Morning: Load Responses into Tool

Create a JSON file from stakeholder responses:

```json
{
  "physics": {
    "mpact_states_per_run": 50,
    "mpact_wall_clock_minutes": 2.5,
    "bias_correction_retraining_frequency": "monthly"
  },
  "operations": {
    "operating_hours_per_week": 80,
    "will_external_collaborators_access": false
  },
  "pixie": {
    "phase_1_inclusion": true,
    "current_daily_data_volume_gb": 0.5
  },
  "ml": {
    "expected_claude_queries_per_day": 10,
    "debug_logging": false
  },
  "compliance": {
    "aws_region_requirement": "standard",
    "audit_trail_retention_years": 7
  }
}
```

Or use Python directly:

```python
from cost_estimation_tool import StakeholderResponses, OperationsInputs, PiXieInputs
from cost_estimation_tool import CostCalculator

responses = StakeholderResponses(
    operations=OperationsInputs(operating_hours_per_week=80),
    pixie=PiXieInputs(phase_1_inclusion=True, current_daily_data_volume_gb=0.5),
    # ... etc for all sections
)

calculator = CostCalculator(responses)
custom_breakdown = calculator.calculate_full_breakdown("Custom (Feb 16 Data)")
```

### Feb 17 Afternoon: Generate Reports

Compare custom estimate vs. pre-defined scenarios:

```bash
# Option 1: Use custom stakeholder data
python main.py --custom --input responses.json --format markdown --detailed

# Option 2: Compare all pre-defined scenarios
python main.py --compare --format markdown

# Option 3: Export for final documents
python main.py --compare --format json --output final-costs.json
python main.py --scenario recommended --detailed --format markdown > detailed-recommended.md
```

### Feb 17–18: Write Approval Documents

Use tool output to populate:
1. **Executive Summary** (1 page)
   - Use `to_plain_text_summary()` or `to_markdown_table()` output
   - Show monthly/annual/biennial costs

2. **Detailed Cost Tables** (5 pages)
   - Use `to_detailed_markdown()` for service-by-service breakdown
   - Include pricing sources from each CostBreakdown object

3. **Technical Justification** (10 pages)
   - Reference tool code + assumptions
   - Link to AWS pricing pages

### Feb 18: Submit to Dr. Clarno

All three documents with tool output + traceability to AWS pricing pages.

---

## Advanced Usage: Custom Scenarios & Sensitivity Analysis

### Modify a Scenario

```python
from cost_estimation_tool import scenario_recommended

# Get the base scenario
breakdown = scenario_recommended()

# Increase egress assumption (scientists download data)
breakdown.networking.data_egress_monthly = 200  # Instead of 80
breakdown.networking.__post_init__()  # Recalculate total

# Redpanda tier increase
breakdown.external_services.redpanda_cloud_monthly = 300  # Instead of 200
breakdown.external_services.__post_init__()

# Recalculate total
breakdown.__post_init__()

print(f"With higher egress + Redpanda: ${breakdown.total_monthly:.2f}/mo")
```

### Sensitivity Analysis

```python
# What if egress doubles?
scenarios_high_egress = []
for egress in [50, 100, 200, 400]:
    breakdown = scenario_recommended()
    breakdown.networking.data_egress_monthly = egress
    breakdown.networking.__post_init__()
    breakdown.__post_init__()
    scenarios_high_egress.append(breakdown)

# Compare
from cost_estimation_tool import CostReporter
table = CostReporter.to_markdown_table(scenarios_high_egress)
print("Sensitivity Analysis: Data Egress Impact")
print(table)
```

### What-If: Skip Redpanda?

```python
breakdown = scenario_recommended()
breakdown.external_services.redpanda_cloud_monthly = 0  # Skip PiXie
breakdown.external_services.__post_init__()
breakdown.__post_init__()

print(f"If PiXie deferred: ${breakdown.total_monthly:.2f}/mo (save ${breakdown.external_services.redpanda_cloud_monthly:.2f})")
```

---

## Traceability: From Tool to AWS Pricing Pages

Every cost in the tool traces back to an AWS pricing page:

**Example: S3 Storage**

```python
# In cost_calculator.py, calculate_storage_costs():
s3_standard_monthly = (daily_avg_gb * 2) * 0.023
#                                            ^
#                                    $0.023/GB/mo
#                                    From: https://aws.amazon.com/s3/pricing/
#                                    Last verified: Feb 12, 2026
```

**Example: EKS Compute**

```python
# In scenarios.py, scenario_recommended():
eks_control_plane_monthly = 72.0
#                           ^
#                    $0.10/hour × 730 hours/month = $73
#                    From: https://aws.amazon.com/eks/pricing/
#                    Last verified: Feb 12, 2026
```

**To verify any cost:**

1. Find the service in `cost_calculator.py`
2. Look for unit price (e.g., `0.023` for S3)
3. Check the comment for AWS pricing page link
4. Visit that page and confirm price matches

---

## Testing & Validation

Run the included tests to verify calculations:

```bash
# Run all tests
python test_scenarios.py

# Output:
# ✓ Minimal scenario: $612/mo
# ✓ Recommended scenario: $1,134/mo
# ✓ Full Cloud scenario: $2,016/mo
# ✓ All service cost ranges validated
# ✓ Annual calculations correct
```

Each test verifies:
- Monthly costs match expected values (±tolerance)
- Service costs fall within known ranges
- Annual/biennial calculations are correct
- Export formats (JSON, CSV, markdown) work

---

## Exporting to Excel / Finance Tools

### Export as CSV

```bash
python main.py --compare --format csv --output costs.csv
```

Open in Excel and enhance:
- Add your own formatting
- Create charts/graphs
- Build financial models
- Calculate ROI vs. TACC

### Export as JSON for Data Pipelines

```bash
python main.py --compare --format json --output costs.json
```

Load into Python/R/SQL for:
- Join with other cost data
- Track over time
- Statistical analysis
- Dashboard integration

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'cost_estimation_tool'"

Ensure you're in the right directory:
```bash
cd Neutron_OS/cost_estimation_tool
python main.py --compare
```

### "AssertionError: Scenario cost mismatch"

The pre-defined scenarios don't match expected values (e.g., $612 for minimal).

**Check:**
1. Did you modify scenarios.py? Revert.
2. Did you modify data_models.py cost logic? Revert.
3. Run `python test_scenarios.py` to see which scenario failed.

### "ValueError: Unknown scenario"

Use correct scenario names (case-insensitive):
```bash
python main.py --scenario minimal      # ✓
python main.py --scenario MINIMAL      # ✓
python main.py --scenario min          # ✗ Unknown scenario
```

### Custom responses don't load

Check JSON format:
```json
{
  "operations": {
    "operating_hours_per_week": 80,  // Numeric, not string
    "will_external_collaborators_access": true  // Boolean
  }
}
```

---

## Key Files Reference

| File | Purpose | Read If |
|------|---------|---------|
| `data_models.py` | Data classes | You want to understand the structure |
| `cost_calculator.py` | Cost formulas | You want to understand how we calculate |
| `scenarios.py` | Pre-defined scenarios | You want to modify a scenario |
| `reporter.py` | Output formatting | You want to add a new export format |
| `main.py` | CLI interface | You want to understand command-line options |
| `test_scenarios.py` | Validation tests | You want to verify calculations |
| `requirements.txt` | Dependencies | You want to install packages |

---

## Integration with Approval Documents

### In Executive Summary

```markdown
**Cost Estimate (Recommended Scenario)**

Generated by: cost_estimation_tool (Python), Feb 17, 2026
Based on stakeholder data collected Feb 12–16
All costs verified against AWS Pricing Calculator

| Timeframe | Cost |
|-----------|------|
| Monthly | $1,134 |
| 2026 (9 months) | $10,206 |
| 2027 (12 months) | $13,608 |
| **Phase 1 Total** | **$23,814** |

See [Detailed Cost Tables](aws-cost-estimate-tables.md) for service breakdown.
```

### In Detailed Cost Tables

```markdown
**Generated by:** cost_estimation_tool/scenarios.py::scenario_recommended()
**Pricing Date:** February 12, 2026
**Pricing Sources:** AWS (https://aws.amazon.com/pricing/), Redpanda (https://redpanda.com/pricing/), Anthropic (https://www.anthropic.com/pricing/)

[Tool outputs table here]

**Assumptions:**
- Operating hours: 80/week (from Nick, Section B1a)
- Data volume: 150 GB/year baseline + PiXie 0.5 GB/day (from Jay & Max)
- External collaboration: No external dashboard access (from Nick, Section B)
- Region: US East 1 standard AWS (from Dr. Clarno, Section E)
```

---

## Next Steps

1. ✅ **Test the tool** (run test_scenarios.py)
2. ⏳ **Wait for stakeholder responses** (due Feb 16)
3. ⏳ **Load responses** into cost_estimation_tool or JSON file (Feb 17)
4. ⏳ **Generate reports** using main.py (Feb 17–18)
5. ⏳ **Write approval documents** with tool output (Feb 17–18)
6. ⏳ **Submit to Dr. Clarno** with all three documents (Feb 18)
7. 🚀 **Launch Phase 1** (Feb 2026)
8. 📊 **Track actual costs** with AWS Cost Explorer (ongoing)
9. 🔄 **Compare estimated vs. actual** (monthly)

---

**Questions?** See README.md in this tool directory, or refer to:
- [COST-ESTIMATION-SOURCES.md](COST-ESTIMATION-SOURCES.md) — Where all the numbers come from
- [aws-cost-estimation-methodology.md](aws-cost-estimation-methodology.md) — Deep dive into methodology
