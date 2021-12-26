from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigRateGroup
from .Ref_RateGroup import Schema_RefRateGroup
from .Ref_RateType import Schema_RefRateType


class Schema_ConfigRateGroup(BaseSchema):
    class Meta:
        model = Model_ConfigRateGroup
        load_instance = True
        include_relationships = True
        include_fk = True

    rate_type = ma.Nested(Schema_RefRateType)
    rate_group = ma.Nested(Schema_RefRateGroup)
