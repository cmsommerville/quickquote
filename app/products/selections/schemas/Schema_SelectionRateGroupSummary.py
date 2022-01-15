from app.extensions import ma
from app.shared import BaseSchema
from ..models.Model_SelectionRateGroupSummary import Model_SelectionRateGroupSummary
from .Schema_SelectionAgeBands import Schema_SelectionAgeBands


class Schema_SelectionRateGroupSummary(BaseSchema):
    class Meta:
        model = Model_SelectionRateGroupSummary
        load_instance = True
        include_fk = True

    age_band = ma.Nested(Schema_SelectionAgeBands)