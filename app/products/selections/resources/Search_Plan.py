from flask import request
from flask_restful import Resource

from ..models.PlanModel import PlanModel
from ..schemas.PlanSchema import PlanSchema

plan_schema = PlanSchema()
plan_list_schema = PlanSchema(many=True)


class PlanSearch(Resource):

    @classmethod
    def get(cls):
        plan_id = request.args.get("plan_id")

        try:
            plan = PlanModel.search_by_id(int(plan_id))
            return plan_list_schema.dump(plan), 200
        except:
            return None, 200
