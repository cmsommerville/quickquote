from app.schemas import ma
from app.models.CoverageModel import CoverageModel


class CoverageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CoverageModel
        load_instance = True
        include_fk = True
