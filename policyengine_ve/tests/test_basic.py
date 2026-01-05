"""Basic tests for policyengine-ve."""

import pytest
from policyengine_ve import Simulation, CountryTaxBenefitSystem


def test_system_loads():
    """Test that the tax-benefit system loads correctly."""
    system = CountryTaxBenefitSystem()
    assert system is not None
    assert len(system.variables) > 0


def test_basic_simulation():
    """Test that a basic simulation runs."""
    sim = Simulation(
        situation={
            "persons": {
                "adult": {
                    "age": {2025: 30},
                    "employment_income": {2025: 1000},
                }
            },
            "households": {
                "household": {
                    "members": ["adult"],
                }
            },
        }
    )
    income = sim.calculate("employment_income", 2025)
    assert income[0] == 1000


def test_household_aggregation():
    """Test household income aggregation."""
    sim = Simulation(
        situation={
            "persons": {
                "adult1": {
                    "age": {2025: 35},
                    "employment_income": {2025: 500},
                },
                "adult2": {
                    "age": {2025: 32},
                    "employment_income": {2025: 300},
                },
            },
            "households": {
                "household": {
                    "members": ["adult1", "adult2"],
                }
            },
        }
    )
    hh_income = sim.calculate("household_market_income", 2025)
    assert hh_income[0] == 800
