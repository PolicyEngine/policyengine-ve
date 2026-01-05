"""Tax-benefit system for Venezuela."""

from pathlib import Path
from policyengine_core.taxbenefitsystems import TaxBenefitSystem
from policyengine_core.simulations import Simulation as CoreSimulation
from policyengine_ve.entities import entities

COUNTRY_DIR = Path(__file__).parent
CURRENT_YEAR = 2025


class CountryTaxBenefitSystem(TaxBenefitSystem):
    """Venezuela tax-benefit system."""

    CURRENCY = "VES"  # Venezuelan Bolivar Soberano
    entities = entities
    variables_dir = COUNTRY_DIR / "variables"
    auto_carry_over_input_variables = True
    basic_inputs = [
        "age",
        "employment_income",
        "is_public_sector",
        "has_carnet_patria",
    ]

    def __init__(self, reform=None):
        super().__init__(entities)
        self.load_parameters(COUNTRY_DIR / "parameters")
        if reform:
            self.apply_reform(reform)


class Simulation(CoreSimulation):
    """Simulation for Venezuela tax-benefit system."""

    default_tax_benefit_system = CountryTaxBenefitSystem
    default_tax_benefit_system_instance = None
    default_calculation_period = CURRENT_YEAR
    default_input_period = CURRENT_YEAR


system = CountryTaxBenefitSystem()
