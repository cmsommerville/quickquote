from app.extensions import ma
from ..models import Model_RefProvision, Model_ConfigProvision, Model_ConfigProvisionUIComponent, \
    Model_ConfigProvisionUIComponent_SelectField, Model_ConfigProvisionStateAvailability, \
    Model_ConfigProvisionUIComponent_CheckboxField, Model_ConfigProvisionUIComponent_SelectItemField, \
    Model_ConfigProvisionUIComponent_TextField

class Schema_RefProvision(ma.SQLAlchemyAutoSchema): 
    class Meta:
        model = Model_RefProvision
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

class Schema_ConfigProvisionUIComponent_SelectField(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigProvisionUIComponent_SelectField
        load_instance = True
        include_relationships = True
        include_fk = True


class Schema_ConfigProvisionUIComponent_SelectItemField(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigProvisionUIComponent_SelectItemField
        load_instance = True
        include_relationships = True
        include_fk = True

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
        