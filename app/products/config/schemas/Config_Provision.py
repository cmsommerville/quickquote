from app.extensions import ma
from app.products.config.models.Config_Provision import Model_RefTextFieldTypes
from marshmallow import validate
from .constants import ENUM_ComponentTypes
from app.products.config.models.Config_Factor import Model_RefComparisonOperator
from ..models import Model_RefProvision, Model_ConfigProvision, Model_ConfigProvisionUIComponent, \
    Model_ConfigProvisionUIComponent_SelectField, Model_ConfigProvisionStateAvailability, \
    Model_ConfigProvisionUIComponent_CheckboxField, Model_ConfigProvisionUIComponent_SelectItemField, \
    Model_ConfigProvisionUIComponent_TextField, Model_RefComponentTypes

class Schema_RefProvision(ma.SQLAlchemyAutoSchema): 
    class Meta:
        model = Model_RefProvision
        load_instance = True
    


class Schema_RefComponentTypes(ma.SQLAlchemyAutoSchema): 
    class Meta:
        model = Model_RefComponentTypes
        load_instance = True

    component_type_code = ma.String()
    component_type_label = ma.String()
    component_type_enum = ma.String(validate=validate.OneOf(ENUM_ComponentTypes))

    
class Schema_RefTextFieldTypes(ma.SQLAlchemyAutoSchema): 
    class Meta:
        model = Model_RefTextFieldTypes
        load_instance = True
    
class Schema_RefComparisonOperator(ma.SQLAlchemyAutoSchema): 
    class Meta:
        model = Model_RefComparisonOperator
        load_instance = True
    
class Schema_ConfigProvision(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigProvision
        load_instance = True
        include_relationships = True
        include_fk = True

    provision = ma.Nested(Schema_RefProvision)

class Schema_ConfigProvisionStateAvailability(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigProvisionStateAvailability
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_ConfigProvisionUIComponent(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigProvisionUIComponent
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_ConfigProvisionUIComponent_SelectItemField(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigProvisionUIComponent_SelectItemField
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_ConfigProvisionUIComponent_SelectField(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigProvisionUIComponent_SelectField
        load_instance = True
        include_relationships = True
        include_fk = True

    items = ma.List(ma.Nested(Schema_ConfigProvisionUIComponent_SelectItemField))


class Schema_ConfigProvisionUIComponent_CheckboxField(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigProvisionUIComponent_CheckboxField
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_ConfigProvisionUIComponent_TextField(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigProvisionUIComponent_TextField
        load_instance = True
        include_relationships = True
        include_fk = True
        