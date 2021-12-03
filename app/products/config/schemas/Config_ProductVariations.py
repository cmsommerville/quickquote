from app.extensions import ma
from ..models import Model_ConfigProductVariations, Model_RefRatingAlgorithm


class Schema_ConfigProductVariations(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigProductVariations
        load_instance = True
        include_relationships = True
        include_fk = True


class Schema_RefRatingAlgorithm(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_RefRatingAlgorithm
        load_instance = True
        include_relationships = True
        include_fk = True
