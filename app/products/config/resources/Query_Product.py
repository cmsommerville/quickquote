from flask import request
from flask_restful import Resource

from ..models import Model_ConfigProduct
from ..schemas import Schema_ConfigProduct

config_product_schema = Schema_ConfigProduct()
config_product_schema_list = Schema_ConfigProduct(many=True)

class Query_ProductStateConfig(Resource):

    @classmethod
    def get(cls):
        product_code = request.args.get('product_code')
        state = request.args.get('state')
        effective_date = request.args.get('effective_date')
        res = Model_ConfigProduct.find_by_state(state, effective_date, product_code)
        return config_product_schema_list.dump(res), 200
