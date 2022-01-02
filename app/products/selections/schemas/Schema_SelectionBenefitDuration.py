from app.shared import BaseSchema
from app.extensions import ma
from ..models import Model_SelectionBenefitDuration


class Schema_SelectionBenefitDuration(BaseSchema):
    class Meta:
        model = Model_SelectionBenefitDuration
        load_instance = True
        include_relationships = True
        include_fk = True