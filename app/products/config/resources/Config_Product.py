from flask import request
from flask_restful import Resource

from ..models import Model_ConfigProduct
from ..schemas import Schema_ConfigProduct

config_product_schema = Schema_ConfigProduct()


class Resource_ProductConfig(Resource):

    @classmethod
    def get(self):
        id = request.args.get('id')
        res = Model_ConfigProduct.find(id)
        return config_product_schema.dump(res), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_product_schema.load(req)
        config.save_to_db()
        return config_product_schema.dump(config), 201
