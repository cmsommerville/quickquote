from collections import defaultdict
from flask import request
from flask_restful import Resource
from sqlalchemy.orm import aliased, contains_eager
from sqlalchemy import and_
from sqlalchemy.sql.expression import literal_column
from app.extensions import db


from ...config.models import Model_ConfigBenefitProductVariation, Model_ConfigBenefit, Model_ConfigBenefitDuration, Model_ConfigBenefitDurationItem
from ..models import Model_SelectionBenefit, Model_SelectionBenefitDuration, Model_SelectionPlan
from ..schemas.Schema_QueryBenefitProductVariations import Schema_QueryBPV

config_schema_list = Schema_QueryBPV(many=True)

def formatter(config):
    """
    Allocate benefits to coverages
    """
    covg_dd = defaultdict(list)
    for bnft in config:
        covg = bnft['coverage']['coverage_label']
        covg_dd[covg].append(bnft)
    
    return [{
        **bnfts[0]['coverage'],
        "benefits": bnfts
    } for covg, bnfts in covg_dd.items()]


class Query_AllBenefitProductVariations(Resource):

    @classmethod
    def get(cls, plan_id):
        plan = Model_SelectionPlan.find_one(plan_id)
        if not plan: 
            return "error", 400
        # check that plan benefits exist 
        has_plan_benefits = (Model_SelectionBenefit.query.filter(Model_SelectionBenefit.selection_plan_id == plan_id).count() > 0)

        ConfigBenefitState = aliased(Model_ConfigBenefit)
        bnft_prod_variation = db.session.query(
            Model_ConfigBenefitProductVariation, 
            )\
            .join(Model_ConfigBenefit)\
            .join(ConfigBenefitState, ConfigBenefitState.parent_id == Model_ConfigBenefit.benefit_id)\
            .outerjoin(Model_ConfigBenefitDuration, 
                Model_ConfigBenefit.benefit_id == Model_ConfigBenefitDuration.benefit_id
            )\
            .outerjoin(Model_ConfigBenefitDurationItem)\
            .filter(
                Model_ConfigBenefitProductVariation.product_variation_id == plan.config_product_variation_id, 
                Model_ConfigBenefit.parent_id == None, 
                ConfigBenefitState.state_id == plan.config_state_id
            )\
            .outerjoin(Model_SelectionBenefitDuration, and_(
                Model_ConfigBenefitDuration.benefit_duration_id == Model_SelectionBenefitDuration.config_benefit_duration_id, 
                Model_SelectionBenefitDuration.selection_plan_id == plan_id, 
                has_plan_benefits == True
            ))\
            .outerjoin(Model_SelectionBenefit, and_(
                Model_ConfigBenefit.benefit_id == Model_SelectionBenefit.config_benefit_id,
                Model_SelectionBenefit.selection_plan_id == plan_id, 
                has_plan_benefits == True
            )).options(
                contains_eager(
                    Model_ConfigBenefitProductVariation.benefit, 
                    Model_ConfigBenefit.selected_benefit
                ), 
                contains_eager(
                    Model_ConfigBenefitProductVariation.benefit,
                    Model_ConfigBenefit.durations,
                    Model_ConfigBenefitDuration.selected_duration_item
                )
            )
            

        data = config_schema_list.dump(bnft_prod_variation.populate_existing())
        data = formatter(config_schema_list.dump(bnft_prod_variation))
        return {"coverages":data, "selections_exist": has_plan_benefits}, 200