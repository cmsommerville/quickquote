from app.schemas import ma
from app.models.GroupModel import GroupModel
from marshmallow import post_load


class GroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GroupModel
        load_instance = True
