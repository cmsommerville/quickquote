from app.extensions import ma
from app.shared import BaseSchema
from ..models.Model_SelectionBenefitRate import Model_SelectionBenefitRate


class Schema_SelectionBenefitRate(BaseSchema):
    class Meta:
        model = Model_SelectionBenefitRate
        load_instance = True
        include_fk = True