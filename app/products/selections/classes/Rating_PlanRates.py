import os
from typing import List
from decimal import Decimal
from functools import reduce
from collections import defaultdict

from ..models import Model_SelectionPlan, Model_SelectionBenefitRate, Model_SelectionRateGroupSummary


class Rating_PlanRates:

    def __init__(
            self,
            plan: Model_SelectionPlan,
            age_band_id: int,
            rate_group_id: int,
            family_code: str,
            smoker_status: str,
            gender: str, 
            benefit_rates: List[Model_SelectionBenefitRate],
            *args, **kwargs):
        self.plan = plan
        self.age_band_id = age_band_id
        self.rate_group_id = rate_group_id
        self.family_code = family_code
        self.smoker_status = smoker_status
        self.gender = gender
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
        plan_rate_model = Model_SelectionRateGroupSummary(
            selection_plan_id=self.plan.selection_plan_id,
            selection_age_band_id=self.age_band_id,
            config_rate_group_id=self.rate_group_id,
            family_code=self.family_code,
            smoker_status=self.smoker_status,
            gender=self.gender, 
            rate_group_premium=premium
        )
        plan_rate_model.benefit_rates = self.benefit_rates
        return plan_rate_model

