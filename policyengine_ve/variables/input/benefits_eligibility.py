"""Benefits eligibility input variables."""

from policyengine_ve.model_api import *


class has_carnet_patria(Variable):
    value_type = bool
    entity = Person
    label = "Whether registered with Carnet de la Patria"
    definition_period = YEAR
    default_value = False
    documentation = """The Carnet de la Patria (Fatherland Card) is required
    to access most Venezuelan social programs including CLAP food boxes
    and Sistema Patria bonuses."""
    reference = "https://en.wikipedia.org/wiki/Carnet_de_la_Patria"


class receives_clap(Variable):
    value_type = bool
    entity = Household
    label = "Whether household receives CLAP food boxes"
    definition_period = YEAR
    default_value = False
    documentation = """CLAP (Comités Locales de Abastecimiento y Producción)
    provides subsidized food boxes to registered households."""
