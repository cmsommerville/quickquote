from sqlalchemy.orm import aliased, contains_eager, Query
from sqlalchemy import and_, between, literal
from app.extensions import db

from ..config.models import Model_ConfigBenefit, Model_ConfigProvision,\
    Model_ConfigBenefitProvision, Model_ConfigFactor, Model_ConfigFactorRule
from ..selections.models import RateTableModel, Model_SelectionProvision, Model_SelectionBenefit, Model_SelectionPlan

def query_rating(
    plan: Model_SelectionPlan) -> Query: 


    qry = db.session.query(
        Model_SelectionPlan.selection_plan_id, 
        Model_SelectionPlan.broker_id, 
        Model_SelectionPlan.group_id, 
        Model_SelectionPlan.is_smoker_distinct, 
        Model_SelectionPlan.is_gender_distinct, 

        Model_SelectionBenefit.selection_benefit_id, 
        Model_SelectionProvision.selection_provision_id, 
        Model_SelectionBenefit.config_benefit_id, 
        Model_SelectionProvision.config_provision_id, 
        Model_ConfigBenefit.coverage_id, 
        Model_ConfigBenefit.rate_group_id,
        Model_ConfigFactor.factor_id, 
        Model_ConfigFactorRule.factor_rule_id, 

        RateTableModel.rate_table_id, 
        RateTableModel.product_code, 
        RateTableModel.product_variation_code, 
        RateTableModel.age, 
        RateTableModel.family_code, 
        RateTableModel.smoker_status, 
        RateTableModel.gender, 
        RateTableModel.benefit_code, 
        RateTableModel.annual_rate_per_unit, 
        RateTableModel.unit_value, 
        
        Model_SelectionBenefit.benefit_value, 
        Model_SelectionProvision.provision_value, 
        Model_SelectionProvision.provision_data_type, 
        
        Model_ConfigFactor.factor_priority, 
        Model_ConfigFactor.factor_value, 
        
        Model_ConfigFactorRule.class_name, 
        Model_ConfigFactorRule.field_name, 
        Model_ConfigFactorRule.comparison_operator_code, 
        Model_ConfigFactorRule.field_value, 
        Model_ConfigFactorRule.field_value_data_type
    )

    qry = qry.join(Model_ConfigBenefit, RateTableModel.benefit_code == Model_ConfigBenefit.benefit_code)
    
    qry = qry.join(Model_ConfigBenefitProvision, Model_ConfigBenefit.benefit_id == Model_ConfigBenefitProvision.benefit_id)

    qry = qry.join(Model_ConfigProvision, Model_ConfigBenefitProvision.provision_id == Model_ConfigProvision.provision_id)

    qry = qry.join(Model_ConfigFactor, Model_ConfigProvision.provision_id == Model_ConfigFactor.provision_id)

    qry = qry.join(Model_ConfigFactorRule)

    qry = qry.join(Model_SelectionBenefit, and_(
        Model_ConfigBenefit.benefit_id == Model_SelectionBenefit.config_benefit_id, 
        Model_SelectionBenefit.selection_plan_id == plan.selection_plan_id
        )
    )

    qry =  qry.join(Model_SelectionProvision, and_(
        Model_ConfigProvision.provision_id == Model_SelectionProvision.config_provision_id,  
        Model_SelectionProvision.selection_plan_id == plan.selection_plan_id
        )
    )

    qry =  qry.join(Model_SelectionPlan, Model_SelectionProvision.selection_plan_id == Model_SelectionPlan.selection_plan_id)

    return qry