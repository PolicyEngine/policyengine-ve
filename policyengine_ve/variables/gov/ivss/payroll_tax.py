"""Employee payroll tax contributions for Venezuela.

Implements IVSS (social security) and BANAVIH (housing) employee contributions.

References:
- https://www.ssa.gov/policy/docs/progdesc/ssptw/2018-2019/americas/venezuela.html
- https://www.cloudpay.com/payroll-guide/venezuela-payroll-and-benefits-guide/
"""

from policyengine_ve.model_api import *


class ivss_employee_contribution(Variable):
    value_type = float
    entity = Person
    label = "IVSS employee social security contribution"
    unit = VES
    definition_period = YEAR
    reference = (
        "https://www.ssa.gov/policy/docs/progdesc/ssptw/2018-2019/americas/"
        "venezuela.html",
        "https://www.cloudpay.com/payroll-guide/"
        "venezuela-payroll-and-benefits-guide/",
    )

    def formula(person, period, parameters):
        employment_income = person("employment_income", period)

        # Get IVSS parameters
        p = parameters(period).gov.ivss.employee
        rate = p.rate
        cap_multiplier = p.cap_multiplier

        # Get minimum wage (monthly) and convert to annual cap
        min_wage_monthly = parameters(period).gov.minimum_wage
        annual_cap = min_wage_monthly * cap_multiplier * 12

        # Apply rate to capped income
        capped_income = min_(employment_income, annual_cap)
        return capped_income * rate


class banavih_employee_contribution(Variable):
    value_type = float
    entity = Person
    label = "BANAVIH employee housing contribution"
    unit = VES
    definition_period = YEAR
    reference = (
        "https://www.ssa.gov/policy/docs/progdesc/ssptw/2018-2019/americas/"
        "venezuela.html",
        "https://www.cloudpay.com/payroll-guide/"
        "venezuela-payroll-and-benefits-guide/",
    )

    def formula(person, period, parameters):
        employment_income = person("employment_income", period)

        # Get BANAVIH rate (no cap)
        rate = parameters(period).gov.banavih.employee.rate
        return employment_income * rate


class employee_payroll_tax(Variable):
    value_type = float
    entity = Person
    label = "Total employee payroll taxes"
    unit = VES
    definition_period = YEAR
    reference = (
        "https://www.ssa.gov/policy/docs/progdesc/ssptw/2018-2019/americas/"
        "venezuela.html",
        "https://www.cloudpay.com/payroll-guide/"
        "venezuela-payroll-and-benefits-guide/",
    )
    adds = ["ivss_employee_contribution", "banavih_employee_contribution"]
