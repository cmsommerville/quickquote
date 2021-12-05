from flask import request
from flask_restful import Resource

from ..models import Model_ConfigProduct, Model_ConfigProductStateAvailability
from ..schemas import Schema_ConfigProduct, Schema_ConfigProductStateAvailability

config_product_schema = Schema_ConfigProduct()
config_product_state_schema = Schema_ConfigProductStateAvailability()

config_product_schema_list = Schema_ConfigProduct(many=True)
config_product_state_schema_list = Schema_ConfigProductStateAvailability(many=True)

class Resource_ProductStateConfig(Resource):

    @classmethod
    def get(cls):
        state = request.args.get('state')
        effective_date = request.args.get('effective_date')
        product_code = request.args.get('product_code')
        res = Model_ConfigProduct.find_by_state(state, effective_date, product_code)
        return config_product_schema_list.dump(res), 200


class CRUD_ProductConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigProduct.find(id)
        return config_product_schema.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_product_state_schema_list.load(req)
        config.save_to_db()
        return config_product_state_schema_list.dump(config), 201

    @classmethod
    def put(cls, id):
        req = request.get_json()
        config = config_product_schema.load({**req, "product_id": id})
        config.save_to_db()
        return config_product_schema.dump(config), 201

    @classmethod
    def delete(cls, id):
        config = Model_ConfigProduct.find(id)
        config.delete()
        return "Deleted", 204
        


class CRUD_ProductStateAvailabilityConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigProductStateAvailability.find(id)
        return config_product_state_schema.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_product_state_schema.load(req)
        Model_ConfigProductStateAvailability.save_all_to_db(config)
        return config_product_state_schema.dump(config), 201

    @classmethod
    def put(cls, id):
        req = request.get_json()
        config = config_product_state_schema.load({**req, "product_state_availability_id": id})
        config.save_to_db()
        return config_product_state_schema.dump(config), 201

    @classmethod
    def delete(cls, id):
        config = Model_ConfigProductStateAvailability.find(id)
        config.delete()
        return "Deleted", 204