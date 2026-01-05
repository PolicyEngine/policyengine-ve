"""Input variables related to children."""

from policyengine_ve.model_api import *


class is_in_school(Variable):
    value_type = bool
    entity = Person
    label = "Whether the person is enrolled in school"
    definition_period = YEAR
    default_value = False


class is_breastfeeding(Variable):
    value_type = bool
    entity = Person
    label = "Whether the person is a breastfeeding mother"
    definition_period = YEAR
    default_value = False


class has_child_under_2(Variable):
    value_type = bool
    entity = Person
    label = "Whether the person has a child under 2 years old"
    definition_period = YEAR
    default_value = False
