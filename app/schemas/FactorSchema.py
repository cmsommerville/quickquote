from app.schemas import ma
from app.models.FactorModel import FactorModel


class FactorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FactorModel
        load_instance = True
        include_fk = True
