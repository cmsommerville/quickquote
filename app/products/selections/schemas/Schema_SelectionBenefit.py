from app.shared import BaseSchema
from app.extensions import ma
from ..models import Model_SelectionBenefit
from .Schema_SelectionBenefitDuration import Schema_SelectionBenefitDuration


class Schema_SelectionBenefit(BaseSchema):
    class Meta:
        model = Model_SelectionBenefit
        load_instance = True
        include_relationships = True
        include_fk = True

    durations = ma.List(ma.Nested(Schema_SelectionBenefitDuration))