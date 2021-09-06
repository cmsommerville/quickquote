from app.schemas import ma
from app.models.BenefitModel import BenefitModel


class BenefitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BenefitModel
        load_instance = True
        include_fk = True
