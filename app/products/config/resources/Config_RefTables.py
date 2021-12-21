from flask import request
from flask_restful import Resource

from ..models import Model_RefBenefit, Model_RefBenefitDuration, Model_RefBenefitDurationItems, \
    Model_RefComparisonOperator, Model_RefComponentTypes, Model_RefInterpolationRule, \
    Model_RefRatingAlgorithm, Model_RefProvision, Model_RefStates, Model_RefTextFieldTypes, \
    Model_RefUnitCode, Model_RefRateGroup, Model_RefRateType
from ..schemas import Schema_RefRatingAlgorithm, Schema_RefStates, Schema_RefUnitCode, \
    Schema_RefRateGroup, Schema_RefRateType, Schema_RefComponentTypes, Schema_RefTextFieldTypes, \
        Schema_RefComparisonOperator, Schema_RefInterpolationRule

schema_ref_states = Schema_RefStates()
schema_ref_rating_algorithm = Schema_RefRatingAlgorithm()
schema_ref_component_types = Schema_RefComponentTypes()
schema_ref_text_field_types = Schema_RefTextFieldTypes()
schema_ref_comparison_operator = Schema_RefComparisonOperator()
schema_ref_interpolation_rule = Schema_RefInterpolationRule()

schema_ref_unit_code_list = Schema_RefUnitCode(many=True)
schema_ref_states_list = Schema_RefStates(many=True)
schema_ref_component_types_list = Schema_RefComponentTypes(many=True)
schema_ref_text_field_types_list = Schema_RefTextFieldTypes(many=True)
schema_ref_comparison_operator_list = Schema_RefComparisonOperator(many=True)
schema_ref_interpolation_rule_list = Schema_RefInterpolationRule(many=True)

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




class CRUD_RefUnitCode(Resource):

    @classmethod
    def get(cls):
        config = Model_RefUnitCode.find_all()
        return schema_ref_unit_code_list.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = schema_ref_unit_code_list.load(req)
        Model_RefUnitCode.save_all_to_db(config)
        return schema_ref_unit_code_list.dump(config), 201

    @classmethod
    def put(cls, code):
        req = request.get_json()
        config = schema_ref_unit_code_list.load({**req, "unit_code": code})
        config.save_to_db()
        return schema_ref_unit_code_list.dump(config), 201

    @classmethod
    def delete(cls, code):
        config = Model_RefUnitCode.find(code)
        config.delete()
        return "Deleted", 204




class CRUD_RefComponentTypes(Resource):

    @classmethod
    def get(cls, code):
        config = Model_RefComponentTypes.find(code)
        return schema_ref_rating_algorithm.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = schema_ref_component_types_list.load(req)
        Model_RefComponentTypes.save_all_to_db(config)
        return schema_ref_component_types_list.dump(config), 201

    @classmethod
    def put(cls, code):
        req = request.get_json()
        config = schema_ref_component_types.load({**req})
        config.save_to_db()
        return schema_ref_component_types.dump(config), 201

    @classmethod
    def delete(cls, code):
        config = Model_RefComponentTypes.find(code)
        config.delete()
        return "Deleted", 204


class CRUD_RefTextFieldTypes(Resource):

    @classmethod
    def get(cls, code):
        config = Model_RefTextFieldTypes.find(code)
        return schema_ref_text_field_types.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = schema_ref_text_field_types_list.load(req)
        Model_RefTextFieldTypes.save_all_to_db(config)
        return schema_ref_text_field_types_list.dump(config), 201

    @classmethod
    def put(cls, code):
        req = request.get_json()
        config = schema_ref_text_field_types.load({**req})
        config.save_to_db()
        return schema_ref_text_field_types.dump(config), 201

    @classmethod
    def delete(cls, code):
        config = Model_RefTextFieldTypes.find(code)
        config.delete()
        return "Deleted", 204



class CRUD_RefComparisonOperator(Resource):

    @classmethod
    def get(cls, code):
        config = Model_RefComparisonOperator.find(code)
        return schema_ref_comparison_operator.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = schema_ref_comparison_operator_list.load(req)
        Model_RefComparisonOperator.save_all_to_db(config)
        return schema_ref_comparison_operator_list.dump(config), 201

    @classmethod
    def put(cls, code):
        req = request.get_json()
        config = schema_ref_comparison_operator.load({**req, "comparison_operator_code": code})
        config.save_to_db()
        return schema_ref_comparison_operator.dump(config), 201

    @classmethod
    def delete(cls, code):
        config = Model_RefComparisonOperator.find(code)
        config.delete()
        return "Deleted", 204



class CRUD_RefInterpolationRule(Resource):

    @classmethod
    def get(cls, code):
        config = Model_RefInterpolationRule.find(code)
        return schema_ref_interpolation_rule.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = schema_ref_interpolation_rule_list.load(req)
        Model_RefInterpolationRule.save_all_to_db(config)
        return schema_ref_interpolation_rule_list.dump(config), 201

    @classmethod
    def put(cls, code):
        req = request.get_json()
        config = schema_ref_interpolation_rule.load({**req, "comparison_operator_code": code})
        config.save_to_db()
        return schema_ref_interpolation_rule.dump(config), 201

    @classmethod
    def delete(cls, code):
        config = Model_RefInterpolationRule.find(code)
        config.delete()
        return "Deleted", 204

