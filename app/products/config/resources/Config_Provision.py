from flask import request
from flask_restful import Resource

from ..models import Model_ConfigProvision, Model_ConfigProvisionStateAvailability, \
    Model_ConfigProvisionUIComponent, Model_ConfigProvisionUIComponent_CheckboxField, \
    Model_ConfigProvisionUIComponent_TextField, Model_ConfigProvisionUIComponent_SelectField, \
    Model_ConfigProvisionUIComponent_SelectItemField
from ..schemas import Schema_ConfigProvision, Schema_ConfigProvisionStateAvailability, \
    Schema_ConfigProvisionUIComponent, Schema_ConfigProvisionUIComponent_CheckboxField, \
    Schema_ConfigProvisionUIComponent_TextField, Schema_ConfigProvisionUIComponent_SelectField, \
    Schema_ConfigProvisionUIComponent_SelectItemField

config_provision_schema = Schema_ConfigProvision()
config_provision_ui_schema = Schema_ConfigProvisionUIComponent()
config_provision_ui_checkbox_schema = Schema_ConfigProvisionUIComponent_CheckboxField()
config_provision_ui_text_schema = Schema_ConfigProvisionUIComponent_TextField()
config_provision_ui_select_schema = Schema_ConfigProvisionUIComponent_SelectField()
config_provision_ui_select_item_schema = Schema_ConfigProvisionUIComponent_SelectItemField()
config_provision_state_schema = Schema_ConfigProvisionStateAvailability()

config_provision_schema_list = Schema_ConfigProvision(many=True)
config_provision_state_schema_list = Schema_ConfigProvisionStateAvailability(many=True)
config_provision_ui_select_item_schema_list = Schema_ConfigProvisionUIComponent_SelectItemField(many=True)

class Resource_ProvisionStateConfig(Resource):

    @classmethod
    def get(cls):
        state = request.args.get('state')
        effective_date = request.args.get('effective_date')
        product_code = request.args.get('product_code')
        res = Model_ConfigProvision.find_by_state(state, effective_date, product_code)
        return config_provision_schema_list.dump(res), 200


class CRUD_ProvisionConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigProvision.find(id)
        return config_provision_schema.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_provision_schema.load(req)
        config.save_to_db()
        return config_provision_schema.dump(config), 201

    @classmethod
    def put(cls, id):
        req = request.get_json()
        config = config_provision_schema.load({**req, "provision_id": id})
        config.save_to_db()
        return config_provision_schema.dump(config), 201

    @classmethod
    def delete(cls, id):
        config = Model_ConfigProvision.find(id)
        config.delete()
        return "Deleted", 204
        


class CRUD_ProvisionStateAvailabilityConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigProvisionStateAvailability.find(id)
        return config_provision_state_schema.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_provision_state_schema_list.load(req)
        Model_ConfigProvisionStateAvailability.save_all_to_db(config)
        return config_provision_state_schema_list.dump(config), 201

    @classmethod
    def put(cls, id):
        req = request.get_json()
        config = config_provision_state_schema.load({**req, "provision_state_availability_id": id})
        config.save_to_db()
        return config_provision_state_schema.dump(config), 201

    @classmethod
    def delete(cls, id):
        config = Model_ConfigProvisionStateAvailability.find(id)
        config.delete()
        return "Deleted", 204



