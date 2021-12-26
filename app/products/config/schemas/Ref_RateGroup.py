from app.shared import BaseSchema

from ..models import Model_RefRateGroup

class Schema_RefRateGroup(BaseSchema):
    class Meta:
        model = Model_RefRateGroup
        load_instance = True
        include_relationships = True
        include_fk = True
