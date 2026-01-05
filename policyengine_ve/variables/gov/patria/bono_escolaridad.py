"""Bono 100% Escolaridad - School bonus for children.

This is a monthly bonus paid per child enrolled in school (initial, primary,
or secondary education). Requires Carnet de la Patria registration.

References:
- https://meridiano.net/servicios/bono-100-escolaridad-5-pasos-para-registrar-a-tu-hijo-y-recibir-bs-446-mensuales-por-nino-a-202551110300
"""

from policyengine_ve.model_api import *


class bono_escolaridad_eligible(Variable):
    value_type = bool
    entity = Person
    label = "Eligible for school bonus"
    definition_period = YEAR
    reference = "https://meridiano.net/servicios/bono-100-escolaridad-5-pasos-para-registrar-a-tu-hijo-y-recibir-bs-446-mensuales-por-nino-a-202551110300"

    def formula(person, period, parameters):
        age = person("age", period)
        p = parameters(period).gov.patria.bonuses.escolaridad
        min_age = p.min_age
        max_age = p.max_age

        age_eligible = (age >= min_age) & (age <= max_age)

        # Must be enrolled in school
        in_school = person("is_in_school", period)

        # Household must have Carnet de la Patria
        # We check if any adult in household has carnet
        has_carnet = person.household("household_has_carnet_patria", period)

        return age_eligible & in_school & has_carnet


class bono_escolaridad(Variable):
    value_type = float
    entity = Person
    label = "Bono 100% Escolaridad (school bonus)"
    unit = VES
    definition_period = YEAR
    reference = "https://meridiano.net/servicios/bono-100-escolaridad-5-pasos-para-registrar-a-tu-hijo-y-recibir-bs-446-mensuales-por-nino-a-202551110300"

    def formula(person, period, parameters):
        eligible = person("bono_escolaridad_eligible", period)
        monthly_amount = parameters(period).gov.patria.bonuses.escolaridad.amount
        annual_amount = monthly_amount * 12
        return where(eligible, annual_amount, 0)
