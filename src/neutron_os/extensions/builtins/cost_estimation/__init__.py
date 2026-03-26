"""
NeutronOS AWS Cost Estimation Tool.

Calculates comprehensive AWS infrastructure costs for NeutronOS Phase 1
based on stakeholder inputs and pre-defined scenarios.

Usage:
    from cost_estimation_tool import scenarios, CostCalculator

    # Get a pre-defined scenario
    recommended = scenarios.scenario_recommended()

    # Or calculate custom costs from stakeholder responses
    from data_models import StakeholderResponses
    responses = StakeholderResponses(...)
    calculator = CostCalculator(responses)
    breakdown = calculator.calculate_full_breakdown()
"""

from .cost_calculator import CostCalculator
from .data_models import (
    ComplianceInputs,
    CostBreakdown,
    MLInputs,
    OperationsInputs,
    PhysicsInputs,
    PiXieInputs,
    StakeholderResponses,
)
from .reporter import CostReporter
from .scenarios import get_scenario, scenario_full_cloud, scenario_minimal, scenario_recommended

__version__ = "0.1.0"
__all__ = [
    "StakeholderResponses",
    "CostBreakdown",
    "PhysicsInputs",
    "OperationsInputs",
    "PiXieInputs",
    "MLInputs",
    "ComplianceInputs",
    "CostCalculator",
    "get_scenario",
    "scenario_minimal",
    "scenario_recommended",
    "scenario_full_cloud",
    "CostReporter",
]
