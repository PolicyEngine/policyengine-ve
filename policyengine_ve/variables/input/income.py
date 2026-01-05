"""Income input variables."""

from policyengine_ve.model_api import *


class employment_income(Variable):
    value_type = float
    entity = Person
    label = "Employment income"
    unit = VES
    definition_period = YEAR
    reference = "https://taxsummaries.pwc.com/venezuela/individual/taxes-on-personal-income"


class self_employment_income(Variable):
    value_type = float
    entity = Person
    label = "Self-employment income"
    unit = VES
    definition_period = YEAR


class pension_income(Variable):
    value_type = float
    entity = Person
    label = "Pension income"
    unit = VES
    definition_period = YEAR
