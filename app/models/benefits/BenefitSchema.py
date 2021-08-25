from app.models import ma
from .BenefitModel import BenefitModel


class BenefitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BenefitModel
