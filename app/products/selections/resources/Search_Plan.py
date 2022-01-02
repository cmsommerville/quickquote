from flask import request
from flask_restful import Resource

from ..models import Model_SelectionPlan
from ..schemas import Schema_SelectionPlan

plan_schema = Schema_SelectionPlan()
plan_list_schema = Schema_SelectionPlan(many=True)


class PlanSearch(Resource):

    @classmethod
    def get(cls):
        plan_id = request.args.get("plan_id")

        try:
            plan = Model_SelectionPlan.search_by_id(int(plan_id))
            return plan_list_schema.dump(plan), 200
        except:
            return None, 200
