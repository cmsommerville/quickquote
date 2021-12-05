from app.extensions import ma
from ..models import Model_ConfigProduct, Model_ConfigProductStateAvailability


class Schema_ConfigProduct(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigProduct
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_ConfigProductStateAvailability(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigProductStateAvailability
        load_instance = True
        include_relationships = True
        include_fk = True

