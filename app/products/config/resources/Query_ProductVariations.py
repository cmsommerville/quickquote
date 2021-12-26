from flask import request
from flask_restful import Resource

from ..models import Model_ConfigProductVariation
from ..schemas import Schema_ConfigProductVariation

config_schema = Schema_ConfigProductVariation()
config_schema_list = Schema_ConfigProductVariation(many=True)


class Query_AllProductVariations(Resource):

    @classmethod
    def get(cls):
        product_id = request.args.get('product_id')
        res = Model_ConfigProductVariation.find_by_product(product_id)
        return config_schema_list.dump(res), 200


# class Query_ProductStateConfig(Resource):

#     @classmethod
#     def get(cls):
#         product_code = request.args.get('product_code')
#         state = request.args.get('state')
#         effective_date = request.args.get('effective_date')
#         res = Model_ConfigProduct.find_by_state(state, effective_date, product_code)
#         return config_product_schema_list.dump(res), 200
