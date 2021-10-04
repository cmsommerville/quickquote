from typing import List
from decimal import Decimal
from functools import reduce
from collections import defaultdict

from ..models import PlanModel, BenefitModel, AgeBandsModel,\
    RateTableModel, BenefitRateModel, BenefitFactorModel, \
    ProvisionModel, BenefitAgeRateModel
from .Rating_BenefitFactors import Rating_BenefitFactorList


class Rating_BenefitAgeRates:

    def __init__(
            self,
            plan: PlanModel,
            benefit: BenefitModel,
            rate_table: RateTableModel,
            benefit_factors: List[BenefitFactorModel],
            product_factors: list,
            age_weight: float = 1,
            *args, **kwargs):
        self.plan = plan
        self.benefit = benefit
        self.rate_table = rate_table
        self.benefit_factors = benefit_factors
        self.product_factors = product_factors
        self.age_weight = age_weight

    def calculateBaseRate(self) -> Decimal:
        """
        Calculates the base rate
        """
        return (Decimal(self.benefit.benefit_value) *
                Decimal(self.rate_table.annual_rate_per_unit) /
                Decimal(self.rate_table.unit_value))

    def accumulateFactors(self, factors: List[BenefitFactorModel]) -> Decimal:
        cumulative_factor = 1
        if factors:
            cumulative_product_factor = reduce(
                lambda x, y: x * y, [factor.factor_value for factor in factors])
        return Decimal(cumulative_factor)

    def calculateFinalPremium(
        self,
        base_rate: Decimal,
        cumulative_product_factor: Decimal = 1,
        cumulative_benefit_factor: Decimal = 1
    ) -> Decimal:
        """
        Accumulates all the factors that are passed in.
        Sets the cumululative factors on the benefit rate model.
        Calculates the final premium. 
        """
        return Decimal(base_rate * cumulative_benefit_factor * cumulative_product_factor)

    def returnModel(self) -> BenefitAgeRateModel:
        benefit_age_rate = BenefitAgeRateModel(
            benefit_id=self.benefit.benefit_id,
            plan_id=self.plan.plan_id,
            family_code=self.rate_table.family_code,
            smoker_status=self.rate_table.smoker_status,
            age=self.rate_table.age,
            age_weight=self.age_weight,
            benefit_age_rate_base_premium=self.base_rate,
            benefit_age_rate_product_factor=self.cumulative_product_factor,
            benefit_age_rate_benefit_factor=self.cumulative_benefit_factor,
            benefit_age_rate_final_premium=self.final_premium
        )
        benefit_age_rate.benefit_factors = self.benefit_factors
        return benefit_age_rate

    def calculate(self) -> None:
        """
        Main method for creating a benefit rate model.
        """
        # set base rate
        self.base_rate = self.calculateBaseRate()

        # accumulate factors
        self.cumulative_product_factor = self.accumulateFactors(
            self.product_factors)
        self.cumulative_benefit_factor = self.accumulateFactors(
            self.benefit_factors)

        # calculate final premium
        self.final_premium = self.calculateFinalPremium(
            self.base_rate, self.cumulative_product_factor, self.cumulative_benefit_factor)

        benefit_age_rate = self.returnModel()
        return benefit_age_rate