class CRUD_ProvisionUIComponentConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigProvisionUIComponent.find(id)
        if config is None:
            return [], 200
        if config.component_type == "INPUT":
            return config_provision_ui_text_schema.dump(config), 200
        if config.component_type == "CHECKBOX":
            return config_provision_ui_checkbox_schema.dump(config), 200
        if config.component_type == "SELECT":
            return config_provision_ui_select_schema.dump(config), 200
        return "error", 404

    @classmethod
    def post(cls):
        req = request.get_json()
        component_type = req.get('component_type')

        if component_type == "INPUT":
            config = config_provision_ui_text_schema.load(req)
        elif component_type == "CHECKBOX":
            config = config_provision_ui_checkbox_schema.load(req)
        elif component_type == "SELECT":
            config = config_provision_ui_select_schema.load(req)

        config.save_to_db()

        if config.component_type == "INPUT":
            return config_provision_ui_text_schema.dump(config), 201
        if config.component_type == "CHECKBOX":
            return config_provision_ui_checkbox_schema.dump(config), 201
        if config.component_type == "SELECT":
            return config_provision_ui_select_schema.dump(config), 201

        return "error", 404

    @classmethod
    def put(cls, id):
        req = request.get_json()

        component_type = req.get('component_type')

        if component_type == "INPUT":
            config = config_provision_ui_text_schema.load({**req, "provision_id": id})
        elif component_type == "CHECKBOX":
            config = config_provision_ui_checkbox_schema.load({**req, "provision_id": id})
        elif component_type == "SELECT":
            config = config_provision_ui_select_schema.load({**req, "provision_id": id})

        config.save_to_db()

        if config.component_type == "INPUT":
            return config_provision_ui_text_schema.dump(config), 201
        if config.component_type == "CHECKBOX":
            return config_provision_ui_checkbox_schema.dump(config), 201
        if config.component_type == "SELECT":
            return config_provision_ui_select_schema.dump(config), 201
        
        return "error", 404

    @classmethod
    def delete(cls, id):
        config = Model_ConfigProvisionUIComponent.find(id)
        config.delete()
        return "Deleted", 204
        

class CRUD_ProvisionUIComponent_CheckboxConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigProvisionUIComponent_CheckboxField.find(id)
        return config_provision_ui_checkbox_schema.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_provision_ui_checkbox_schema.load(req)
        config.save_to_db()
        return config_provision_ui_checkbox_schema.dump(config), 201

    @classmethod
    def put(cls, id):
        req = request.get_json()
        config = config_provision_ui_checkbox_schema.load({**req, "provision_id": id})
        config.save_to_db()
        return config_provision_ui_checkbox_schema.dump(config), 201

    @classmethod
    def delete(cls, id):
        config = Model_ConfigProvisionUIComponent_CheckboxField.find(id)
        config.delete()
        return "Deleted", 204
        
class CRUD_ProvisionUIComponent_TextFieldConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigProvisionUIComponent_TextField.find(id)
        return config_provision_ui_text_schema.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_provision_ui_text_schema.load(req)
        config.save_to_db()
        return config_provision_ui_text_schema.dump(config), 201

    @classmethod
    def put(cls, id):
        req = request.get_json()
        config = config_provision_ui_text_schema.load({**req, "provision_id": id})
        config.save_to_db()
        return config_provision_ui_text_schema.dump(config), 201

    @classmethod
    def delete(cls, id):
        config = Model_ConfigProvisionUIComponent_TextField.find(id)
        config.delete()
        return "Deleted", 204
        
class CRUD_ProvisionUIComponent_SelectConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigProvisionUIComponent_SelectField.find(id)
        return config_provision_ui_select_schema.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_provision_ui_select_schema.load(req)
        config.save_to_db()
        return config_provision_ui_select_schema.dump(config), 201

    @classmethod
    def put(cls, id):
        req = request.get_json()
        config = config_provision_ui_select_schema.load({**req, "provision_id": id})
        config.save_to_db()
        return config_provision_ui_select_schema.dump(config), 201

    @classmethod
    def delete(cls, id):
        config = Model_ConfigProvisionUIComponent_SelectField.find(id)
        config.delete()
        return "Deleted", 204
        
class CRUD_ProvisionUIComponent_SelectItemConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigProvisionUIComponent_SelectItemField.find(id)
        return config_provision_ui_select_item_schema.dump(config), 200

    @classmethod
    def post(cls):
        req = request.get_json()
        config = config_provision_ui_select_item_schema_list.load(req)
        Model_ConfigProvisionUIComponent_SelectItemField.save_all_to_db(config)
        return config_provision_ui_select_item_schema_list.dump(config), 201

    @classmethod
    def put(cls, id):
        req = request.get_json()
        config = config_provision_ui_select_item_schema.load({**req, "ui_component_item_id": id})
        config.save_to_db()
        return config_provision_ui_select_item_schema.dump(config), 201

    @classmethod
    def delete(cls, id):
        config = Model_ConfigProvisionUIComponent_SelectItemField.find(id)
        config.delete()
        return "Deleted", 204
        