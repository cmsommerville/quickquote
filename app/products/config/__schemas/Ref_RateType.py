from app.shared import BaseSchema

from ..models import Model_RefRateType

class Schema_RefRateType(BaseSchema):
    class Meta:
        model = Model_RefRateType
        load_instance = True
        include_relationships = True
        include_fk = True
