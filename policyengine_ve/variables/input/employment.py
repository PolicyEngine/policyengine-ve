"""Employment status input variables."""

from policyengine_ve.model_api import *


class is_public_sector(Variable):
    value_type = bool
    entity = Person
    label = "Whether employed in public sector"
    definition_period = YEAR
    default_value = False
    documentation = """Public sector workers receive different compensation
    including the Bono de Guerra Economica and other supplements that
    private sector workers do not receive."""


class is_employed(Variable):
    value_type = bool
    entity = Person
    label = "Whether currently employed"
    definition_period = YEAR
    default_value = False


class is_retired(Variable):
    value_type = bool
    entity = Person
    label = "Whether retired"
    definition_period = YEAR
    default_value = False


class was_public_sector_retiree(Variable):
    value_type = bool
    entity = Person
    label = "Whether retired from public sector"
    definition_period = YEAR
    default_value = False
    documentation = """Public administration and state company retirees
    receive higher bonus payments than regular pensioners."""
