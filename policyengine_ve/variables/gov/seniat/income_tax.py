"""Personal income tax (Impuesto Sobre la Renta - ISLR)."""

from policyengine_ve.model_api import *
import numpy as np


class taxable_income(Variable):
    value_type = float
    entity = Person
    label = "Taxable income"
    unit = VES
    definition_period = YEAR
    reference = "https://taxsummaries.pwc.com/venezuela/individual/taxes-on-personal-income"

    adds = ["employment_income", "self_employment_income"]


class income_tax(Variable):
    value_type = float
    entity = Person
    label = "Personal income tax"
    unit = VES
    definition_period = YEAR
    reference = "https://taxsummaries.pwc.com/venezuela/individual/taxes-on-personal-income"

    def formula(person, period, parameters):
        # Get taxable income in VES
        income_ves = person("taxable_income", period)

        # Get Tax Unit value (Unidad Tributaria)
        tu_value = parameters(period).gov.tax_unit

        # Convert income to Tax Units
        income_tu = income_ves / tu_value

        # Get tax scales
        p = parameters(period).gov.seniat.income_tax
        rate_scale = p.rate
        deduction_scale = p.deduction

        # Extract thresholds, rates, and deductions
        thresholds = np.array(rate_scale.thresholds)
        rates = np.array(rate_scale.rates)
        deductions = np.array(deduction_scale.amounts)

        # Determine bracket index for each person (highest applicable bracket)
        # Process from low to high so higher brackets overwrite lower ones
        bracket_idx = np.zeros_like(income_tu, dtype=int)
        for i in range(len(thresholds)):
            bracket_idx = where(income_tu >= thresholds[i], i, bracket_idx)

        # Get rate and deduction for each person's bracket
        rate = np.take(rates, bracket_idx)
        deduction_tu = np.take(deductions, bracket_idx)

        # Calculate tax: (income * rate - deduction) in Tax Units
        tax_tu = income_tu * rate - deduction_tu

        # Convert back to VES and ensure non-negative
        return max_(tax_tu * tu_value, 0)
