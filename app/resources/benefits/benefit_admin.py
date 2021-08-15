from flask import request
from flask_restful import Resource
from app.models.benefits.BenefitModel import BenefitModel
from app.models.benefits.BenefitSchema import BenefitSchema


benefit_schema = BenefitSchema()
benefit_list_schema = BenefitSchema(many=True)


class BenefitAdmin(Resource):

    @classmethod
    def get(cls):
        id = request.args.get("id")
        benefit = BenefitModel.find_by_id(id)
        return benefit_schema.dump(benefit)

    def post(self):
        data = request.get_json()
        benefit = BenefitModel(**benefit_schema.load(data))
        benefit.save_to_db()
        return benefit_schema.dump(benefit)


class BenefitAdminList(Resource):

    @classmethod
    def get(cls):
        benefits = BenefitModel.find_all(num_rows=1000)
        return benefit_list_schema.dump(benefits)
