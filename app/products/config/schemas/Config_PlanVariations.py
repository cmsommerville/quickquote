import decimal
from marshmallow import post_dump
from app.extensions import ma
from ..models import Model_ConfigPlanVariations, Model_RefPlanVariations, Model_RefRatingAlgorithm


class Schema_ConfigPlanVariations(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigPlanVariations
        load_instance = True
        include_relationships = True
        include_fk = True


class Schema_RefPlanVariations(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_RefPlanVariations
        load_instance = True
        include_relationships = True
        include_fk = True


class Schema_RefRatingAlgorithm(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_RefRatingAlgorithm
        load_instance = True
        include_relationships = True
        include_fk = True
