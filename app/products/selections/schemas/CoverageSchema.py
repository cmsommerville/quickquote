from app.extensions import ma
from ..models.CoverageModel import CoverageModel


class CoverageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CoverageModel
        load_instance = True
        include_fk = True
