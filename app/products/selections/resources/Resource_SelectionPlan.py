import requests
from flask import request, session
from flask_restful import Resource

from ..models import Model_SelectionPlan
from ..schemas import Schema_SelectionPlan

plan_schema = Schema_SelectionPlan()


class Resource_SelectionPlan(Resource):

    @classmethod
    def get(cls, plan_id):
        try:
            plan = Model_SelectionPlan.find_one(plan_id)
            return plan_schema.dump(plan), 200
        except:
            return None, 200

    @classmethod
    def post(cls):
        data = request.get_json()
        plan = plan_schema.load(data)

        try:
            plan.save_to_db()
        except Exception as e:
            print(e)

        # add default distributions to selections table
        requests.post(f'http://localhost:5000/selections/plan/{plan.selection_plan_id}/default-dist', json={})

        return plan_schema.dump(plan), 201
