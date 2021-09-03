from abc import ABCMeta, abstractmethod
from app.util import deep_getattr


class FactorBase:
    def __init__(self, plan_rate, factor_name, factor_type, config):
        self.config = config
        self.plan_rate = plan_rate
        self.plan_rate_id = plan_rate.plan_rate_id
        self.factor_name = factor_name
        self.factor_type = factor_type
        self.factor_value = self.set(plan_rate)

    def set(self, plan_rate):

        val = self.config['value']
        variability = self.config.get('variability')
        if variability:
            return self._variabilityHandler(variability, plan_rate, val)

        functional = self.config.get('function')
        if functional:
            pass

        return val

    def _variabilityHandler(self, variability, plan_rate, default):

        for item in variability:
            applyRule = True
            for k, v in item.items():
                if k in ['value', '_id']:
                    continue

                attr = deep_getattr(plan_rate, k)
                if type(v) == list:
                    applyRule = (attr in v) and applyRule
                elif type(v) == dict:
                    if v['comparison'] == "range":
                        applyRule = (attr >= v['lower'] and
                                     attr <= v['upper'] and
                                     applyRule)

                    elif v['comparison'] == "nlist":
                        applyRule = attr in v['value'] and applyRule
                    if v['comparison'] == "nrange":
                        applyRule = not (attr >= v['lower'] and
                                         attr <= v['upper']) and applyRule
                    elif v['comparison'] == 'lt':
                        applyRule = attr < v['value'] and applyRule
                    elif v['comparison'] == 'le':
                        applyRule = attr <= v['value'] and applyRule
                    elif v['comparison'] == 'gt':
                        applyRule = attr > v['value'] and applyRule
                    elif v['comparison'] == 'ge':
                        applyRule = attr >= v['value'] and applyRule
                else:
                    applyRule = (attr == v) and applyRule

            if applyRule:
                val = item['value']
                return val
        return default

    def _functionalHandler(self):
        return
