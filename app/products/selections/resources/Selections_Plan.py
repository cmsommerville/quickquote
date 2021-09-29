import requests
from flask import request, session
from flask_restful import Resource

from ..models.PlanModel import PlanModel
from ..schemas.PlanSchema import PlanSchema

plan_schema = PlanSchema()


class PlanSelections(Resource):

    @classmethod
    def get(cls):
        plan_id = request.args.get("plan_id")
        if plan_id is None:
            raise Exception("Please provide a plan_id query parameter")

        plan = PlanModel.find_by_id(plan_id)
        return plan_schema.dump(plan), 200

    def post(self):
        plan_config_id = request.args.get("plan_config_id")
        data = request.get_json()
        plan = plan_schema.load(data)
        config = requests.get(
            f"{request.url_root}config/plan/{plan_config_id}").json()

        try:
            plan.save_to_db()
            plan_id = plan.plan_id
            session["PLAN-" + str(plan_id)] = {
                "plan": plan_schema.dump(plan),
                "plan_config": config
            }
        except Exception as e:
            print(e)

        return plan_schema.dump(plan), 201
