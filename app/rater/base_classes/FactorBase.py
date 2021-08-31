from abc import ABCMeta, abstractmethod


class FactorBase(object, metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, plan, factor_name, factor_type):
        self.plan = plan
        self.plan_id = plan.plan_id
        self.factor_name = factor_name
        self.factor_type = factor_type
        self.factor_selection, self.factor_value = self.set()

    @abstractmethod
    def set(self):
        pass
