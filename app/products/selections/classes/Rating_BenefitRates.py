import os
from typing import List
from decimal import Decimal
from functools import reduce
from collections import defaultdict

from ..models import Model_SelectionPlan, Model_SelectionBenefit, Model_SelectionAgeBands, RateTableModel, \
    Model_SelectionBenefitRate, Model_SelectionBenefitFactor, Model_SelectionProvision, \
    Model_SelectionBenefitAgeRate, PlanRateModel

RATE_ROUNDING_PRECISION = os.getenv("RATE_ROUNDING_PRECISION", 5)


class Rating_BenefitRates:

    def __init__(
            self,
            plan: Model_SelectionPlan,
            benefit: Model_SelectionBenefit,
            age_band: Model_SelectionAgeBands,
            family_code: str,
            smoker_status: str,
            gender: str, 
            benefit_age_rates: List[Model_SelectionBenefitAgeRate],
            *args, **kwargs):
        self.plan = plan
        self.benefit = benefit
        self.age_band = age_band
        self.family_code = family_code
        self.smoker_status = smoker_status
        self.gender = gender
        self.benefit_age_rates = benefit_age_rates

        self.benefit_rates = []

    def weightedAverageAgeBandRates(self) -> Decimal:
        """
        Calculate the weighted average premium for an age band.
        """
        denom = 0
        prem = 0
        for rate in self.benefit_age_rates:
            prem += rate.weight * rate.benefit_age_rate_final_premium
            denom += rate.weight
        return Decimal(round(prem / denom, int(RATE_ROUNDING_PRECISION))) if denom > 0 else 0

    def calculate(self) -> Model_SelectionBenefitRate:
        """
        Calculate the weighted average of all benefit age rates
        underneath a benefit rate. 
        """
        premium = self.weightedAverageAgeBandRates()

        benefit_rate = Model_SelectionBenefitRate(
            selection_plan_id=self.plan.selection_plan_id,
            selection_benefit_id=self.benefit.selection_benefit_id,
            selection_age_band_id=self.age_band.selection_age_band_id,
            family_code=self.family_code,
            smoker_status=self.smoker_status,
            gender=self.gender, 
            benefit_rate_premium=premium
        )

        benefit_rate.benefit_age_rates = self.benefit_age_rates

        return benefit_rate
