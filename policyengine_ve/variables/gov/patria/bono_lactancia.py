"""Bono Lactancia Materna - Breastfeeding bonus.

This is a monthly bonus for mothers with young children (under 2 years).
Requires Carnet de la Patria registration.

References:
- https://www.trosell.net/news/inicia_pago_del_bono_de_lactancia_materna/2025-03-02-1652
"""

from policyengine_ve.model_api import *


class bono_lactancia(Variable):
    value_type = float
    entity = Person
    label = "Bono Lactancia Materna (breastfeeding bonus)"
    unit = VES
    definition_period = YEAR
    reference = "https://www.trosell.net/news/inicia_pago_del_bono_de_lactancia_materna/2025-03-02-1652"

    def formula(person, period, parameters):
        # Must have a child under 2 (proxy for breastfeeding eligibility)
        has_young_child = person("has_child_under_2", period)

        # Must have Carnet de la Patria
        has_carnet = person("has_carnet_patria", period)

        # Must be female (mother)
        is_female = ~person("is_male", period)

        eligible = has_young_child & has_carnet & is_female

        monthly_amount = parameters(period).gov.patria.bonuses.lactancia.amount
        annual_amount = monthly_amount * 12

        return where(eligible, annual_amount, 0)
