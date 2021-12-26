from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProvisionUIComponent, Model_ConfigProvisionUIComponent_SelectItemField, \
    Model_ConfigProvisionUIComponent_SelectField, Model_ConfigProvisionUIComponent_CheckboxField, \
    Model_ConfigProvisionUIComponent_TextField


class Schema_ConfigProvisionUIComponent(BaseSchema):
    class Meta:
        model = Model_ConfigProvisionUIComponent
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_ConfigProvisionUIComponent_SelectItemField(BaseSchema):
    class Meta:
        model = Model_ConfigProvisionUIComponent_SelectItemField
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_ConfigProvisionUIComponent_SelectField(BaseSchema):
    class Meta:
        model = Model_ConfigProvisionUIComponent_SelectField
        load_instance = True
        include_relationships = True
        include_fk = True

    items = ma.List(ma.Nested(Schema_ConfigProvisionUIComponent_SelectItemField))


class Schema_ConfigProvisionUIComponent_CheckboxField(BaseSchema):
    class Meta:
        model = Model_ConfigProvisionUIComponent_CheckboxField
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_ConfigProvisionUIComponent_TextField(BaseSchema):
    class Meta:
        model = Model_ConfigProvisionUIComponent_TextField
        load_instance = True
        include_relationships = True
        include_fk = True
        