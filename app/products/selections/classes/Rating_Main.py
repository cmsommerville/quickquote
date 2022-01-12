import os
from typing import List
from decimal import Decimal
from functools import reduce
from collections import defaultdict


from ..models import Model_SelectionPlan, Model_SelectionBenefit, Model_SelectionAgeBands, \
    RateTableModel, Model_SelectionBenefitRate, Model_SelectionBenefitFactor, \
    Model_SelectionProvision, Model_SelectionBenefitAgeRate, \
    Model_SelectionRateGroupSummary
from .Rating_BenefitAgeRates import Rating_BenefitAgeRates
from .Rating_BenefitRates import Rating_BenefitRates
from .Rating_PlanRates import Rating_PlanRates
from .Rating_BenefitFactors import Rating_BenefitFactorList
from .Rating_BenefitAgeRateWeights import Rating_BenefitAgeRateWeights


class Rating_Main:

    def __init__(self, 
        plan: Model_SelectionPlan, 
        weights: list = None, 
        *args, **kwargs):

        self.plan = plan
        self.benefits = plan.benefits
        self.age_bands = plan.age_bands
        self.provisions = plan.provisions
        self.product_id = plan.config_product_id
        self.product_variation = plan.product_variation
        self.product_variation_id = plan.config_product_variation_id
        
        self.product_code = plan.product.product_code
        self.product_variation_code = plan.product_variation.product_variation_code

        self.weights = Rating_BenefitAgeRateWeights(plan, weights)

        self.rate_groups = []
        # a dictionary keyed by the benefit_rates natural key, containing a list of benefit_age_rates
        self._benefit_age_rates_dict = defaultdict(list)
        # a dictionary keyed by the plan_rates natural key, containing a list of benefit_rates
        self._benefit_rates_dict = defaultdict(list)
        # a dictionary keyed by the benefit_code, containing the corresponding benefit object
        self._benefits_dict = {
            bnft.config_benefit.benefit_code: bnft for bnft in self.benefits}
        # a dictionary keyed by every distinct age, with each age containing its corresponding age band object
        self._age_band_dict = self.defineAgeBandDictionary()
        self.rate_table = self.initRateTables()
        # self.age_distribution = self.initAgeDistribution()

    def initRateTables(self) -> List[RateTableModel]:
        return RateTableModel.find_many_benefit_ratesets(
            self.product_code,
            self.product_variation_code,
            [bnft.config_benefit.benefit_code for bnft in self.benefits]
        )

    def defineAgeBandDictionary(self):
        return {
            age: age_band
            for age_band in self.age_bands
            for age in range(age_band.lower_age, age_band.upper_age + 1)
        }

    def calcBenefitAgeRates(self) -> None:
        """
        Rates from the rate table are the basis of the calculation.
        Loop over them, calculating factors first, then the benefit
        age rates. 

        Append the benefit age rate objects into a dictionary with
        BenefitRate (not BenefitAgeRate) natural keys
        """

        # expire the old benefit age rate and factor records
        Model_SelectionBenefitFactor.delete_by_plan(self.plan.selection_plan_id)
        Model_SelectionBenefitAgeRate.delete_by_plan(self.plan.selection_plan_id)

        for rate in self.rate_table:
            # look up age band
            age_band = self._age_band_dict.get(rate.age)
            if not age_band:
                continue

            # calculate the benefit factors for this rate key
            factors = Rating_BenefitFactorList(
                config=self.config['provisions'],
                plan=self.plan,
                benefit=self._benefits_dict[rate.benefit_code],
                rate_table=rate,
                provisions=self.provisions
            ).calculate()

            # get age weight 
            weight = self.weights.get(age=rate.age, smoker_status=rate.smoker_status, gender=rate.gender)

            # create the benefit age rate
            benefit_age_rate = Rating_BenefitAgeRates(
                plan=self.plan,
                benefit=self._benefits_dict[rate.benefit_code],
                rate_table=rate,
                factors=factors,
                weight=weight
            ).calculate()

            # a list of the rate table natural key, but by AGE BAND
            age_band_rate_key = [rate.product_code, rate.product_variation_code, age_band.age_band_id,
                                 rate.family_code, rate.benefit_code]

            age_band.rate_key.append(rate.smoker_status if self.plan.is_smoker_distinct else 'U')                     
            age_band.rate_key.append(rate.gender if self.plan.is_gender_distinct else 'U')                     

            self._benefit_age_rates_dict[tuple(age_band_rate_key)].append(benefit_age_rate)

    def calcBenefitRates(self) -> None:
        """
        Calculate the benefit rates. 
        """

        # expire the old benefit rate records
        Model_SelectionBenefitRate.delete_by_plan(self.plan.selection_plan_id)

        for age_band_rate_key, benefit_age_rates in self._benefit_age_rates_dict.items():
            # unpack the age_band_rate_key tuple

            (product_code, product_variation_code, age_band_id,
                family_code, benefit_code, smoker_status, gender) = age_band_rate_key

            # build the benefit rate object
            benefit_rate = Rating_BenefitRates(
                plan=self.plan,
                benefit=self._benefits_dict[benefit_code],
                benefit_age_rates=benefit_age_rates,
                age_band_id=age_band_id,
                family_code=family_code,
                smoker_status=smoker_status,
                benefit_code=benefit_code, 
                gender=gender
            ).calculate()

            # lookup the plan rate code
            rate_group_id = self._benefits_dict[benefit_code].config_rate_group_id

            # create plan rate key by removing benefit code and adding plan rate code
            rate_group_key = (product_code, product_variation_code, age_band_id,
                             family_code, smoker_status, gender, rate_group_id)

            self._benefit_rates_dict[rate_group_key].append(benefit_rate)

    def calcRateGroups(self) -> None:
        """
        Calculate the rate group rates
        """

        # expire the old plan rate records
        Model_SelectionRateGroupSummary.delete_by_plan(self.plan.selection_plan_id)

        for plan_rate_key, benefit_rates in self._benefit_rates_dict.items():
            (product_code, product_variation_code, age_band_id,
             family_code, smoker_status, gender, rate_group_id) = plan_rate_key

            plan_rate = Rating_PlanRates(
                plan=self.plan,
                benefit_rates=benefit_rates,
                age_band_id=age_band_id,
                family_code=family_code,
                smoker_status=smoker_status,
                gender=gender, 
                rate_group_id=rate_group_id
            ).calculate()

            self.rate_groups.append(plan_rate)

    def calculate(self) -> None:
        # calculate benefit age rates and benefit factors
        self.calcBenefitAgeRates()
        # calculate benefit rates
        self.calcBenefitRates()
        # calculate plan rates
        self.calcRateGroups()

        Model_SelectionRateGroupSummary.save_all_to_db(self.rate_groups)
        return self.rate_groups
