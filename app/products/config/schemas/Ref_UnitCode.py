from app.shared import BaseSchema

from ..models import Model_RefUnitCode

class Schema_RefUnitCode(BaseSchema):
    class Meta:
        model = Model_RefUnitCode
        load_instance = True
        include_relationships = True
        include_fk = True
