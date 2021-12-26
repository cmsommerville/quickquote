from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProduct
from .Config_ProductStateAvailability import Schema_ConfigProductStateAvailability

class Schema_ConfigProduct(BaseSchema):
    class Meta:
        model = Model_ConfigProduct
        load_instance = True
        include_relationships = True
        include_fk = True

    states = ma.List(ma.Nested(Schema_ConfigProductStateAvailability))

