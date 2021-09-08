

class FactorAttributes:
    def __init__(self, group, plan, plan_rate, provision=None):
        self._provision = provision
        self._plan_rate = plan_rate
        self._plan = plan
        self._group = group

        self.set(group)
        self.set(plan)
        self.set(plan_rate)
        if provision:
            self.set(provision)

    def set(self, instance):
        for k, v in instance.__dict__.items():
            setattr(self, k, v)
