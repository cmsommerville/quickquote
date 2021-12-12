from flask import request
from app.products.config.models.Config_Benefit import Model_ConfigBenefitDuration
from flask_restful import Resource

from ..models import Model_ConfigBenefit, Model_ConfigBenefitDuration
from ..schemas import Schema_ConfigBenefit, Schema_ConfigBenefitDuration

config_schema = Schema_ConfigBenefit()
config_schema_list = Schema_ConfigBenefit(many=True)


config_duration_schema = Schema_ConfigBenefitDuration()
config_duration_schema_list = Schema_ConfigBenefitDuration(many=True)


class Query_AllBenefits(Resource):

    @classmethod
    def get(cls):
        product_id = request.args.get('product_id')
        res = Model_ConfigBenefit.find_by_product(product_id)
        return config_schema_list.dump(res), 200


class Query_AllBenefitDurations(Resource):

    @classmethod
    def get(cls):
        benefit_id = request.args.get('benefit_id')
        res = Model_ConfigBenefitDuration.find_by_benefit(benefit_id)
        return config_duration_schema_list.dump(res), 200
