from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigBenefitDuration
from .Config_Benefit import Schema_ConfigBenefit
from .Config_BenefitDurationItem import Schema_ConfigBenefitDurationItem
from .Ref_BenefitDuration import Schema_RefBenefitDuration

class Schema_ConfigBenefitDuration(BaseSchema):
    class Meta:
        model = Model_ConfigBenefitDuration
        load_instance = True
        include_relationships = True
        include_fk = True

    benefit = ma.Nested(Schema_ConfigBenefit)
    duration = ma.Nested(Schema_RefBenefitDuration)
    duration_items = ma.List(ma.Nested(Schema_ConfigBenefitDurationItem))
