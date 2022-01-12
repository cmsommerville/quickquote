from typing import List
from decimal import Decimal

from ..models import Model_SelectionBenefitFactor, Model_SelectionPlan, \
    Model_SelectionBenefit, RateTableModel, Model_SelectionProvision
from ...config.models import Model_ConfigFactor

class Rating_BenefitFactorList:

    def __init__(self,
                 plan: Model_SelectionPlan,
                 benefit: Model_SelectionBenefit,
                 rate_table: RateTableModel,
                 provisions: List[Model_SelectionProvision]
                 ):

        self.plan = plan
        self.benefit = benefit
        self.rate_table = rate_table
        self.provisions = provisions
        self.factors = []

    def calculate(self) -> List[Model_SelectionBenefitFactor]:
        """
        Loop over all the factor data and create factor objects.
        """

        for provision in self.provisions:

            # this instantiates a benefit factor object
            factor = Rating_BenefitFactor(
                plan=self.plan,
                benefit=self.benefit,
                rate_table=self.rate_table,
                provision=provision
            )
            
            self.factors.append(factor.selected_factor)

        return self.factors


class Rating_BenefitFactor:

    def __init__(self,
                 plan: Model_SelectionPlan,
                 benefit: Model_SelectionBenefit,
                 rate_table: RateTableModel,
                 provision: Model_SelectionProvision
                 ):

        self.provision = provision
        self.config_factors = provision.config_provision.factors
        self.benefit = benefit
        self.rate_table = rate_table
        self.plan = plan
        self.selected_factor = None

        # set value, selection, and selection_type
        self.calculate()

    def return_model(self, selected_factor: Model_ConfigFactor) -> Model_SelectionBenefitFactor:
        """
        Create a factor database model after all the 
        calculations have completed
        """
        return Model_SelectionBenefitFactor(
            selection_plan_id=self.plan.selection_plan_id,
            selection_provision_id=self.provision.selection_provision_id,
            config_factor_id=selected_factor.factor_id if selected_factor is not None else None, 
            factor_value=selected_factor.factor_value if selected_factor is not None else 1
        )

    def calculate(self) -> Model_SelectionBenefitFactor:
        """
        Calculate the factor value and selection.
        This function mostly calls other functions to do the processing.

        Call the factor handler method
        """
        selected_factor = self._factor_handler()
        self.selected_factor = self.return_model(selected_factor)
        

    def _cast(self, attr, data_type): 
        if data_type == 'number':
            attr = float(attr)
        elif data_type == 'boolean':
            attr = attr.lower() == 'true'
        return attr

    def _factor_handler(self) -> Model_ConfigFactor:
        """
        Process each rule in the factor variability object. The first rule 
        that is true is returned.

        """
        for item in self.config_factors:
            applyRule = True
            for rule in item.factor_rules:
                # get instance 
                instance = getattr(self, rule.class_name)

                # get attribute
                if rule.field_name == 'provision_code':
                    attr = instance.provision_value
                    attr = self._cast(attr, self.provision.provision_data_type)
                else: 
                    attr = getattr(instance, rule.field_name)

                # get rule value to compare to
                rule_value = self._cast(rule.field_value, rule.field_value_data_type)

                # apply comparison
                applyRule = getattr(attr, rule.comparison_operator_code)(rule_value) and applyRule
                    
            if applyRule:
                return item

        return None

    def _functionalHandler(self):
        return
