from app.extensions import ma
from app.shared import BaseSchema
from ..models import Model_SelectionDistribution


class Schema_SelectionDistribution(BaseSchema):
    class Meta:
        model = Model_SelectionDistribution
        load_instance = True
        include_fk = True