import json
from flask import request, session
from flask_restful import Resource
from app.models import mongo

from app.models.PlanModel import PlanModel
from app.schemas.PlanSchema import PlanSchema

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

        # selections = {}
        # group = session.get("selections", {}).get("group")

        # if group:
        #     selections = group_schema.dump(group)

        # return {
        #     "product": data['productName'],
        #     "statesApproved": data['statesApproved'],
        #     "selections": selections
        # }, 200

        return {"products": products}, 200

    def post(self):

        data = request.get_json()
        plan = session.get("selections", {}).get("plan")
        if plan:
            plan.reset(data)
        else:
            plan = plan_schema.load(data)

        try:
            plan.save_to_db()
        except:
            print("Couldn't write to db")

        session['selections'] = {
            **session.get('selections', {}),
            "plan": plan
        }

        return "Success", 201
