"""Sistema Patria bonus programs for workers and retirees."""

from policyengine_ve.model_api import *


class sistema_patria_bonus(Variable):
    value_type = float
    entity = Person
    label = "Sistema Patria annual bonus"
    unit = VES
    definition_period = YEAR
    default_value = 0
    reference = (
        "https://venezuelanalysis.com/news/venezuela-maduro-govt-announces-may-day-bonus-increase-maintains-wage-freeze/",
        "https://misionverdad.com/english/venezuelas-minimum-comprehensive-income-announcements-thorough-reading",
    )

    def formula(person, period, parameters):
        # Must have Carnet de la Patria to receive any bonus
        has_carnet = person("has_carnet_patria", period)

        # Employment and retirement status
        is_public = person("is_public_sector", period)
        is_employed = person("is_employed", period)
        is_retired = person("is_retired", period)
        was_public_retiree = person("was_public_sector_retiree", period)

        # Parameter paths for bonus amounts
        p = parameters(period).gov.patria.bonuses

        # Determine which bonus tier applies (priority order)
        is_public_worker = is_public & is_employed
        is_public_retiree = is_retired & was_public_retiree
        is_regular_pensioner = is_retired & ~was_public_retiree

        # Calculate bonus based on tier
        bonus = where(
            is_public_worker,
            p.public_sector_worker.amount,
            where(
                is_public_retiree,
                p.public_sector_retiree.amount,
                where(is_regular_pensioner, p.regular_pensioner.amount, 0),
            ),
        )

        return has_carnet * bonus
