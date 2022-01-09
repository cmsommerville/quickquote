from typing import List
from decimal import Decimal
from itertools import product

from ..models import Model_SelectionPlan, Model_SelectionBenefit, Model_SelectionAgeBands,\
    RateTableModel, Model_SelectionBenefitRate, Model_SelectionBenefitFactor, \
    Model_SelectionProvision, Model_SelectionBenefitAgeRate


class Rating_BenefitAgeRateWeights:

    def __init__(
            self,
            plan: Model_SelectionPlan = None,
            weights: dict = None,
            *args, **kwargs):
        
        if plan is None and weights is None:
            raise Exception("Must pass either a plan or weights to Benefit Age Rate Weights")

        self._plan = plan
        self._weights = weights

    def default_weights(self) -> dict:
        """
        Calculates the base rate
        """
        pass


