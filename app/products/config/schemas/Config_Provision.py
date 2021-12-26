from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProvision
from .Ref_Provision import Schema_RefProvision

class Schema_ConfigProvision(BaseSchema):
    class Meta:
        model = Model_ConfigProvision
        load_instance = True
        include_relationships = True
        include_fk = True

    provision = ma.Nested(Schema_RefProvision)
