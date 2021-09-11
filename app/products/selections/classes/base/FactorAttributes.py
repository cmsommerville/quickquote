

class FactorAttributes:
    def __init__(self, plan, benefit, benefit_rate, provision):
        self._provision = provision
        self._benefit = benefit
        self._benefit_rate = benefit_rate
        self._plan = plan

        self.set(plan)
        self.set(benefit)
        self.set(benefit_rate)
        self.set(provision)

    def set(self, instance):
        for k, v in instance.__dict__.items():
            setattr(self, k, v)
