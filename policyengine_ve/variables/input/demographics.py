"""Demographic input variables."""

from policyengine_ve.model_api import *


class age(Variable):
    value_type = int
    entity = Person
    label = "Age in years"
    definition_period = YEAR


class is_male(Variable):
    value_type = bool
    entity = Person
    label = "Whether this person is male"
    definition_period = YEAR
    default_value = True


class is_head_of_household(Variable):
    value_type = bool
    entity = Person
    label = "Whether this person is the head of household"
    definition_period = YEAR
    default_value = False
