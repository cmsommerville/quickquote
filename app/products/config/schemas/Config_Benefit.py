import decimal
from marshmallow import post_dump
from app.extensions import ma
from ..models import Model_ConfigBenefit, Model_ConfigBenefitDuration, \
    Model_ConfigBenefitDurationItems, \
    Model_RefBenefit, Model_RefBenefitDuration, Model_RefBenefitDurationItems, \
    Model_RefUnitCode



class Schema_RefBenefit(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_RefBenefit
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_RefBenefitDuration(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_RefBenefitDuration
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_RefBenefitDurationItems(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_RefBenefitDurationItems
        load_instance = True
        include_relationships = True
        include_fk = True

class Schema_RefUnitCode(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_RefUnitCode
        load_instance = True
        include_relationships = True
        include_fk = True



class Schema_ConfigBenefit(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigBenefit
        load_instance = True
        include_relationships = True
        include_fk = True

    benefit = ma.Nested(Schema_RefBenefit)

    @post_dump(pass_many=True)
    def formatDecimal(self, data, many, **kwargs):
        if many:
            return [{k: v if type(v) != decimal.Decimal else float(v) for k, v in item.items()}
                    for item in data]
        else:
            new_data = {k: v if type(v) != decimal.Decimal else float(v)
                        for k, v in data.items()}
            return new_data


class Schema_ConfigBenefitDuration(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigBenefitDuration
        load_instance = True
        include_relationships = True
        include_fk = True

    @post_dump(pass_many=True)
    def formatDecimal(self, data, many, **kwargs):
        if many:
            return [{k: v if type(v) != decimal.Decimal else float(v) for k, v in item.items()}
                    for item in data]
        else:
            new_data = {k: v if type(v) != decimal.Decimal else float(v)
                        for k, v in data.items()}
            return new_data

class Schema_ConfigBenefitDurationItems(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model_ConfigBenefitDurationItems
        load_instance = True
        include_relationships = True
        include_fk = True

    @post_dump(pass_many=True)
    def formatDecimal(self, data, many, **kwargs):
        if many:
            return [{k: v if type(v) != decimal.Decimal else float(v) for k, v in item.items()}
                    for item in data]
        else:
            new_data = {k: v if type(v) != decimal.Decimal else float(v)
                        for k, v in data.items()}
            return new_data

