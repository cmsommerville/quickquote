from typing import List
from decimal import Decimal
from functools import reduce
from collections import defaultdict

from app.products.selections.models.Model_SelectionBenefitAgeRate import Model_SelectionBenefitAgeRate

from ..models import Model_SelectionPlan, Model_SelectionBenefit, Model_SelectionAgeBands,\
    RateTableModel, Model_SelectionBenefitRate, Model_SelectionBenefitFactor, \
    Model_SelectionProvision, Model_SelectionBenefitAgeRate
from .Rating_BenefitFactors import Rating_BenefitFactorList


class Rating_BenefitAgeRates:

    def __init__(
            self,
            plan: Model_SelectionPlan,
            benefit: Model_SelectionBenefit,
            rate_table: RateTableModel,
            factors: List[Model_SelectionBenefitFactor],
            weights: dict = {},
            *args, **kwargs):
        self.plan = plan
        self.benefit = benefit
        self.rate_table = rate_table
        self.factors = factors
        self.weights = weights

    def calculateBaseRate(self) -> Decimal:
        """
        Calculates the base rate
        """
        return (Decimal(self.benefit.benefit_value) *
                Decimal(self.rate_table.annual_rate_per_unit) /
                Decimal(self.rate_table.unit_value))

    def accumulateFactors(self, factors: List[Model_SelectionBenefitFactor]) -> Decimal:
        cumulative_factor = 1
        if factors:
            cumulative_product_factor = reduce(
                lambda x, y: x * y, [factor.factor_value for factor in factors])
        return Decimal(cumulative_factor)

    def calculateFinalPremium(
        self,
        base_rate: Decimal,
        cumulative_provision_factor: Decimal = 1,
        discretionary_factor: Decimal = 1
    ) -> Decimal:
        """
        Accumulates all the factors that are passed in.
        Sets the cumululative factors on the benefit rate model.
        Calculates the final premium. 
        """
        return Decimal(base_rate * cumulative_provision_factor * discretionary_factor)

    def return_model(self) -> Model_SelectionBenefitAgeRate:
        weight_key = (
            self.rate_table.age, 
            self.rate_table.smoker_status, 
            self.rate_table.gender, )

        benefit_age_rate = Model_SelectionBenefitAgeRate(
            selection_benefit_id=self.benefit.selection_benefit_id,
            selection_plan_id=self.plan.selection_plan_id,
            family_code=self.rate_table.family_code,
            smoker_status=self.rate_table.smoker_status,
            gender=self.rate_table.gender, 
            age=self.rate_table.age,
            weight=self.weights.get(weight_key, 0),
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
        self.cumulative_factor = self.accumulateFactors(
            self.factors)

        # calculate final premium
        self.final_premium = self.calculateFinalPremium(
            self.base_rate, self.cumulative_factor)

        benefit_age_rate = self.returnModel()
        return benefit_age_rate
