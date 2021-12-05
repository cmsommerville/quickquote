from flask import request
from flask_restful import Resource

from ..models import Model_ConfigCoverage, Model_ConfigCoverageStateAvailability
from ..schemas import Schema_ConfigCoverage, Schema_ConfigCoverageStateAvailability

config_coverage_schema = Schema_ConfigCoverage()
config_coverage_state_schema = Schema_ConfigCoverageStateAvailability()

config_coverage_schema_list = Schema_ConfigCoverage(many=True)

class Resource_CoverageStateConfig(Resource):

    @classmethod
    def get(cls):
        state = request.args.get('state')
        effective_date = request.args.get('effective_date')
        product_code = request.args.get('product_code')
        res = Model_ConfigCoverage.find_by_state(state, effective_date, product_code)
        return config_coverage_schema_list.dump(res), 200


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
        


class CRUD_CoverageStateAvailabilityConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigCoverageStateAvailability.find(id)
        return config_coverage_state_schema.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_coverage_state_schema.load(req)
        config.save_to_db()
        return config_coverage_state_schema.dump(config), 201

    @classmethod
    def put(cls, id):
        req = request.get_json()
        config = config_coverage_state_schema.load({**req, "coverage_state_availability_id": id})
        config.save_to_db()
        return config_coverage_state_schema.dump(config), 201

    @classmethod
    def delete(cls, id):
        config = Model_ConfigCoverageStateAvailability.find(id)
        config.delete()
        return "Deleted", 204