import decimal
from marshmallow import post_dump
from app.extensions import ma
from ..models import Model_ConfigRateGroup, Model_RefRateGroup, Model_RefRateType


class Schema_RefRateGroup(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_RefRateGroup
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_RefRateType(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_RefRateType
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_ConfigRateGroup(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigRateGroup
        load_instance = True
        include_relationships = True
        include_fk = True

    rate_type = ma.Nested(Schema_RefRateType)
    rate_group = ma.Nested(Schema_RefRateGroup)

    @post_dump(pass_many=True)
    def formatDecimal(self, data, many, **kwargs):
        if many:
            return [{k: v if type(v) != decimal.Decimal else float(v) for k, v in item.items()}
                    for item in data]
        else:
            new_data = {k: v if type(v) != decimal.Decimal else float(v)
                        for k, v in data.items()}
            return new_data

