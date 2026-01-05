"""PolicyEngine Venezuela - Tax-benefit microsimulation model."""

from policyengine_ve.system import (
    CountryTaxBenefitSystem,
    Simulation,
    system,
    CURRENT_YEAR,
)
from policyengine_ve.entities import entities, Person, Household

__all__ = [
    "CountryTaxBenefitSystem",
    "Simulation",
    "system",
    "entities",
    "Person",
    "Household",
    "CURRENT_YEAR",
]

__version__ = "0.1.0"
