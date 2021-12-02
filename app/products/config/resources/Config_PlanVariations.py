from flask import request
from flask_restful import Resource

from ..models import Model_ConfigPlanVariations
from ..schemas import Schema_ConfigPlanVariations

config_plan_variation_schema_list = Schema_ConfigPlanVariations(many=True)


class Resource_PlanVariationConfig(Resource):

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_plan_variation_schema_list.load(req)
        Model_ConfigPlanVariations.save_all_to_db(config)
        return "woot", 201
