from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigBenefitDurationItem
from .Ref_BenefitDurationItem import Schema_RefBenefitDurationItem

class Schema_ConfigBenefitDurationItem(BaseSchema):
    class Meta:
        model = Model_ConfigBenefitDurationItem
        load_instance = True
        include_relationships = True
        include_fk = True

    duration_item = ma.Nested(Schema_RefBenefitDurationItem)
