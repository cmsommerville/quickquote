import os
from typing import List
from decimal import Decimal
from functools import reduce
from app.shared import list_to_dict
from collections import defaultdict

from ...models import PlanModel, BenefitModel, AgeBandsModel, RateTableModel, \
    BenefitRateModel, FactorModel, ProvisionModel
from .BenefitAgeRate import BenefitAgeRate
from .Rating_ProductFactorsCalculator import ProductFactorsCalculator

PRODUCT_CODE = 'critical_illness'
PRODUCT_VARIATION_CODE = 'issue_age'
RATE_ROUNDING_PRECISION = os.getenv("RATE_ROUNDING_PRECISION", 5)


class Rating_PremiumCalculator:

    def __init__(
            self,
            plan: PlanModel,
            benefits: List[BenefitModel],
            age_bands: List[AgeBandsModel],
            provisions: List[ProvisionModel],
            plan_config: dict,
            *args, **kwargs):
        self.plan = plan
        self.benefits = benefits
        self.age_bands = age_bands
        self.provisions = provisions
        self.plan_config = plan_config
        self.age_distribution = {}

        self.benefit_rates = []
        self.factors = []

    def getRateTables(self) -> None:
        """
        Get rate tables for each benefit from the database. 
        """
        self.rate_tables = RateTableModel.find_many_benefit_ratesets(
            PRODUCT_CODE, PRODUCT_VARIATION_CODE, [bnft.benefit_code for bnft in self.benefits])

    def getAgeDistribution(self) -> None:
        self.age_distribution = {}

    def assignRatesToAgeBands(self) -> dict:
        """
        Create a dictionary that assigns rate tables to age bands
        The key is a tuple of (lower_age, upper_age)
        """
        age_band_rates = defaultdict(list)
        benefits_dict = {bnft.benefit_code: bnft for bnft in self.benefits}
        # loop over rates
        for rate in self.rate_tables:
            # loop over age bands
            for band in self.age_bands:
                age_band_nk = (rate.product_code, rate.product_variation_code, rate.benefit_code,
                               rate.family_code, rate.smoker_status, band.lower_age, band.upper_age)
                # if rate age is in age band, append
                if (rate.age >= band.lower_age) and (rate.age <= band.upper_age):
                    age_band_rates[age_band_nk].append({
                        "rate_table": rate,
                        "benefit": benefits_dict[rate.benefit_code],
                        "age_band": band
                    })
        return age_band_rates

    def weightedAverageAgeBandRates(self, benefit_age_rates: List[BenefitAgeRate]):
        denom = 0
        prem = 0
        for rate in benefit_age_rates:
            prem += rate.age_weight * rate.final_premium
            denom += rate.age_weight
        return Decimal(round(prem / denom, RATE_ROUNDING_PRECISION)) if denom > 0 else 0

    def calculateBenefitRates(self) -> None:
        age_band_rates = self.assignRatesToAgeBands()

        # loop over rate keys to get list of rates/benefits belonging to an age band
        for rate_key, rate_data_list in age_band_rates.items():
            benefit_age_rate_list = []
            # within each age band, loop over each rate to create benefit_rate object
            for rate_data in rate_data_list:
                # unpack data from rate_data dictionary
                benefit = rate_data['benefit']
                rate_table = rate_data['rate_table']
                age_band = rate_data['age_band']
                age_weight = self.age_distribution.get(rate_table.age, 1)

                # create benefit_age_rate object
                benefit_age_rate = BenefitAgeRate(
                    plan=self.plan,
                    plan_config=self.plan_config,
                    benefit=benefit,
                    age_band=age_band,
                    rate_table=rate_table,
                    provisions=self.provisions,
                    age_weight=age_weight
                )
                # calculate final premium and factors
                benefit_age_rate.calculate()
                benefit_age_rate_list.append(benefit_age_rate)

            # calculate weighted average final premium per age band
            final_premium = self.weightedAverageAgeBandRates(
                benefit_age_rate_list)

            # create benefit rate
            benefit_rate = BenefitRateModel(
                benefit_id=benefit.benefit_id,
                plan_id=self.plan.plan_id,
                age_band_id=age_band.age_band_id,
                family_code=rate_table.family_code,
                smoker_status=rate_table.smoker_status,
                benefit_rate_premium=final_premium
            )
            # self.factors.extend(benefit_rate.factors)
            self.benefit_rates.append(benefit_rate)

    def calculate(self) -> None:
        # get the rate table data
        self.getRateTables()
        # instantiate the benefit_rate models with final premiums
        self.calculateBenefitRates()

        BenefitRateModel.save_all_to_db(self.benefit_rates)
        FactorModel.save_all_to_db(self.factors)

        return(self.benefit_rates)
