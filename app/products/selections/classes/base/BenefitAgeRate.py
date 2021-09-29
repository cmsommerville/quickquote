from typing import List
from decimal import Decimal
from functools import reduce
from collections import defaultdict

from ...models import PlanModel, BenefitModel, AgeBandsModel, RateTableModel, BenefitRateModel, FactorModel, ProvisionModel
from .Rating_ProductFactorsCalculator import ProductFactorsCalculator


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

    def calculateProductFactors(self):
        product_factors = ProductFactorsCalculator(
            config=self.plan_config['provisions'],
            plan=self.plan,
            benefit=self.benefit,
            rate_table=self.rate_table,
            provisions=self.provisions
        )
        self.factors = product_factors.calculate()
        return self.factors

    def calculateFinalPremium(
        self,
        base_rate: Decimal,
        product_factors: List[FactorModel],
        benefit_factors: list = []
    ) -> None:
        """
        Accumulates all the factors that are passed in.
        Sets the cumululative factors on the benefit rate model.
        Calculates the final premium. 
        """
        cumulative_product_factor = 1
        cumulative_benefit_factor = 1

        # calculate cumulative factor
        if product_factors:
            cumulative_product_factor = reduce(
                lambda x, y: x * y, [factor.factor_value for factor in product_factors])

        # calculate cumulative factor
        if benefit_factors:
            cumulative_benefit_factor = reduce(
                lambda x, y: x * y, [factor.factor_value for factor in benefit_factors])

        # calculate the final premium
        return Decimal(base_rate * cumulative_benefit_factor * cumulative_product_factor)

    def calculate(self):
        """
        Main method for creating a benefit rate model.
        """
        # set base rate
        self.base_rate = self.calculateBaseRate()
        # calculate array of product factors
        self.product_factors = self.calculateProductFactors()
        # calculate benefit factors
        self.benefit_factors = []
        # calculate final premium
        self.final_premium = self.calculateFinalPremium(
            self.base_rate, self.product_factors, self.benefit_factors)
