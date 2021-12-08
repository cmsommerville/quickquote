from flask import request
from flask_restful import Resource

from ..models import Model_RefBenefit, Model_RefBenefitDuration, Model_RefBenefitDurationItems, \
    Model_RefComparisonOperator, Model_RefComponentTypes, Model_RefInterpolationRule, \
    Model_RefRatingAlgorithm, Model_RefProvision, Model_RefStates, Model_RefTextFieldTypes, \
    Model_RefUnitCode
from ..schemas import Schema_RefRatingAlgorithm, Schema_RefStates

schema_ref_states = Schema_RefStates()
schema_ref_rating_algorithm = Schema_RefRatingAlgorithm()

schema_ref_states_list = Schema_RefStates(many=True)

class CRUD_RefRatingAlgorithm(Resource):

    @classmethod
    def get(cls, code):
        config = Model_RefRatingAlgorithm.find(code)
        return schema_ref_rating_algorithm.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = schema_ref_rating_algorithm.load(req)
        config.save_to_db()
        return schema_ref_rating_algorithm.dump(config), 201

    @classmethod
    def put(cls, code):
        req = request.get_json()
        config = schema_ref_rating_algorithm.load({**req, "rating_algorithm_code": code})
        config.save_to_db()
        return schema_ref_rating_algorithm.dump(config), 201

    @classmethod
    def delete(cls, code):
        config = Model_RefRatingAlgorithm.find(code)
        config.delete()
        return "Deleted", 204


class CRUD_RefStates(Resource):

    @classmethod
    def get(cls):
        config = Model_RefStates.find_all()
        return schema_ref_states_list.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = schema_ref_states_list.load(req)
        Model_RefStates.save_all_to_db(config)
        return schema_ref_states_list.dump(config), 201

    @classmethod
    def put(cls, code):
        req = request.get_json()
        config = schema_ref_states.load({**req, "state_code": code})
        config.save_to_db()
        return schema_ref_states.dump(config), 201

    @classmethod
    def delete(cls, code):
        config = Model_RefStates.find(code)
        config.delete()
        return "Deleted", 204
