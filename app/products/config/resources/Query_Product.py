from app.products.config.models.Config_ProductStateAvailability import Model_ConfigProductStateAvailability
from flask import request
from flask_restful import Resource

from ..models import Model_ConfigProduct, Model_ConfigProductStateAvailability
from ..schemas import Schema_ConfigProduct, Schema_ConfigProductStateAvailability

config_product_schema = Schema_ConfigProduct()
config_product_schema_list = Schema_ConfigProduct(many=True)
config_product_state_schema_list = Schema_ConfigProductStateAvailability(many=True)

class Query_AllProducts(Resource):

    @classmethod
    def get(cls):
        res = Model_ConfigProduct.find_all()
        return config_product_schema_list.dump(res), 200


class Query_AllProductStates(Resource):

    @classmethod
    def get(cls):
        product_id = request.args.get('product_id')
        res = Model_ConfigProductStateAvailability.find_by_product(product_id)
        return config_product_state_schema_list.dump(res), 200

