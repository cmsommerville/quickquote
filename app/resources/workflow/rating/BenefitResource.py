from flask import request, session
from flask_restful import Resource
from app.models import mongo
from app.util.mongo import projectMongoResults

from app.models.PlanModel import PlanModel
from app.models.PlanRateModel import PlanRateModel
from app.models.BenefitModel import BenefitModel
from app.models.CoverageModel import CoverageModel

from app.schemas.BenefitSchema import BenefitSchema
from app.schemas.CoverageSchema import CoverageSchema

benefit_list_schema = BenefitSchema(many=True)


class BenefitsList(Resource):

    @classmethod
    def get(cls):

        res = mongo.db.products.find(
            projection=["benefits"])

        benefits = projectMongoResults(res, ["benefits"])[0]['benefits']

        return benefits, 200

    @classmethod
    def post(cls):
        factorList = []
        plan_id = request.args.get("plan_id")
        if plan_id is None:
            raise Exception("Plan ID not provided")

        return "Success", 201
