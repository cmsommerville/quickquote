from flask import request
from flask_restful import Resource

from ..models import Model_ConfigCoverage
from ..schemas import Schema_ConfigCoverage

config_coverage_schema = Schema_ConfigCoverage()

config_coverage_schema_list = Schema_ConfigCoverage(many=True)

class CRUD_CoverageConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigCoverage.find(id)
        return config_coverage_schema.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_coverage_schema.load(req)
        config.save_to_db()
        return config_coverage_schema.dump(config), 201

    @classmethod
    def put(cls, id):
        req = request.get_json()
        config = config_coverage_schema.load({**req, "coverage_id": id})
        config.save_to_db()
        return config_coverage_schema.dump(config), 201

    @classmethod
    def delete(cls, id):
        config = Model_ConfigCoverage.find(id)
        config.delete()
        return "Deleted", 204
        

