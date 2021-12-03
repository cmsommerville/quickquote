from app.extensions import ma
from ..models import Model_ConfigProduct


class Schema_ConfigProduct(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigProduct
        load_instance = True
        include_relationships = True
        include_fk = True

