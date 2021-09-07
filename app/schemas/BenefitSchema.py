import decimal
from marshmallow import post_dump
from app.schemas import ma
from app.models.BenefitModel import BenefitModel


class BenefitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BenefitModel
        load_instance = True
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
