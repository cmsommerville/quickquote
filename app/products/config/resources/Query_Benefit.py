from flask import request
from flask_restful import Resource

from ..models import Model_ConfigBenefit
from ..schemas import Schema_ConfigBenefit

config_schema = Schema_ConfigBenefit()
config_schema_list = Schema_ConfigBenefit(many=True)



class Query_AllBenefits(Resource):

    @classmethod
    def get(cls):
        product_id = request.args.get('product_id')
        res = Model_ConfigBenefit.find_by_product(product_id)
        return config_schema_list.dump(res), 200
