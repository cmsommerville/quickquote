from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigAgeBandSet
from .Config_AgeBand import Schema_ConfigAgeBand
from .Ref_States import Schema_RefStates
from .Config_ProductVariation import Schema_ConfigProductVariation

class Schema_ConfigAgeBandSet(BaseSchema):
    class Meta:
        model = Model_ConfigAgeBandSet
        load_instance = True
        include_relationships = True
        include_fk = True

    product_variation = ma.Nested(Schema_ConfigProductVariation)
    age_bands = ma.List(ma.Nested(Schema_ConfigAgeBand))
    state = ma.Nested(Schema_RefStates)
