from app.extensions import db
from app.shared import BaseModel

from .__constants__ import TBL_NAMES

REF_COMPONENT_TYPES = TBL_NAMES['REF_COMPONENT_TYPES']

class Model_RefComponentTypes(BaseModel):
    __tablename__ = REF_COMPONENT_TYPES

    component_type_code = db.Column(db.String(50), primary_key=True)
    component_type_label = db.Column(db.String(100), nullable=False)
    component_type_enum = db.Column(db.String(50), nullable=False)
