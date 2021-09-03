from app.rater.base_classes.FactorBase import FactorBase


class FactorPrex(FactorBase):

    def __init__(self, plan_rate):
        factor_type = 'product'
        factor_name = 'prex'
        super().__init__(plan_rate, factor_name, factor_type)

    def findProvision(self):
        prex = [
            prov for prov in self.plan_rate.plan.provisions if prov.provision_code == self.factor_name]
        if len(prex) > 0:
            return prex[0]
        return None

    def set(self):
        prex = self.findProvision()
        if prex is None:
            return 1

        if prex.getValue() == "12/12":
            return "12/12",  0.9
        else:
            return "Other", 1
