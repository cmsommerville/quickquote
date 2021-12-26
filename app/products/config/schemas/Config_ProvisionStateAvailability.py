from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProvisionStateAvailability
from .Config_Provision import Schema_ConfigProvision
from .Ref_States import Schema_RefStates


class Schema_ConfigProvisionStateAvailability(BaseSchema):
    class Meta:
        model = Model_ConfigProvisionStateAvailability
        load_instance = True
        include_relationships = True
        include_fk = True

    provision = ma.Nested(Schema_ConfigProvision)
    state = ma.Nested(Schema_RefStates)
