from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProductStateAvailability
from .Ref_States import Schema_RefStates


class Schema_ConfigProductStateAvailability(BaseSchema):
    class Meta:
        model = Model_ConfigProductStateAvailability
        load_instance = True
        include_relationships = True
        include_fk = True

    state = ma.Nested(Schema_RefStates)
