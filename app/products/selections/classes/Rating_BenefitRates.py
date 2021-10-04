import os
from typing import List
from decimal import Decimal
from functools import reduce
from collections import defaultdict

from ..models import PlanModel, BenefitModel, AgeBandsModel, RateTableModel, \
    BenefitRateModel, BenefitFactorModel, ProvisionModel, BenefitAgeRateModel, \
    PlanRateModel

RATE_ROUNDING_PRECISION = os.getenv("RATE_ROUNDING_PRECISION", 5)


class Rating_BenefitRates:

    def __init__(
            self,
            plan: PlanModel,
            benefit: BenefitModel,
            age_band_id: int,
            family_code: str,
            smoker_status: str,
            benefit_age_rates: List[BenefitAgeRateModel],
            *args, **kwargs):
        self.plan = plan
        self.benefit = benefit
        self.age_band_id = age_band_id
        self.family_code = family_code
        self.smoker_status = smoker_status
        self.benefit_age_rates = benefit_age_rates

        self.benefit_rates = []

    def weightedAverageAgeBandRates(self) -> Decimal:
        """
        Calculate the weighted average premium for an age band.
        """
        denom = 0
        prem = 0
        for rate in self.benefit_age_rates:
            prem += rate.age_weight * rate.benefit_age_rate_final_premium
            denom += rate.age_weight
        return Decimal(round(prem / denom, int(RATE_ROUNDING_PRECISION))) if denom > 0 else 0

    def calculate(self) -> BenefitRateModel:
        """
        Calculate the weighted average of all benefit age rates
        underneath a benefit rate. 
        """
        premium = self.weightedAverageAgeBandRates()

        benefit_rate = BenefitRateModel(
            plan_id=self.plan.plan_id,
            benefit_id=self.benefit.benefit_id,
            age_band_id=self.age_band_id,
            family_code=self.family_code,
            smoker_status=self.smoker_status,
            benefit_rate_premium=premium
        )

        benefit_rate.benefit_age_rates = self.benefit_age_rates

        return benefit_rate
