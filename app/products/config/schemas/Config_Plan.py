import decimal
from marshmallow import post_dump
from app.extensions import ma
from ..models import Model_ConfigPlan, Model_RefProduct


class Schema_ConfigPlan(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigPlan
        load_instance = True
        include_relationships = True
        include_fk = True


class Schema_RefProduct(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_RefProduct
        load_instance = True
        include_relationships = True
        include_fk = True
