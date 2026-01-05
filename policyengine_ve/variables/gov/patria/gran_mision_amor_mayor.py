"""Gran Mision Amor Mayor (Love for Elders Mission) social pension.

This program provides a pension equal to the minimum wage to elderly residents
who meet age and income requirements. There is a CLIFF at the income threshold:
if household income >= threshold, the entire benefit is lost.

Eligibility:
- Men: age 60+
- Women: age 55+
- Household monthly income below minimum wage

Benefit: Legal monthly minimum wage (130 VES/month as of 2022)
"""

from policyengine_ve.model_api import *


class gran_mision_amor_mayor(Variable):
    value_type = float
    entity = Person
    label = "Gran Mision Amor Mayor social pension"
    unit = VES
    definition_period = YEAR
    reference = "https://www.ssa.gov/policy/docs/progdesc/ssptw/2018-2019/americas/venezuela.html"

    def formula(person, period, parameters):
        p = parameters(period).gov.patria.amor_mayor

        # Age eligibility: 60+ for men, 55+ for women
        age = person("age", period)
        is_male = person("is_male", period)
        age_threshold = where(
            is_male, p.age_threshold_male, p.age_threshold_female
        )
        age_eligible = age >= age_threshold

        # Household income test: total household market income < threshold
        # Threshold is monthly, so annualize for comparison
        annual_threshold = p.income_threshold * 12
        household_income = person.household("household_market_income", period)
        income_eligible = household_income < annual_threshold

        # CLIFF: If income >= threshold, lose entire benefit
        eligible = age_eligible & income_eligible

        # Benefit: monthly amount * 12 for annual
        annual_benefit = p.benefit_amount * 12

        return where(eligible, annual_benefit, 0)
