from flask import request
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

        data = request.get_json()
        plan_id = data.get("plan_id")
        if plan_id:
            oldPlan = PlanModel.find_by_id(plan_id)
            plan = plan_schema.load(
                {**data, "plan_number": oldPlan.plan_number})
        else:
            plan = plan_schema.load(data)

        try:
            plan.save_to_db()
        except Exception as e:
            print(e)

        return plan_schema.dump(plan), 201
