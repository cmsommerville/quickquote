from flask import request
from flask_restful import Resource

from ..models import Model_ConfigProductVariations
from ..schemas import Schema_ConfigProductVariations

config_product_variation_schema_list = Schema_ConfigProductVariations(many=True)


class Resource_ProductVariationConfig(Resource):

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_product_variation_schema_list.load(req)
        Model_ConfigProductVariations.save_all_to_db(config)
        return "woot", 201
