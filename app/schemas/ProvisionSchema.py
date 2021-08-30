from app.schemas import ma
from app.models.ProvisionModel import ProvisionModel


class ProvisionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProvisionModel
        load_instance = True
        include_fk = True
