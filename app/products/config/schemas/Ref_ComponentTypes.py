from marshmallow import validate
from app.extensions import ma
from app.shared import BaseSchema
from ..models import Model_RefComponentTypes
from .__constants__ import ENUM_ComponentTypes

class Schema_RefComponentTypes(BaseSchema): 
    class Meta:
        model = Model_RefComponentTypes
        load_instance = True

    component_type_code = ma.String()
    component_type_label = ma.String()
    component_type_enum = ma.String(validate=validate.OneOf(ENUM_ComponentTypes))

    