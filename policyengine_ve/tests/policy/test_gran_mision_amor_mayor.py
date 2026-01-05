"""Tests for Gran Mision Amor Mayor social pension.

This test file demonstrates the CLIFF behavior in Venezuela's pension system.
The cliff occurs at the household income threshold equal to the minimum wage:
- If household income < 1560 VES/year: receive full pension (1560 VES/year)
- If household income >= 1560 VES/year: receive $0

This creates an INFINITE marginal tax rate at the threshold (a "notch").
"""

import pytest
from policyengine_ve import Simulation


class TestAgeEligibilityMen:
    """Test age thresholds for men (60+)."""

    def test_man_age_59_not_eligible(self):
        """Man age 59 is not eligible (below age threshold)."""
        sim = Simulation(
            situation={
                "persons": {
                    "elder": {
                        "age": {2025: 59},
                        "is_male": {2025: True},
                        "employment_income": {2025: 0},
                    }
                },
                "households": {
                    "household": {"members": ["elder"]},
                },
            }
        )
        result = sim.calculate("gran_mision_amor_mayor", 2025)
        assert result[0] == 0

    def test_man_age_60_eligible(self):
        """Man age 60 is eligible (at age threshold)."""
        sim = Simulation(
            situation={
                "persons": {
                    "elder": {
                        "age": {2025: 60},
                        "is_male": {2025: True},
                        "employment_income": {2025: 0},
                    }
                },
                "households": {
                    "household": {"members": ["elder"]},
                },
            }
        )
        result = sim.calculate("gran_mision_amor_mayor", 2025)
        # 130 VES/month * 12 = 1560 VES/year
        assert result[0] == 1560

    def test_man_age_65_eligible(self):
        """Man age 65 is eligible."""
        sim = Simulation(
            situation={
                "persons": {
                    "elder": {
                        "age": {2025: 65},
                        "is_male": {2025: True},
                        "employment_income": {2025: 0},
                    }
                },
                "households": {
                    "household": {"members": ["elder"]},
                },
            }
        )
        result = sim.calculate("gran_mision_amor_mayor", 2025)
        assert result[0] == 1560


class TestAgeEligibilityWomen:
    """Test age thresholds for women (55+)."""

    def test_woman_age_54_not_eligible(self):
        """Woman age 54 is not eligible (below age threshold)."""
        sim = Simulation(
            situation={
                "persons": {
                    "elder": {
                        "age": {2025: 54},
                        "is_male": {2025: False},
                        "employment_income": {2025: 0},
                    }
                },
                "households": {
                    "household": {"members": ["elder"]},
                },
            }
        )
        result = sim.calculate("gran_mision_amor_mayor", 2025)
        assert result[0] == 0

    def test_woman_age_55_eligible(self):
        """Woman age 55 is eligible (at age threshold)."""
        sim = Simulation(
            situation={
                "persons": {
                    "elder": {
                        "age": {2025: 55},
                        "is_male": {2025: False},
                        "employment_income": {2025: 0},
                    }
                },
                "households": {
                    "household": {"members": ["elder"]},
                },
            }
        )
        result = sim.calculate("gran_mision_amor_mayor", 2025)
        assert result[0] == 1560


class TestCliffBehavior:
    """Test the CRITICAL income cliff behavior.

    This is the key feature of the program:
    - Person earning 1559 VES -> gets 1560 pension -> total 3119
    - Person earning 1560 VES -> gets 0 pension -> total 1560
    - Earning $1 more loses the ENTIRE benefit!
    """

    def test_just_below_threshold_receives_full_benefit(self):
        """Just below income threshold - receives full benefit."""
        sim = Simulation(
            situation={
                "persons": {
                    "elder": {
                        "age": {2025: 65},
                        "is_male": {2025: True},
                        "employment_income": {2025: 1559},  # Just below 1560
                    }
                },
                "households": {
                    "household": {"members": ["elder"]},
                },
            }
        )
        result = sim.calculate("gran_mision_amor_mayor", 2025)
        # Receives full pension (1560 VES/year)
        # Total income: 1559 + 1560 = 3119 VES
        assert result[0] == 1560

    def test_at_threshold_loses_entire_benefit(self):
        """At income threshold - loses ENTIRE benefit (CLIFF)."""
        sim = Simulation(
            situation={
                "persons": {
                    "elder": {
                        "age": {2025: 65},
                        "is_male": {2025: True},
                        "employment_income": {2025: 1560},  # At threshold
                    }
                },
                "households": {
                    "household": {"members": ["elder"]},
                },
            }
        )
        result = sim.calculate("gran_mision_amor_mayor", 2025)
        # CLIFF: Entire benefit lost when income >= threshold
        # Total income: 1560 + 0 = 1560 VES
        # Earning $1 more loses $1560!
        assert result[0] == 0

    def test_above_threshold_no_benefit(self):
        """Above income threshold - no benefit."""
        sim = Simulation(
            situation={
                "persons": {
                    "elder": {
                        "age": {2025: 65},
                        "is_male": {2025: True},
                        "employment_income": {2025: 2000},
                    }
                },
                "households": {
                    "household": {"members": ["elder"]},
                },
            }
        )
        result = sim.calculate("gran_mision_amor_mayor", 2025)
        assert result[0] == 0


