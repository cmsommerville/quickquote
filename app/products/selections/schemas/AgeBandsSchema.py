from app.extensions import ma
from ..models.AgeBandsModel import AgeBandsModel


class AgeBandsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AgeBandsModel
        load_instance = True
        include_fk = True
