from app.products.config.models.Config_Provision import Model_ConfigProvisionStateAvailability
from flask import request
from flask_restful import Resource

from ..models import Model_ConfigProvision, Model_RefComponentTypes, Model_ConfigProvisionStateAvailability
from ..schemas import Schema_ConfigProvision, Schema_RefComponentTypes,  Schema_ConfigProvisionStateAvailability

config_schema = Schema_ConfigProvision()
config_schema_list = Schema_ConfigProvision(many=True)
config_provision_state_schema_list = Schema_ConfigProvisionStateAvailability(many=True)

ref_component_type_schema_list = Schema_RefComponentTypes(many=True)

class Query_AllProvisions(Resource):

    @classmethod
    def get(cls):
        product_id = request.args.get('product_id')
        res = Model_ConfigProvision.find_by_product(product_id)
        return config_schema_list.dump(res), 200

class Query_AllProvisionStates(Resource):

    @classmethod
    def get(cls):
        provision_id = request.args.get('provision_id')
        res = Model_ConfigProvisionStateAvailability.find_by_provision(provision_id)
        return config_provision_state_schema_list.dump(res), 200

class Query_AllUIComponents(Resource):

    @classmethod
    def get(cls):
        res = Model_RefComponentTypes.find_all()
        return ref_component_type_schema_list.dump(res), 200


class Query_ProvisionStateConfig(Resource):

    @classmethod
    def get(cls):
        product_id = request.args.get('product_id')
        state = request.args.get('state')
        effective_date = request.args.get('effective_date')
        res = Model_ConfigProvision.find_by_state(state, effective_date, product_id)
        return config_schema_list.dump(res), 200
