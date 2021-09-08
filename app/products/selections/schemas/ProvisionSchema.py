from app.extensions import ma
from ..models.ProvisionModel import ProvisionModel


class ProvisionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProvisionModel
        load_instance = True
        include_fk = True
