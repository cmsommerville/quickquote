from app.shared import BaseSchema

from ..models import Model_ConfigAgeBand

class Schema_ConfigAgeBand(BaseSchema):
    class Meta:
        model = Model_ConfigAgeBand
        load_instance = True
        include_relationships = True
        include_fk = True
