from flask import request
from flask_restful import Resource

from ..models import Model_ConfigProvisionUIComponent
from ..schemas import Schema_ConfigProvisionUIComponent_CheckboxField, \
    Schema_ConfigProvisionUIComponent_TextField, Schema_ConfigProvisionUIComponent_SelectField

config_provision_ui_checkbox_schema = Schema_ConfigProvisionUIComponent_CheckboxField()
config_provision_ui_text_schema = Schema_ConfigProvisionUIComponent_TextField()
config_provision_ui_select_schema = Schema_ConfigProvisionUIComponent_SelectField()


class CRUD_ProvisionUIComponentConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigProvisionUIComponent.find_one(id)
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
        config = Model_ConfigProvisionUIComponent.find_one(id)
        config.delete()
        return "Deleted", 204
        