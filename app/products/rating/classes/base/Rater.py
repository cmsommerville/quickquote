from app.extensions import mongo

from ..client import ELIGIBLE_FACTORS
from .FactorAttributes import FactorAttributes
from .FactorCalc import FactorCalc


class Rater:

    def __init__(self, plan, plan_rates, provisions, coverages, benefits, plan_rating_attributes=None, group=None):
        self._provisions = provisions
        self._plan_rates = plan_rates
        self._plan = plan
        self._coverages = coverages
        self._benefits = benefits
        self._plan_rating_attributes = plan_rating_attributes
        self._group = group

        self._config = self.getProductConfig(plan.product_name)

        self._factors = []

    def getProductConfig(self, product_name):
        return mongo.db.products.find_one({"name": product_name})

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
