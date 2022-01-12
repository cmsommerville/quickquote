from typing import List
from decimal import Decimal
from functools import reduce
from collections import defaultdict

from app.products.selections.models.Model_SelectionBenefitAgeRate import Model_SelectionBenefitAgeRate

from ..models import Model_SelectionPlan, Model_SelectionBenefit, Model_SelectionAgeBands,\
    RateTableModel, Model_SelectionBenefitRate, Model_SelectionBenefitFactor, \
    Model_SelectionProvision, Model_SelectionBenefitAgeRate
from .Rating_BenefitAgeRateWeights import Rating_BenefitAgeRateWeights
from .Rating_BenefitFactors import Rating_BenefitFactorList


class Rating_BenefitAgeRates:

    def __init__(
            self,
            plan: Model_SelectionPlan,
            benefit: Model_SelectionBenefit,
            rate_table: RateTableModel,
            provision_factors: List[Model_SelectionBenefitFactor],
            weight: Decimal = 0,
            *args, **kwargs):
        self.plan = plan
        self.benefit = benefit
        self.rate_table = rate_table
        self.provision_factors = provision_factors
        self.weight = weight
        self.discretionary_factor = kwargs.get('discretionary_factor', 1)
        self.durations = self.benefit.durations or None


    def calculateBaseRate(self) -> Decimal:
        """
        Calculates the base rate
        """
        return (Decimal(self.benefit.benefit_value) *
                Decimal(self.rate_table.annual_rate_per_unit) /
                Decimal(self.rate_table.unit_value))

    def accumulateDurationalFactors(self):
        cumulative_factor = 1
        if self.durations:
            cumulative_factor = reduce(
                lambda x, y: x * y, [dur.duration_factor for dur in self.durations])
        return Decimal(cumulative_factor) 

    def accumulateFactors(self, factors: List[Model_SelectionBenefitFactor]) -> Decimal:
        cumulative_factor = 1
        if factors:
            cumulative_factor = reduce(
                lambda x, y: x * y, [factor.factor_value for factor in factors])
        return Decimal(cumulative_factor)

    def calculateFinalPremium(
        self,
        base_rate: Decimal,
        cumulative_provision_factor: Decimal = 1,
        cumulative_duration_factor: Decimal = 1, 
        discretionary_factor: Decimal = 1
    ) -> Decimal:
        """
        Accumulates all the factors that are passed in.
        Sets the cumululative factors on the benefit rate model.
        Calculates the final premium. 
        """
        return Decimal(base_rate * cumulative_provision_factor * 
            cumulative_duration_factor * discretionary_factor)

    def return_model(self) -> Model_SelectionBenefitAgeRate:

        benefit_age_rate = Model_SelectionBenefitAgeRate(
            selection_benefit_id=self.benefit.selection_benefit_id,
            selection_plan_id=self.plan.selection_plan_id,
            family_code=self.rate_table.family_code,
            smoker_status=self.rate_table.smoker_status,
            gender=self.rate_table.gender, 
            age=self.rate_table.age,
            weight=self.weight or 0, 
            base_premium=self.base_rate,
            provision_factor=self.provision_factor,
            duration_factor=self.duration_factor,
            discretionary_factor=self.discretionary_factor, 
            final_premium=self.final_premium
        )
        benefit_age_rate.provision_factors = self.provision_factors
        return benefit_age_rate

    def calculate(self) -> None:
        """
        Main method for creating a benefit rate model.
        """
        # set base rate
        self.base_rate = self.calculateBaseRate()

        # accumulate provision factors
        self.provision_factor = self.accumulateFactors(self.provision_factors)

        # accumulate provision factors
        self.duration_factor = self.accumulateDurationalFactors()

        # calculate final premium
        self.final_premium = self.calculateFinalPremium(
            self.base_rate, 
            self.provision_factor, 
            self.duration_factor, 
            self.discretionary_factor
        )

        return self.return_model()
