from flask import request
from flask_restful import Resource

from ..models import Model_ConfigFactor, Model_RefInterpolationRule, Model_RefComparisonOperator, \
    Model_ConfigFactorRule, Model_ConfigBenefitFactorApplicability
from ..schemas import Schema_ConfigFactor, Schema_RefInterpolationRule, Schema_RefComparisonOperator, \
    Schema_ConfigFactorRule, Schema_ConfigBenefitFactorApplicability

schema_factor = Schema_ConfigFactor()
schema_factor_rule = Schema_ConfigFactorRule(many=True)

schema_factor_list = Schema_ConfigFactor(many=True)
schema_benefit_factor_applicability = Schema_ConfigBenefitFactorApplicability(many=True)
schema_factor_rule_list = Schema_ConfigFactorRule(many=True)


class CRUD_FactorConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigFactor.find(id)
        return schema_factor.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = schema_factor_list.load(req)
        Model_ConfigFactor.save_all_to_db(config)
        return schema_factor_list.dump(config), 201

    @classmethod
    def put(cls, id):
        req = request.get_json()
        config = schema_factor.load({**req, "factor_id": id})
        config.save_to_db()
        return schema_factor.dump(config), 201

    @classmethod
    def delete(cls, id):
        config = Model_ConfigFactor.find(id)
        config.delete()
        return "Deleted", 204
        


class CRUD_FactorRuleConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigFactorRule.find(id)
        return schema_factor_rule.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = schema_factor_rule_list.load(req)
        Model_ConfigFactorRule.save_all_to_db(config)
        return schema_factor_rule_list.dump(config), 201

    @classmethod
    def put(cls, id):
        req = request.get_json()
        config = schema_factor_rule.load({**req, "factor_rule_id": id})
        config.save_to_db()
        return schema_factor_rule.dump(config), 201

    @classmethod
    def delete(cls, id):
        config = Model_ConfigFactorRule.find(id)
        config.delete()
        return "Deleted", 204