class TestHouseholdIncomeTest:
    """Test that income test is at household level, not individual."""

    def test_eligible_elder_with_earning_spouse_disqualified(self):
        """Eligible elder with earning spouse - household income test."""
        sim = Simulation(
            situation={
                "persons": {
                    "elder": {
                        "age": {2025: 65},
                        "is_male": {2025: True},
                        "employment_income": {2025: 0},
                    },
                    "spouse": {
                        "age": {2025: 50},
                        "is_male": {2025: False},
                        "employment_income": {
                            2025: 1560
                        },  # Spouse earns enough to disqualify
                    },
                },
                "households": {
                    "household": {"members": ["elder", "spouse"]},
                },
            }
        )
        elder_result = sim.calculate("gran_mision_amor_mayor", 2025)
        # Household income >= threshold, so elder loses benefit
        assert elder_result[0] == 0  # elder
        assert elder_result[1] == 0  # spouse (not age-eligible anyway)

    def test_eligible_elder_with_low_earning_spouse_qualifies(self):
        """Eligible elder with low-earning spouse - passes income test."""
        sim = Simulation(
            situation={
                "persons": {
                    "elder": {
                        "age": {2025: 65},
                        "is_male": {2025: True},
                        "employment_income": {2025: 0},
                    },
                    "spouse": {
                        "age": {2025: 50},
                        "is_male": {2025: False},
                        "employment_income": {2025: 500},  # Below threshold
                    },
                },
                "households": {
                    "household": {"members": ["elder", "spouse"]},
                },
            }
        )
        result = sim.calculate("gran_mision_amor_mayor", 2025)
        # Household income < threshold, elder receives benefit
        assert result[0] == 1560  # elder
        assert result[1] == 0  # spouse (not age-eligible)


class TestBothSpousesEligible:
    """Test when both spouses meet age requirements."""

    def test_both_elderly_spouses_receive_pension(self):
        """Both elderly spouses eligible - both receive pension."""
        sim = Simulation(
            situation={
                "persons": {
                    "elder1": {
                        "age": {2025: 65},
                        "is_male": {2025: True},
                        "employment_income": {2025: 0},
                    },
                    "elder2": {
                        "age": {2025: 60},
                        "is_male": {2025: False},
                        "employment_income": {2025: 0},
                    },
                },
                "households": {
                    "household": {"members": ["elder1", "elder2"]},
                },
            }
        )
        result = sim.calculate("gran_mision_amor_mayor", 2025)
        # Both meet age requirements, household income = 0 < threshold
        assert result[0] == 1560  # elder1
        assert result[1] == 1560  # elder2


class TestEdgeCases:
    """Test edge cases."""

    def test_young_person_not_eligible(self):
        """Young person not eligible regardless of income."""
        sim = Simulation(
            situation={
                "persons": {
                    "young": {
                        "age": {2025: 30},
                        "is_male": {2025: True},
                        "employment_income": {2025: 0},
                    }
                },
                "households": {
                    "household": {"members": ["young"]},
                },
            }
        )
        result = sim.calculate("gran_mision_amor_mayor", 2025)
        assert result[0] == 0

    def test_pension_income_counts_toward_income_test(self):
        """Elder with pension income also counts toward income test."""
        sim = Simulation(
            situation={
                "persons": {
                    "elder": {
                        "age": {2025: 70},
                        "is_male": {2025: True},
                        "employment_income": {2025: 0},
                        "pension_income": {
                            2025: 1600
                        },  # Other pension above threshold
                    }
                },
                "households": {
                    "household": {"members": ["elder"]},
                },
            }
        )
        result = sim.calculate("gran_mision_amor_mayor", 2025)
        # Already receiving pension above threshold, not eligible
        assert result[0] == 0
