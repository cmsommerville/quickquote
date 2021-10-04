import decimal
from marshmallow import post_dump
from app.extensions import ma
from ..models.PlanRateModel import PlanRateModel


class PlanRateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PlanRateModel
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
