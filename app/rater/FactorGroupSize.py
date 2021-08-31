from app.rater.base_classes.FactorBase import FactorBase


class FactorGroupSize(FactorBase):

    def __init__(self, plan):
        factor_type = 'product'
        factor_name = 'groupsize'
        super().__init__(plan, factor_name, factor_type)

    def set(self):
        groupsize = self.plan.group.group_size
        if groupsize < 1000:
            return '<1000', 1
        else:
            return '1000+', 0.8
