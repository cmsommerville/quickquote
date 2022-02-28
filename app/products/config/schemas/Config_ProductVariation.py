from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProductVariation
from .Config_ProvisionStateAvailability import Schema_ConfigProvisionStateAvailability

class Schema_ConfigProductVariation(BaseSchema):
    class Meta:
        model = Model_ConfigProductVariation
        load_instance = True
        include_relationships = True
        include_fk = True

    states = ma.Nested(Schema_ConfigProvisionStateAvailability)

