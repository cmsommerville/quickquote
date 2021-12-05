from flask import request
from flask_restful import Resource

from ..models import Model_ConfigBenefit, Model_ConfigBenefitStateAvailability, \
    Model_ConfigBenefitDuration, Model_ConfigBenefitDurationItems
from ..schemas import Schema_ConfigBenefit, Schema_ConfigBenefitStateAvailability, \
    Schema_ConfigBenefitDuration, Schema_ConfigBenefitDurationItems

config_benefit_schema = Schema_ConfigBenefit()
config_benefit_duration_schema = Schema_ConfigBenefitDuration()
config_benefit_duration_items_schema = Schema_ConfigBenefitDurationItems()
config_benefit_state_schema = Schema_ConfigBenefitStateAvailability()

config_benefit_schema_list = Schema_ConfigBenefit(many=True)

class Resource_BenefitStateConfig(Resource):

    @classmethod
    def get(cls):
        state = request.args.get('state')
        effective_date = request.args.get('effective_date')
        product_code = request.args.get('product_code')
        res = Model_ConfigBenefit.find_by_state(state, effective_date, product_code)
        return config_benefit_schema_list.dump(res), 200


class CRUD_BenefitConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigBenefit.find(id)
        return config_benefit_schema.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_benefit_schema.load(req)
        config.save_to_db()
        return config_benefit_schema.dump(config), 201

    @classmethod
    def put(cls, id):
        req = request.get_json()
        config = config_benefit_schema.load({**req, "benefit_id": id})
        config.save_to_db()
        return config_benefit_schema.dump(config), 201

    @classmethod
    def delete(cls, id):
        config = Model_ConfigBenefit.find(id)
        config.delete()
        return "Deleted", 204
        


class CRUD_BenefitStateAvailabilityConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigBenefitStateAvailability.find(id)
        return config_benefit_state_schema.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_benefit_state_schema.load(req)
        config.save_to_db()
        return config_benefit_state_schema.dump(config), 201

    @classmethod
    def put(cls, id):
        req = request.get_json()
        config = config_benefit_state_schema.load({**req, "benefit_state_availability_id": id})
        config.save_to_db()
        return config_benefit_state_schema.dump(config), 201

    @classmethod
    def delete(cls, id):
        config = Model_ConfigBenefitStateAvailability.find(id)
        config.delete()
        return "Deleted", 204



class CRUD_BenefitDurationConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigBenefitDuration.find(id)
        return config_benefit_duration_schema.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_benefit_duration_schema.load(req)
        config.save_to_db()
        return config_benefit_duration_schema.dump(config), 201

    @classmethod
    def put(cls, id):
        req = request.get_json()
        config = config_benefit_duration_schema.load({**req, "benefit_duration_id": id})
        config.save_to_db()
        return config_benefit_duration_schema.dump(config), 201

    @classmethod
    def delete(cls, id):
        config = Model_ConfigBenefitDuration.find(id)
        config.delete()
        return "Deleted", 204
        

class CRUD_BenefitDurationItemsConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigBenefitDurationItems.find(id)
        return config_benefit_duration_items_schema.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_benefit_duration_items_schema.load(req)
        config.save_to_db()
        return config_benefit_duration_items_schema.dump(config), 201

    @classmethod
    def put(cls, id):
        req = request.get_json()
        config = config_benefit_duration_items_schema.load({**req, "benefit_duration_item_id": id})
        config.save_to_db()
        return config_benefit_duration_items_schema.dump(config), 201

    @classmethod
    def delete(cls, id):
        config = Model_ConfigBenefitDurationItems.find(id)
        config.delete()
        return "Deleted", 204
        