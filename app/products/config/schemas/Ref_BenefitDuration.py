from app.shared import BaseSchema

from ..models import Model_RefBenefitDuration

class Schema_RefBenefitDuration(BaseSchema):
    class Meta:
        model = Model_RefBenefitDuration
        load_instance = True
        include_relationships = True
        include_fk = True
