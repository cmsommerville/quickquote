from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProvisionStateAvailability
from .Ref_States import Schema_RefStates


class Schema_ConfigProvisionStateAvailability(BaseSchema):
    class Meta:
        model = Model_ConfigProvisionStateAvailability
        load_instance = True
        include_relationships = True
        include_fk = True

    state_code = ma.Function(lambda obj: getattr(obj.state, "state_code"))
    state_name = ma.Function(lambda obj: getattr(obj.state, "state_name"))
