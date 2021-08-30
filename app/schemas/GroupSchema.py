from app.schemas import ma
from app.models.GroupModel import GroupModel


class GroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GroupModel
        load_instance = True
