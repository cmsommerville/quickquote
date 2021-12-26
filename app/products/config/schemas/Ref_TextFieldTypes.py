from app.shared import BaseSchema

from ..models import Model_RefTextFieldTypes

class Schema_RefTextFieldTypes(BaseSchema): 
    class Meta:
        model = Model_RefTextFieldTypes
        load_instance = True