from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProvision
from .Config_ProvisionStateAvailability import Schema_ConfigProvisionStateAvailability

class Schema_ConfigProvision(BaseSchema):
    class Meta:
        model = Model_ConfigProvision
        load_instance = True
        include_relationships = True
        include_fk = True

    states = ma.List(ma.Nested(Schema_ConfigProvisionStateAvailability))