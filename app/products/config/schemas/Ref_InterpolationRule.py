from app.extensions import ma
from app.shared import BaseSchema
from ..models import Model_RefInterpolationRule

class Schema_RefInterpolationRule(BaseSchema): 
    class Meta:
        model = Model_RefInterpolationRule
        load_instance = True
