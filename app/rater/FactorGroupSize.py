from app.rater.base_classes.FactorBase import FactorBase
from app.models import mongo


class FactorGroupSize(FactorBase):

    def __init__(self, plan_rate, config):
        factor_type = 'product'
        factor_name = 'groupsize'
        super().__init__(plan_rate, factor_name, factor_type, config)

    def __repr__(self):
        return f"<Factor: {self.factor_name} - Plan Rate ID: {self.plan_rate.plan_rate_id}>"
