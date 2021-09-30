from typing import List, Union, Tuple
from decimal import Decimal
from ..models import BenefitFactorModel, PlanModel, BenefitModel, RateTableModel, ProvisionModel


class BenefitFactorsCalculator:

    def __init__(self,
                 config: dict,
                 plan: PlanModel,
                 benefit: BenefitModel,
                 rate_table: RateTableModel,
                 provisions: List[ProvisionModel]
                 ):

        self.config = config
        self.plan = plan
        self.benefit = benefit
        self.rate_table = rate_table
        self.provisions = provisions
        self.benefit_factors = []

        self.factor_data = self._factor_config_formatter()

    def _factor_config_formatter(self) -> dict:
        """
        Combine configuration and selections into a single dictionary. 
        Configuration under the `config` key.
        Selections under the `selection` key. 
        """
        config = {fctr['name']: fctr for fctr in self.config}
        try:
            output = {
                prov.provision_code: {
                    'config': config[prov.provision_code],
                    'selection': prov
                }
                for prov in self.provisions
            }
        except Exception as e:
            raise
        return output

    def calculate(self) -> List[BenefitFactorModel]:
        """
        Loop over all the factor data and create factor objects.
        """

        for name, data in self.factor_data.items():
            # this instantiates a benefit factor object
            factor_calc = BenefitFactor(
                factor_name=name,
                factor_type="benefit",
                factor_config=data['config'],
                plan=self.plan,
                benefit=self.benefit,
                rate_table=self.rate_table,
                provision=data['selection']
            )

            # this outputs a database benefit factor model
            factor = factor_calc.calculate()
            self.benefit_factors.append(factor)

        return self.benefit_factors


class BenefitFactor:

    def __init__(self,
                 factor_name: str,
                 factor_type: str,
                 factor_config: dict,
                 plan: PlanModel,
                 benefit: BenefitModel,
                 rate_table: RateTableModel,
                 provision: ProvisionModel
                 ):

        self.__config = factor_config
        self.__factor_name = factor_name
        self.__factor_type = factor_type

        self.__provision = provision
        self.__benefit = benefit
        self.__rate_table = rate_table
        self.__plan = plan
        self.__attributes = {}

        self.set_attributes(plan)
        self.set_attributes(benefit)
        self.set_attributes(rate_table)
        self.set_attributes(provision)

        self.__provision_value = self.__provision.getValue()

        # set value, selection, and selection_type
        self.calculate()

    def __repr__(self) -> str:
        return f"<Factor: {self.__factor_name}>"

    def set_attributes(self, instance) -> None:
        for k, v in instance.__dict__.items():
            setattr(self, k, v)

    def _create_factor(self) -> BenefitFactorModel:
        """
        Create a factor database model after all the 
        calculations have completed
        """
        self.__factor = BenefitFactorModel(
            plan_id=self.plan_id,
            provision_id=self.provision_id,
            factor_type=self.__factor_type,
            factor_name=self.__factor_name,
            factor_selection=self.__factor_selection,
            factor_selection_type=self.__factor_selection_type,
            factor_value=self.__factor_value
        )
        return self.__factor

    def calculate(self) -> BenefitFactorModel:
        """
        Calculate the factor value and selection.
        This function mostly calls other functions to do the processing.

        If `variability` is a key in the provision configuration, then that
        subroutine is called. 

        If `function` is a key in the provision configuration, then that 
        subroutine is called. 

        Otherwise, the default factor value is returned. 
        """
        val = self.__config.get('default_factor_value', 1)
        uuid = self.__config.get('uuid')
        variability = self.__config.get('variability')
        functional = self.__config.get('function')

        # if there is factor variability, process it
        if variability:
            selection, sel_value = self._variabilityHandler(
                variability, self, val, uuid)

            self.__factor_selection = selection
            self.__factor_selection_type = 'uuid'
            self.__factor_value = sel_value
        # if there is a custom factor function, process it
        elif functional:
            pass
        # otherwise, return the default factor
        else:
            self.__factor_selection = 'default'
            self.__factor_selection_type = 'uuid'
            self.__factor_value = val

        return self._create_factor()

    def _variabilityHandler(
        self,
        variability: dict,
        factor_attributes,
        default_value: float,
        default_uuid: str
    ) -> Tuple[str, float]:
        """
        Process each rule in the factor variability object. The first rule 
        that is true is returned.

        Each rule should be an object. Each key in the object should correspond
        to an attribute from either the plan, provision, benefit, or rate_table
        objects. The values can be a string, boolean, list, or object. 
        """
        for item in variability:
            applyRule = True
            for k, v in item.items():
                if k in ['factor_value', '_id', 'uuid']:
                    continue

                attr = getattr(factor_attributes, k, '__DUMMY__')
                if type(v) == list:
                    applyRule = (attr in v) and applyRule
                elif type(v) == dict:
                    if v['comparison'] == "range":
                        applyRule = (float(attr) >= v['lower'] and
                                     float(attr) <= v['upper'] and
                                     applyRule)

                    elif v['comparison'] == "nlist":
                        applyRule = attr in v['value'] and applyRule
                    elif v['comparison'] == "nrange":
                        applyRule = not (float(attr) >= v['lower'] and
                                         float(attr) <= v['upper']) and applyRule
                    elif v['comparison'] == 'lt':
                        applyRule = float(attr) < v['value'] and applyRule
                    elif v['comparison'] == 'le':
                        applyRule = float(attr) <= v['value'] and applyRule
                    elif v['comparison'] == 'gt':
                        applyRule = float(attr) > v['value'] and applyRule
                    elif v['comparison'] == 'ge':
                        applyRule = float(attr) >= v['value'] and applyRule
                elif type(v) == bool:
                    attr = (str(attr).lower().strip() == 'true')
                    applyRule = (attr == v) and applyRule
                else:
                    applyRule = (attr == v) and applyRule

            if applyRule:
                val = item['factor_value']
                uuid = item.get('uuid')
                return uuid, val

        return default_uuid, default_value

    def _functionalHandler(self):
        return
