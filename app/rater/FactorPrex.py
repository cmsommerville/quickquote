from app.rater.base_classes.FactorBase import FactorBase


class FactorPrex(FactorBase):

    def __init__(self, plan_rate, config):
        factor_type = 'product'
        factor_name = 'prex'
        super().__init__(plan_rate, factor_name, factor_type, config)

    def findProvision(self):
        prex = [
            prov for prov in self.plan_rate.plan.provisions if prov.provision_code == self.factor_name]
        if len(prex) > 0:
            return prex[0]
        return None
