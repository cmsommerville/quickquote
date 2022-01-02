from app.extensions import ma
from app.shared import BaseSchema
from ..models import Model_SelectionAgeBands


class Schema_SelectionAgeBands(BaseSchema):
    class Meta:
        model = Model_SelectionAgeBands
        load_instance = True
        include_fk = True
