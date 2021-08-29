from flask import request, session
from flask_restful import Resource
from app.models import mongo

from app.models.FactorModel import FactorModel
from app.schemas.FactorSchema import FactorSchema

plan_schema = PlanSchema()


def projectMongoResults(cursor, keys):
    result = []
    for row in cursor:
        result.append({k: v for k, v in row.items() if k in keys})
    return result


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
            plan = PlanModel.find_by_id(plan_id)
            plan.reset(data)
        else:
            plan = plan_schema.load(data)

        try:
            plan.save_to_db()
        except:
            print("Couldn't write to db")

        session['quote']['plan_id'] = plan.plan_id

        return {"plan_id": plan.plan_id}, 201
