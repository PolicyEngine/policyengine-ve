"""Household-level Carnet de la Patria variables."""

from policyengine_ve.model_api import *


class household_has_carnet_patria(Variable):
    value_type = bool
    entity = Household
    label = "Whether any member of the household has Carnet de la Patria"
    definition_period = YEAR

    def formula(household, period, parameters):
        return household.any(household.members("has_carnet_patria", period))
