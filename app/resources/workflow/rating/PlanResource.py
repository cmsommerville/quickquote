from flask import request, session
from flask_restful import Resource
from app.models import mongo
from app.util.mongo import projectMongoResults

from app.models.PlanModel import PlanModel
from app.schemas.PlanSchema import PlanSchema

plan_schema = PlanSchema()


class Plan(Resource):

    @classmethod
    def get(cls):
        res = mongo.db.products.find(
            projection=["name", "text", "statesApproved"])

        products = projectMongoResults(res, ["name", "text", "statesApproved"])

        return {"products": products}, 200

    def post(self):

        data = request.get_json()
        plan_id = session.get("quote", {}).get("plan_id")
        if plan_id:
            oldPlan = PlanModel.find_by_id(plan_id)
            plan = plan_schema.load(
                {**data, "plan_number": oldPlan.plan_number})
        else:
            plan = plan_schema.load(data)

        try:
            plan.save_to_db()
        except:
            print("Couldn't write to db")

        session['quote']['plan_id'] = plan.plan_id

        return {"plan_id": plan.plan_id}, 201
