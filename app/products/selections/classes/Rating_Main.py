import os
from typing import List
from decimal import Decimal
from functools import reduce
from collections import defaultdict

from ..models import PlanModel, BenefitModel, AgeBandsModel, RateTableModel, \
    BenefitRateModel, BenefitFactorModel, ProvisionModel, BenefitAgeRateModel, \
    PlanRateModel
from .Rating_BenefitAgeRates import Rating_BenefitAgeRates
from .Rating_BenefitRates import Rating_BenefitRates
from .Rating_PlanRates import Rating_PlanRates
from .Rating_BenefitFactors import Rating_BenefitFactorList


class Rating_Main:

    def __init__(self, plan, benefits, age_bands, provisions,
                 config, product_code, product_variation_code, *args, **kwargs):

        self.plan = plan
        self.benefits = benefits
        self.age_bands = age_bands
        self.provisions = provisions
        self.config = config
        self.product_code = product_code
        self.product_variation_code = product_variation_code

        self.plan_rates = []
        # a dictionary keyed by the benefit_rates natural key, containing a list of benefit_age_rates
        self._benefit_age_rates_dict = defaultdict(list)
        # a dictionary keyed by the plan_rates natural key, containing a list of benefit_rates
        self._benefit_rates_dict = defaultdict(list)
        # a dictionary keyed by the benefit_code, containing the corresponding benefit object
        self._benefits_dict = {
            bnft.benefit_code: bnft for bnft in self.benefits}
        # a dictionary keyed by every distinct age, with each age containing its corresponding age band object
        self._age_band_dict = self.defineAgeBandDictionary()
        self.rate_table = self.initRateTables()
        self.age_distribution = self.initAgeDistribution()

    def initRateTables(self) -> List[RateTableModel]:
        return RateTableModel.find_many_benefit_ratesets(
            self.product_code,
            self.product_variation_code,
            [*self._benefits_dict.keys()]
        )

    def initAgeDistribution(self) -> dict:
        return {age: 1 for age in range(0, 100)}

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
        BenefitFactorModel.delete_by_plan_id(self.plan.plan_id)
        BenefitAgeRateModel.delete_by_plan_id(self.plan.plan_id)

        for rate in self.rate_table:
            # look up age band
            age_band = self._age_band_dict[rate.age]

            # make a tuple of the rate table natural key, but by AGE BAND
            # not keyed by age
            age_band_rate_key = (rate.product_code, rate.product_variation_code, age_band.age_band_id,
                                 rate.family_code, rate.smoker_status, rate.benefit_code)

            # calculate the benefit factors for this rate key
            benefit_factors = Rating_BenefitFactorList(
                config=self.config['provisions'],
                plan=self.plan,
                benefit=self._benefits_dict[rate.benefit_code],
                rate_table=rate,
                provisions=self.provisions
            ).calculate()

            benefit_age_rate = Rating_BenefitAgeRates(
                plan=self.plan,
                benefit=self._benefits_dict[rate.benefit_code],
                rate_table=rate,
                benefit_factors=benefit_factors,
                product_factors=[],
                age_weight=self.age_distribution[rate.age]
            ).calculate()

            self._benefit_age_rates_dict[age_band_rate_key].append(
                benefit_age_rate)

    def calcBenefitRates(self) -> None:
        """
        Calculate the benefit rates. 
        """

        # expire the old benefit rate records
        BenefitRateModel.delete_by_plan_id(self.plan.plan_id)

        for age_band_rate_key, benefit_age_rates in self._benefit_age_rates_dict.items():
            # unpack the age_band_rate_key tuple
            (product_code, product_variation_code, age_band_id,
                family_code, smoker_status, benefit_code) = age_band_rate_key

            # build the benefit rate object
            benefit_rate = Rating_BenefitRates(
                plan=self.plan,
                benefit=self._benefits_dict[benefit_code],
                benefit_age_rates=benefit_age_rates,
                age_band_id=age_band_id,
                family_code=family_code,
                smoker_status=smoker_status,
                benefit_code=benefit_code
            ).calculate()

            # lookup the plan rate code
            plan_rate_code = self._benefits_dict[benefit_code].plan_rate_code

            # create plan rate key by removing benefit code and adding plan rate code
            plan_rate_key = (product_code, product_variation_code, age_band_id,
                             family_code, smoker_status, plan_rate_code)

            self._benefit_rates_dict[plan_rate_key].append(benefit_rate)

    def calcPlanRates(self) -> None:
        """
        Calculate the plan rates
        """

        # expire the old plan rate records
        PlanRateModel.delete_by_plan_id(self.plan.plan_id)

        for plan_rate_key, benefit_rates in self._benefit_rates_dict.items():
            (product_code, product_variation_code, age_band_id,
             family_code, smoker_status, plan_rate_code) = plan_rate_key

            plan_rate = Rating_PlanRates(
                plan=self.plan,
                benefit_rates=benefit_rates,
                age_band_id=age_band_id,
                family_code=family_code,
                smoker_status=smoker_status,
                plan_rate_code=plan_rate_code
            ).calculate()

            self.plan_rates.append(plan_rate)

    def calculate(self) -> None:
        # calculate benefit age rates and benefit factors
        self.calcBenefitAgeRates()
        # calculate benefit rates
        self.calcBenefitRates()
        # calculate plan rates
        self.calcPlanRates()

        PlanRateModel.save_all_to_db(self.plan_rates)
        return self.plan_rates
