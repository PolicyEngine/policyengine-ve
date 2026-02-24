"""Input variable for Hogares de la Patria eligibility.

Eligibility is determined by Sistema Patria's socioeconomic scoring algorithm,
not a hard income threshold. Priority given to:
- Households with 3+ members
- Families with children, elderly, or disabled
- Female heads of household
- Income below national average
- Informal workers

Since this is discretionary/soft scoring, we model it as an input.
"""

from policyengine_ve.model_api import *


class is_hogares_patria_eligible(Variable):
    value_type = bool
    entity = Person
    label = "Whether the person is eligible for Hogares de la Patria"
    definition_period = YEAR
    default_value = False
    reference = (
        "https://blog.patria.org.ve/bono-unico-familiar-noviembre-2025/"
    )
