from abc import ABCMeta, abstractmethod
from app.util import deep_getattr


class FactorBase:
    def __init__(self, factor_attributes, factor_name, factor_type, config):
        self.config = config
        self.factor_attributes = factor_attributes
        self.plan_rate_id = factor_attributes.plan_rate_id
        try:
            self.provision_id = factor_attributes.provision_id
        except AttributeError:
            pass
        self.factor_name = factor_name
        self.factor_type = factor_type

        # set value, selection, and selection_type
        self.set(factor_attributes)

    def __repr__(self):
        return f"<Factor: {self.factor_name}>"

    def set(self, factor_attributes):

        val = self.config['default_factor_value']
        uuid = self.config['uuid']
        variability = self.config.get('variability')
        if variability:
            selection, sel_value = self._variabilityHandler(
                variability, factor_attributes, val, uuid)

            self.factor_selection = selection
            self.factor_selection_type = 'uuid'
            self.factor_value = sel_value

        functional = self.config.get('function')
        if functional:
            pass

        return val

    def _variabilityHandler(self, variability, factor_attributes, default_value, default_uuid):

        for item in variability:
            applyRule = True
            for k, v in item.items():
                if k in ['factor_value', '_id', 'uuid']:
                    continue

                attr = deep_getattr(factor_attributes, k)
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
                val = item['factor_value']
                uuid = item.get('uuid')
                return uuid, val

        return default_uuid, default_value

    def _functionalHandler(self):
        return
