"""Hogares de la Patria / Bono Único Familiar.

This is a monthly bonus for low-income families selected through Sistema Patria's
socioeconomic assessment algorithm. The Bono Único Familiar consolidates several
programs including Hogares de la Patria, Parto Humanizado, Lactancia Materna,
José Gregorio Hernández, and 100% Escolaridad.

Since eligibility is based on soft scoring rather than a hard income threshold,
we model eligibility as an input variable.

References:
- https://blog.patria.org.ve/bono-unico-familiar-noviembre-2025/
- https://www.bloomberglinea.com/latinoamerica/venezuela/cuando-pagan-el-bono-unico-familiar-de-enero-2026/
"""

from policyengine_ve.model_api import *


class hogares_patria_bonus(Variable):
    value_type = float
    entity = Person
    label = "Hogares de la Patria / Bono Único Familiar"
    unit = VES
    definition_period = YEAR
    reference = "https://blog.patria.org.ve/bono-unico-familiar-noviembre-2025/"

    def formula(person, period, parameters):
        # Eligibility is an input (soft scoring by Sistema Patria)
        eligible = person("is_hogares_patria_eligible", period)

        # Must have Carnet de la Patria
        has_carnet = person("has_carnet_patria", period)

        monthly_amount = parameters(period).gov.patria.hogares.amount
        annual_amount = monthly_amount * 12

        return where(eligible & has_carnet, annual_amount, 0)
