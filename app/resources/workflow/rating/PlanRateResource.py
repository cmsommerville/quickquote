from flask import request, session
from flask_restful import Resource
from app.models import mongo
from app.util.mongo import projectMongoResults

from app.models.PlanRateModel import PlanRateModel
from app.schemas.PlanRateSchema import PlanRateSchema

plan_rate_list_schema = PlanRateSchema(many=True)


class PlanRate(Resource):

    @classmethod
    def get(cls):

        res = projectMongoResults(mongo.db.products.find_one({"name": "critical_illness"}, {
            "rate_template": True}))[0]
        return res
        # selections = {}
        # plan_id = request.args.get("plan_id")

        # plan = PlanModel.find_by_id(plan_id)
        # selections = plan_schema.dump(plan)

        # res = mongo.db.products.find(
        #     projection=["name", "text", "statesApproved"])

        # products = projectMongoResults(res, ["name", "text", "statesApproved"])

        # return {"products": products, "selections": selections}, 200

    def post(self):
        res = projectMongoResults(mongo.db.products.find_one({"name": "critical_illness"}, {
            "rate_template": True}))[0]
        plan_id = request.args.get("plan_id")

        data = [{**pr, "plan_id": plan_id} for pr in res['rate_template']]
        plan_rates = plan_rate_list_schema.load(data)

        try:
            PlanRateModel.save_all_to_db(plan_rates, plan_id)
        except Exception as e:
            print(e)

        return {"plan_rate_id": data}, 201
