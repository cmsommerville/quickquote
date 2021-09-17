from decimal import *
from app.extensions import mongo, db

from ...models import BenefitRateModel, BenefitModel, FactorModel, RateTableModel
from ...schemas import BenefitRateSchema
from ..client import ELIGIBLE_FACTORS
from .FactorAttributes import FactorAttributes
from .FactorCalc import FactorCalc

getcontext().prec = 5


benefit_rate_list_schema = BenefitRateSchema(many=True)


class RatingCalculator:

    def __init__(self, plan, provisions, coverages, benefits, plan_rates=None, plan_rating_attributes=None, group=None):
        self._provisions = provisions
        self._plan_rates = plan_rates
        self._plan = plan
        self._coverages = coverages
        self._benefits = benefits
        self._plan_rating_attributes = plan_rating_attributes
        self._group = group

        self._config = self.getProductConfig(plan.product_code)

        self._benefit_rates = []
        self._factors = []

    def getProductConfig(self, product_name):
        config = mongo.db.products.find_one({"name": product_name})
        return config

    def getFactorValue(self, factor_name):
        return next(iter([factor.factor_value for factor in self._factors if factor.factor_name == factor_name]), None)

    def premCalculator(self, benefit_rate):
        return Decimal(benefit_rate.benefit_rate_base_premium) * Decimal(
            benefit_rate.benefit_rate_factor or 1) * Decimal(benefit_rate.benefit_rate_benefit_factor or 1)

    def getBenefitRateConfig(self, benefit_code):
        return [bnft for bnft in self._config['benefits']
                if bnft['name'] == benefit_code][0]['rates']

    def getProvisionConfigDict(self):
        """
        Return provision configuration as a dictionary with 
        provision code as the key and configuration as the value
        """
        # get provision configuration
        provisions_config = self._config.get('provisions')
        return {
            prov['name']: prov for prov in provisions_config
        }

    def _age_band_mapper(self, age_band_object_list):
        return {
            **{age: ab.age_band_id
                for ab in age_band_object_list
                for age in range(ab.lower_age, ab.upper_age + 1)
               }
        }

    def calcBenefitRates(self):
        age_bands_map = self._age_band_mapper(self._plan.age_bands)

        for benefit in self._benefits:
            # get array of benefit rate configuration
            rates = RateTableModel.find_benefit_rateset(
                self._plan.product_code,
                'issue_age',
                benefit.benefit_code
            )

            if benefit.benefit_rates:
                # delete existing benefit rates
                BenefitRateModel.delete_by_benefit_id(
                    benefit.benefit_id, commit=True)

            # initialize benefit_rates array
            benefit_rates = benefit_rate_list_schema.load([{
                "plan_id": self._plan.plan_id,
                "benefit_id": benefit.benefit_id,
                "rate_table_id": rate.rate_table_id,
                "age_band_id": age_bands_map.get(rate.age),
                "benefit_rate_base_premium": Decimal(
                    benefit.benefit_value) * Decimal(rate.annual_rate_per_unit) / Decimal(rate.unit_value),
                "age": rate.age,
                "smoker_status": rate.smoker_status,
                "family_code": rate.family_code
            } for rate in rates
            ])

            benefit.benefit_rates = benefit_rates
            self._benefit_rates.extend(benefit_rates)

    def calcFactors(self):

        plan_id = self._plan.plan_id

        # get provision configuration as a dictionary
        provisions_config_dict = self.getProvisionConfigDict()

        # create a dictionary of all the provisions selected
        factor_dict = {
            provision.provision_code: provision for provision in self._provisions}

        # loop over benefits
        for benefit_rate in self._benefit_rates:

            # loop over each provision/rating attribute in factor_dict
            for factor_name, factor_obj in factor_dict.items():

                factor_config = provisions_config_dict[factor_name].get(
                    'factor')

                factor_attributes = FactorAttributes(
                    plan=self._plan, benefit=benefit_rate.benefit,
                    benefit_rate=benefit_rate, provision=factor_obj)

                # get the setter object and instantiate with factor attributes
                factor_instance = ELIGIBLE_FACTORS[factor_name](
                    factor_attributes, factor_config)

                factor = FactorModel(
                    plan_id=plan_id,
                    provision_id=factor_instance.provision_id,
                    factor_type=factor_instance.factor_type,
                    factor_name=factor_instance.factor_name,
                    factor_selection=factor_instance.factor_selection,
                    factor_selection_type=factor_instance.factor_selection_type,
                    factor_value=factor_instance.factor_value
                )

                if benefit_rate.benefit_rate_factor:
                    benefit_rate.benefit_rate_factor *= factor.factor_value
                else:
                    benefit_rate.benefit_rate_factor = factor.factor_value
                benefit_rate.benefit_rate_final_premium = self.premCalculator(
                    benefit_rate)

                benefit_rate.factors.append(factor)

        BenefitModel.save_all_to_db(self._benefits, plan_id)

    def calcBenefitAgeBandRates(self):
        return BenefitRateModel.agg_benefit_rates_by_age_band(self._plan.plan_id)

    def execute(self):
        try:
            self.calcBenefitRates()
            self.calcFactors()
            return self.calcBenefitAgeBandRates()
        except:
            raise
