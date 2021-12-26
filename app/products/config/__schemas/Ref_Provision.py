from app.shared import BaseSchema

from ..models import Model_RefProvision

class Schema_RefProvision(BaseSchema):
    class Meta:
        model = Model_RefProvision
        load_instance = True
        include_relationships = True
        include_fk = True
