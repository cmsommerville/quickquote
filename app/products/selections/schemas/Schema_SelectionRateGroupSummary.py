from app.extensions import ma
from app.shared import BaseSchema
from ..models.Model_SelectionRateGroupSummary import Model_SelectionRateGroupSummary


class Schema_SelectionRateGroupSummary(BaseSchema):
    class Meta:
        model = Model_SelectionRateGroupSummary
        load_instance = True
        include_fk = True