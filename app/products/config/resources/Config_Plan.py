from flask import request
from flask_restful import Resource

from ..models import Model_ConfigPlan
from ..schemas import Schema_ConfigPlan

config_plan_schema = Schema_ConfigPlan()


class Resource_PlanConfig(Resource):

    def get(self, id):
        res = Model_ConfigPlan.find_qry(id)
        print(type(res))
        return "Found it!", 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_plan_schema.load(req)
        config.save_to_db()
        return "woot", 201
