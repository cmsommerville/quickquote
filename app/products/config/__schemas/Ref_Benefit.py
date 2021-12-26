from app.shared import BaseSchema

from ..models import Model_RefBenefit

class Schema_RefBenefit(BaseSchema):
    class Meta:
        model = Model_RefBenefit
        load_instance = True
        include_relationships = True
        include_fk = True
