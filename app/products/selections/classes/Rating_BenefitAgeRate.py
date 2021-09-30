from typing import List
from decimal import Decimal
from functools import reduce
from collections import defaultdict

from ..models import PlanModel, BenefitModel, AgeBandsModel,\
    RateTableModel, BenefitRateModel, BenefitFactorModel, \
    ProvisionModel, BenefitAgeRateModel
from .Rating_BenefitFactorsCalculator import BenefitFactorsCalculator


class BenefitAgeRate:

    def __init__(
            self,
            plan: PlanModel,
            plan_config: dict,
            benefit: BenefitModel,
            age_band: AgeBandsModel,
            rate_table: RateTableModel,
            provisions: List[ProvisionModel],
            age_weight: float = 1,
            *args, **kwargs):
        self.plan = plan
        self.plan_config = plan_config
        self.benefit = benefit
        self.rate_table = rate_table
        self.age_band = age_band
        self.provisions = provisions
        self.age_weight = age_weight

    def calculateBaseRate(self) -> Decimal:
        """
        Calculates the base rate
        """
        return (Decimal(self.benefit.benefit_value) *
                Decimal(self.rate_table.annual_rate_per_unit) /
                Decimal(self.rate_table.unit_value))

    def calculateBenefitFactors(self) -> List[BenefitFactorModel]:
        benefit_factors = BenefitFactorsCalculator(
            config=self.plan_config['provisions'],
            plan=self.plan,
            benefit=self.benefit,
            rate_table=self.rate_table,
            provisions=self.provisions
        )

        return benefit_factors.calculate()

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

    def returnBenefitAgeRateModel(self) -> BenefitAgeRateModel:
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
        benefit_age_rate.benefit_factors.extend(self.benefit_factors)
        return benefit_age_rate

    def calculate(self) -> None:
        """
        Main method for creating a benefit rate model.
        """
        # set base rate
        self.base_rate = self.calculateBaseRate()
        # calculate array of product factors
        self.product_factors = []
        # calculate benefit factors
        self.benefit_factors = self.calculateBenefitFactors()

        # accumulate factors
        self.cumulative_product_factor = self.accumulateFactors(
            self.product_factors)
        self.cumulative_benefit_factor = self.accumulateFactors(
            self.benefit_factors)

        # calculate final premium
        self.final_premium = self.calculateFinalPremium(
            self.base_rate, self.cumulative_product_factor, self.cumulative_benefit_factor)
