from flask import request
from flask_restful import Resource

from ..models import Model_ConfigPlan


class Resource_PlanConfig(Resource):

    def get(self, id):
        res = Model_ConfigPlan.find_qry(id)
        print(type(res))
        return "Found it!", 200
