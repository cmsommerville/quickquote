from decimal import *
from app.extensions import mongo, db
import datetime

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
        self.plan_id = plan.plan_id
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

    def getProvisionDict(self):
        """
        Return provision configuration and selections as a dictionary with 
        provision code as the key and configuration as the value
        """
        # get provision configuration
        provisions_config = self._config.get('provisions')
        provision_config_dict = {prov['name']: prov for prov in provisions_config}

        return {
            provision.provision_code: {
                "config": provision_config_dict[provision.provision_code],
                "selection": provision
            }
            for provision in self._provisions
        }

    def _age_band_mapper(self, age_band_object_list):
        return {
            **{age: ab.age_band_id
                for ab in age_band_object_list
                for age in range(ab.lower_age, ab.upper_age + 1)
               }
        }

    def calculator(self):

        age_bands_map = self._age_band_mapper(self._plan.age_bands)
        provision_dict = self.getProvisionDict()

        for benefit in self._benefits:
            # get array of benefit rate configuration
            rates = RateTableModel.find_benefit_rateset(
                self._plan.product_code,
                'issue_age',
                benefit.benefit_code
            )

            for rate in rates:

                # initialize benefit_rates array
                benefit_rate = BenefitRateModel(**{
                    "plan_id": self.plan_id,
                    "benefit_id": benefit.benefit_id,
                    "rate_table_id": rate.rate_table_id,
                    "age_band_id": age_bands_map.get(rate.age),
                    "benefit_rate_base_premium": Decimal(
                        benefit.benefit_value) * Decimal(rate.annual_rate_per_unit) / Decimal(rate.unit_value),
                    "age": rate.age,
                    "smoker_status": rate.smoker_status,
                    "family_code": rate.family_code,
                    "benefit_rate_factor": 1
                })

                benefit.benefit_rates.append(benefit_rate)

                # calculate factors
                for prov_name, provision in provision_dict.items():
                    # print(provision)
                    factor = self.factorSetter(benefit_rate, provision)

                    benefit_rate.benefit_rate_factor *= factor.factor_value
                    benefit_rate.factors.append(factor)
                    self._factors.append(factor)

                benefit_rate.benefit_rate_final_premium = self.premCalculator(
                    benefit_rate)

                self._benefit_rates.append(benefit_rate)

            BenefitModel.save_all_to_db(self._benefits, self.plan_id)

    def factorSetter(self, benefit_rate, provisions_dict):
        """
        Returns a factor model object, given a benefit rate object and
        a dictionary containing: 
        - config (dict): a provision configuration dictionary
        - selection (object): a provision model object containing the 
            provision selections 
        """
        provision_code = provisions_dict['selection'].provision_code

        # configuration
        factor_config = provisions_dict['config'].get(
            'factor')

        # attribute object
        factor_attributes = FactorAttributes(
            plan=self._plan, benefit=benefit_rate.benefit,
            benefit_rate=benefit_rate, provision=provisions_dict['selection'])

        # get the setter object and instantiate with factor attributes
        factor_instance = ELIGIBLE_FACTORS[provision_code](
            factor_attributes, factor_config)

        factor = FactorModel(
            plan_id=factor_attributes.plan_id,
            provision_id=factor_instance.provision_id,
            factor_type=factor_instance.factor_type,
            factor_name=factor_instance.factor_name,
            factor_selection=factor_instance.factor_selection,
            factor_selection_type=factor_instance.factor_selection_type,
            factor_value=factor_instance.factor_value
        )

        return factor

    def calcBenefitAgeBandRates(self):
        return BenefitRateModel.agg_benefit_rates_by_age_band(self.plan_id)

    def execute(self):
        try:
            print(datetime.datetime.now())
            BenefitRateModel.delete_by_plan_id(self.plan_id)
            print(datetime.datetime.now())

            self.calculator()
            print(datetime.datetime.now())
            return self.calcBenefitAgeBandRates()
        except:
            raise
