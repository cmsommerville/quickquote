from app.extensions import ma
from app.shared import BaseSchema
from ..models import Model_RefComparisonOperator

class Schema_RefComparisonOperator(BaseSchema): 
    class Meta:
        model = Model_RefComparisonOperator
        load_instance = True
