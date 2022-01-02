from flask import request
from flask_restful import Resource

from ..models import Model_ConfigBenefit, Model_ConfigBenefitDuration
from ..schemas import Schema_ConfigBenefit, Schema_ConfigBenefitDuration

_config_schema = Schema_ConfigBenefit()
_config_benefit_schema_list = Schema_ConfigBenefit(many=True)

_config_duration_schema = Schema_ConfigBenefitDuration()
_config_duration_schema_list = Schema_ConfigBenefitDuration(many=True)


class Query_AllBenefits(Resource):

    @classmethod
    def get(cls):
        product_id = request.args.get('product_id')
        res = Model_ConfigBenefit.find_by_product(product_id)
        return _config_benefit_schema_list.dump(res), 200


class Query_AllBenefitDurations(Resource):

    @classmethod
    def get(cls):
        benefit_id = request.args.get('benefit_id')
        res = Model_ConfigBenefitDuration.find_by_benefit(benefit_id)
        return _config_duration_schema_list.dump(res), 200
