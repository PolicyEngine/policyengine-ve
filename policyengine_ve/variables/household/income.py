"""Household income aggregation variables."""

from policyengine_ve.model_api import *


class household_market_income(Variable):
    value_type = float
    entity = Household
    label = "Household market income"
    unit = VES
    definition_period = YEAR

    def formula(household, period, parameters):
        person_income = household.members("person_market_income", period)
        return household.sum(person_income)


class person_market_income(Variable):
    value_type = float
    entity = Person
    label = "Person market income"
    unit = VES
    definition_period = YEAR

    adds = [
        "employment_income",
        "self_employment_income",
        "pension_income",
    ]


class household_net_income(Variable):
    value_type = float
    entity = Household
    label = "Household net income after taxes and transfers"
    unit = VES
    definition_period = YEAR

    def formula(household, period, parameters):
        # Sum person-level net income
        person_net = household.members("person_net_income", period)
        person_total = household.sum(person_net)
        # Add household-level benefits
        household_benefits = household("household_benefits", period)
        return person_total + household_benefits


class person_net_income(Variable):
    value_type = float
    entity = Person
    label = "Person net income after taxes and transfers"
    unit = VES
    definition_period = YEAR

    def formula(person, period, parameters):
        market_income = person("person_market_income", period)
        income_tax = person("income_tax", period)
        employee_payroll_tax = person("employee_payroll_tax", period)
        person_benefits = person("person_benefits", period)
        return (
            market_income - income_tax - employee_payroll_tax + person_benefits
        )


class person_benefits(Variable):
    value_type = float
    entity = Person
    label = "Total person-level benefits"
    unit = VES
    definition_period = YEAR

    adds = [
        "sistema_patria_bonus",
        "gran_mision_amor_mayor",
        "bono_escolaridad",
        "bono_lactancia",
        "hogares_patria_bonus",
    ]


class household_benefits(Variable):
    value_type = float
    entity = Household
    label = "Total household-level benefits"
    unit = VES
    definition_period = YEAR
    default_value = 0
    # Will add CLAP value, housing subsidies, etc.
