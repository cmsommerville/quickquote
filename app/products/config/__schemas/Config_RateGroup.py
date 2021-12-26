from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigRateGroup
from .Config_Product import Schema_ConfigProduct
from .Ref_RateType import Schema_RefRateType
from .Ref_RateGroup import Schema_RefRateGroup

class Schema_ConfigRateGroup(BaseSchema):
    class Meta:
        model = Model_ConfigRateGroup
        load_instance = True
        include_relationships = True
        include_fk = True

    product = ma.Nested(Schema_ConfigProduct)
    rate_group = ma.Nested(Schema_RefRateGroup)
    rate_type = ma.Nested(Schema_RefRateType)
