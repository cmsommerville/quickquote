from app.models import ma
from .ProvisionModel import ProvisionModel


class ProvisionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProvisionModel
