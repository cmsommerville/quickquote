from app.extensions import ma
from ..models import Model_ConfigProductVariations, Model_RefRatingAlgorithm, \
    Model_ConfigAgeBands, Model_ConfigAgeBandsSet


class Schema_ConfigProductVariations(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigProductVariations
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_ConfigAgeBandsSet(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigAgeBandsSet
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_ConfigAgeBands(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigAgeBands
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_RefRatingAlgorithm(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_RefRatingAlgorithm
        load_instance = True
        include_relationships = True
        include_fk = True
