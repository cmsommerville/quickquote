from app.rater.base_classes.FactorBase import FactorBase


class FactorPrex(FactorBase):

    def __init__(self, plan_rate):
        factor_type = 'product'
        factor_name = 'prex'
        config = {
            "value": 0.8,
            "variability": [
                {"plan.rating_state": "NC", "value": 0.72,
                 "plan.group.group_size": {"comparison": "lt", "value": 1000}},
                {"plan.rating_state": "NC", "age": {"comparison": "range",
                                                    "lower": 50, "upper": 64}, "value": 0.33},
                {"plan.rating_state": "SC", "age": {
                    "comparison": "ge", 'value': 55}, "value": 0.9},
                {"plan.rating_state": "NC", "age": [
                    45, 46, 47, 48, 49, 50, 51, 52], "value": 0.4}
            ]
        }
        super().__init__(plan_rate, factor_name, factor_type, config)

    def findProvision(self):
        prex = [
            prov for prov in self.plan_rate.plan.provisions if prov.provision_code == self.factor_name]
        if len(prex) > 0:
            return prex[0]
        return None
