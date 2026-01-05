"""Common imports and utilities for Venezuela model."""

from policyengine_core.model_api import *
from policyengine_core.periods import period as period_
from policyengine_ve.entities import *

# Currency constant
VES = "currency-VES"
USD = "currency-USD"  # Many benefits quoted in USD

# Common periods
YEAR = "year"
MONTH = "month"
ETERNITY = "eternity"
