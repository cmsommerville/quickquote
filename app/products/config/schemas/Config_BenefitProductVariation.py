from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigBenefitProductVariation
from .Config_ProductVariation import Schema_ConfigProductVariation
from .Config_Benefit import Schema_ConfigBenefit

class Schema_ConfigBenefitProductVariation(BaseSchema):
    class Meta:
        model = Model_ConfigBenefitProductVariation
        load_instance = True
        include_relationships = True
        include_fk = True

    product_variation = ma.Nested(Schema_ConfigProductVariation)
    benefit = ma.Nested(Schema_ConfigBenefit)