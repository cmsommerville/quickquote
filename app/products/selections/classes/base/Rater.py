from decimal import *
from app.extensions import mongo

from ...models import BenefitRateModel, BenefitModel
from ..client import ELIGIBLE_FACTORS
from .FactorAttributes import FactorAttributes
from .FactorCalc import FactorCalc

getcontext().prec = 5


class Rater:

    def __init__(self, plan, provisions, coverages, benefits, plan_rates=None, plan_rating_attributes=None, group=None):
        self._provisions = provisions
        self._plan_rates = plan_rates
        self._plan = plan
        self._coverages = coverages
        self._benefits = benefits
        self._plan_rating_attributes = plan_rating_attributes
        self._group = group

        self._config = self.getProductConfig(plan.product_code)

        self._factors = []

    def getProductConfig(self, product_name):
        return mongo.db.products.find_one({"name": product_name})

    def getFactorValue(self, factor_name):
        return next(iter([factor.factor_value for factor in self._factors if factor.factor_name == factor_name]), None)

    def calcBenefitRates(self):

        for benefit in self._benefits:
            BenefitRateModel.expire_by_benefit(benefit.benefit_id)
            config = [bnft for bnft in self._config['benefits']
                      if bnft['name'] == benefit.benefit_code][0]['rates']

            benefit_rates = [
                BenefitRateModel(
                    plan_id=self._plan.plan_id,
                    benefit_id=benefit.benefit_id,
                    benefit_rate_uuid=benefit_rate_config['uuid'],
                    benefit_rate_base_premium=Decimal(
                        benefit.benefit_value) * Decimal(benefit_rate_config['cc_per_unit']) / Decimal(benefit_rate_config['unit_value']),
                    age=benefit_rate_config['age'],
                    smoker_status=benefit_rate_config['smoker_status'],
                    family_code=benefit_rate_config['family_code']
                )
                for benefit_rate_config in config
            ]
            benefit.benefit_rates = benefit_rates
        BenefitModel.update_all(self._benefits, self._plan.plan_id)

    def calcFactors(self):

        factorList = []
        plan_id = self._plan.plan_id

        # get provision configuration
        provisions_config = self._config.get('provisions', {})

        # create a dictionary of all the provisions selected
        factor_dict = {
            **{provision.provision_code: provision for provision in self._provisions},
            **{rating_attr.plan_rating_attribute_code: rating_attr for rating_attr in self._plan_rating_attributes}
        }

        # loop over plan rates
        for plan_rate in self._plan_rates:

            # loop over each provision/rating attribute in factor_dict
            for factor_name, factor_obj in factor_dict.items():
                # flatten all rating attributes into factor attributes object
                factor_attributes = FactorAttributes(
                    group=self._group, plan=self._plan,
                    plan_rate=plan_rate, provision=factor_obj)

                factor_config = provisions_config.get('factor')

                # get the setter object and instantiate with factor attributes
                factor_instance = ELIGIBLE_FACTORS[factor_name](
                    factor_attributes, factor_config)

                # add factors to a list
                self._factors.append(factor_instance)
