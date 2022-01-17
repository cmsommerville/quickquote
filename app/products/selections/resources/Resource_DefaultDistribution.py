from flask import request, session
from flask_restful import Resource

from ..models import Model_SelectionDistribution, Model_SelectionPlan
from ..schemas import Schema_SelectionDistribution
from ...config.schemas import Schema_ConfigAttributeDistributionSet

_config_schema_list = Schema_ConfigAttributeDistributionSet()
_selection_schema_list = Schema_SelectionDistribution(many=True)


def _formatter(input_dist: dict, plan_id: int):
    return [{
        "selection_plan_id": plan_id, 
        "attr_type_code": input_dist['attr_type_code'], 
        "attr_value": dist['attr_value'], 
        "weight": dist['weight'], 
    } for dist in input_dist['attr_distribution']]

class Resource_DefaultDistribution(Resource):

    @classmethod
    def post(cls, plan_id: int):
        plan = Model_SelectionPlan.find_one(plan_id)
        product_variation = plan.product_variation

        if plan.is_gender_distinct:
            gender = _config_schema_list.dump(product_variation.sex_distinct_distribution)
        else: 
            gender = _config_schema_list.dump(product_variation.unisex_distribution)
        
        if plan.is_smoker_distinct:
            smoker = _config_schema_list.dump(product_variation.smoker_distinct_distribution)
        else: 
            smoker = _config_schema_list.dump(product_variation.unismoker_distribution)

        dists = _selection_schema_list.load([
            *_formatter(smoker, plan_id), 
            *_formatter(gender, plan_id), 
        ])

        Model_SelectionDistribution.delete_by_plan(plan_id)
        Model_SelectionDistribution.save_all_to_db(dists)

        return "Created", 201
            