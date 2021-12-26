from app.extensions import ma
from app.shared import BaseSchema
from ..models import Model_ConfigProduct


class Schema_ConfigProduct(BaseSchema):
    class Meta:
        model = Model_ConfigProduct
        load_instance = True
        include_relationships = True
        include_fk = True


class Schema_ConfigProduct_FK(BaseSchema):
    class Meta:
        model = Model_ConfigProduct
        load_instance = True
