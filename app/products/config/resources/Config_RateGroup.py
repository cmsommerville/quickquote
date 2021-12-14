from flask import request
from flask_restful import Resource

from ..models import Model_ConfigRateGroup
from ..schemas import Schema_ConfigRateGroup

config_schema = Schema_ConfigRateGroup()
config_schema_list = Schema_ConfigRateGroup(many=True)

class CRUD_RateGroupConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigRateGroup.find(id)
        return config_schema.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_schema.load(req)
        config.save_to_db()
        return config_schema.dump(config), 201

    @classmethod
    def put(cls, id):
        req = request.get_json()
        config = config_schema.load({**req, "rate_group_id": id})
        config.save_to_db()
        return config_schema.dump(config), 201

    @classmethod
    def delete(cls, id):
        config = Model_ConfigRateGroup.find(id)
        config.delete()
        return "Deleted", 204
        

