from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from ..models import Model_ConfigBenefit, Model_ConfigBenefitProductVariation, \
    Model_ConfigBenefitDuration, Model_ConfigBenefitDurationItems, Model_ConfigBenefitProvisionApplicability
from ..schemas import Schema_ConfigBenefit, Schema_ConfigBenefitStateAvailability, \
    Schema_ConfigBenefitDuration, Schema_ConfigBenefitDurationItems, Schema_ConfigBenefitProductVariation, \
        Schema_ConfigBenefitProvisionApplicability

config_benefit_schema = Schema_ConfigBenefit()
config_benefit_state_schema = Schema_ConfigBenefitStateAvailability()
config_benefit_duration_schema = Schema_ConfigBenefitDuration()
config_benefit_duration_items_schema = Schema_ConfigBenefitDurationItems()
config_benefit_product_variation_schema = Schema_ConfigBenefitProductVariation()
config_benefit_provision_schema = Schema_ConfigBenefitProvisionApplicability()

config_benefit_schema_list = Schema_ConfigBenefit(many=True)
config_benefit_state_schema_list = Schema_ConfigBenefitStateAvailability(many=True)
config_benefit_product_variation_schema_list = Schema_ConfigBenefitProductVariation(many=True)
config_benefit_provision_schema_list = Schema_ConfigBenefitProvisionApplicability(many=True)

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
        try: 
            config = config_benefit_schema.load(req)
            config.save_to_db()
            return config_benefit_schema.dump(config), 201
        except ValidationError:
            try: 
                config = config_benefit_schema_list.load(req)
                Model_ConfigBenefit.save_all_to_db(config)
                return config_benefit_schema_list.dump(config), 201
            except Exception as e: 
                return str(e), 400
        except Exception as e: 
            return str(e), 400

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
        config = Model_ConfigBenefit.find_child_states(id)
        return config_benefit_state_schema_list.dump(config), 200


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
        


class CRUD_BenefitProductVariationConfig(Resource):

    @classmethod
    def get(cls):
        benefit_id = request.args.get('benefit_id')
        config = Model_ConfigBenefitProductVariation.find_benefits(benefit_id)
        return config_benefit_product_variation_schema_list.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_benefit_product_variation_schema_list.load(req)
        Model_ConfigBenefitProductVariation.save_all_to_db(config)
        return config_benefit_product_variation_schema_list.dump(config), 201

    @classmethod
    def delete(cls):
        benefit_id = request.args.get('benefit_id')
        product_variation_id = request.args.get('product_variation_id')
        config = Model_ConfigBenefitProductVariation.find(benefit_id, product_variation_id)
        config.delete()
        return "Deleted", 204
        

class CRUD_BenefitProvisionConfig(Resource):

    @classmethod
    def get(cls):
        benefit_id = request.args.get('benefit_id')
        config = Model_ConfigBenefitProvisionApplicability.find_provisions(benefit_id)
        return config_benefit_provision_schema_list.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_benefit_provision_schema_list.load(req)
        Model_ConfigBenefitProvisionApplicability.save_all_to_db(config)
        return config_benefit_provision_schema_list.dump(config), 201

    @classmethod
    def delete(cls):
        benefit_id = request.args.get('benefit_id')
        provision_id = request.args.get('provision_id')
        config = Model_ConfigBenefitProvisionApplicability.find(benefit_id, provision_id)
        config.delete()
        return "Deleted", 204
        
