import os
from typing import List
from decimal import Decimal
from functools import reduce
from collections import defaultdict

from ..models import PlanModel, BenefitModel, AgeBandsModel, RateTableModel, \
    BenefitRateModel, BenefitFactorModel, ProvisionModel, BenefitAgeRateModel, \
    PlanRateModel


class Rating_PlanRates:

    def __init__(
            self,
            plan: PlanModel,
            age_band_id: int,
            plan_rate_code: str,
            family_code: str,
            smoker_status: str,
            benefit_rates: List[BenefitRateModel],
            *args, **kwargs):
        self.plan = plan
        self.age_band_id = age_band_id
        self.plan_rate_code = plan_rate_code
        self.family_code = family_code
        self.smoker_status = smoker_status
        self.benefit_rates = benefit_rates

    def calculate(self) -> None:
        """
        Aggregate the premium from all benefits underneath a
        plan rate code
        """
        premium = Decimal('0.00000')
        for benefit_rate in self.benefit_rates:
            premium += benefit_rate.benefit_rate_premium

        # build the plan rate model
        plan_rate_model = PlanRateModel(
            plan_id=self.plan.plan_id,
            age_band_id=self.age_band_id,
            plan_rate_code=self.plan_rate_code,
            family_code=self.family_code,
            smoker_status=self.smoker_status,
            plan_rate_premium=premium
        )
        plan_rate_model.benefit_rates = self.benefit_rates
        return plan_rate_model
