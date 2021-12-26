from app.shared import BaseSchema

from ..models import Model_RefBenefitDurationItem

class Schema_RefBenefitDurationItem(BaseSchema):
    class Meta:
        model = Model_RefBenefitDurationItem
        load_instance = True
        include_relationships = True
        include_fk = True
