from flask import request
from flask_restful import Resource

from ..models import Model_ConfigProductVariation, Model_ConfigAgeBand, \
    Model_ConfigAgeBandSet
from ..schemas import Schema_ConfigProductVariation, Schema_ConfigAgeBand, \
    Schema_ConfigAgeBandSet

config_product_variation_schema = Schema_ConfigProductVariation()
config_age_bands_set_schema = Schema_ConfigAgeBandSet()
config_age_bands_schema = Schema_ConfigAgeBand()


class CRUD_ProductVariationsConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigProductVariation.find(id)
        return config_product_variation_schema.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_product_variation_schema.load(req)
        config.save_to_db()
        return config_product_variation_schema.dump(config), 201

    @classmethod
    def put(cls, id):
        req = request.get_json()
        config = config_product_variation_schema.load({**req, "product_variation_id": id})
        config.save_to_db()
        return config_product_variation_schema.dump(config), 201

    @classmethod
    def delete(cls, id):
        config = Model_ConfigProductVariation.find(id)
        config.delete()
        return "Deleted", 204
        

class CRUD_AgeBandsSetConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigAgeBandSet.find(id)
        return config_age_bands_set_schema.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_age_bands_set_schema.load(req)
        config.save_to_db()
        return config_age_bands_set_schema.dump(config), 201

    @classmethod
    def put(cls, id):
        req = request.get_json()
        config = config_age_bands_set_schema.load({**req, "age_band_set_id": id})
        config.save_to_db()
        return config_age_bands_set_schema.dump(config), 201

    @classmethod
    def delete(cls, id):
        config = Model_ConfigAgeBandSet.find(id)
        config.delete()
        return "Deleted", 204


class CRUD_AgeBandsConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigAgeBand.find(id)
        return config_age_bands_schema.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_age_bands_schema.load(req)
        config.save_to_db()
        return config_age_bands_schema.dump(config), 201

    @classmethod
    def put(cls, id):
        req = request.get_json()
        config = config_age_bands_schema.load({**req, "age_band_id": id})
        config.save_to_db()
        return config_age_bands_schema.dump(config), 201

    @classmethod
    def delete(cls, id):
        config = Model_ConfigAgeBand.find(id)
        config.delete()
        return "Deleted", 204
        