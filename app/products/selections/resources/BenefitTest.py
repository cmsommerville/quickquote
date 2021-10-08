from flask import request, session
from flask_restful import Resource

from ..models.BenefitModel import BenefitModel
from ..schemas.BenefitSchema import BenefitSchema

benefit_schema = BenefitSchema()
benefit_list_schema = BenefitSchema(many=True)


class BenefitResource(Resource):

    @classmethod
    def get(cls):
        benefit_id = request.args.get('benefit_id')
        benefit = BenefitModel.find_by_id(benefit_id)
        return benefit_schema.dump(benefit), 200

    @classmethod
    def post(cls):
        data = request.get_json()
        benefit = benefit_schema.load(data)

        try:
            benefit.save_to_db()
        except Exception as e:
            return str(e), 400

        return benefit_schema.dump(benefit), 201
