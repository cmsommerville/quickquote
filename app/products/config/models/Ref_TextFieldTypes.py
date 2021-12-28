from app.extensions import db
from app.shared import BaseModel

from ...__constants__ import TBL_NAMES

REF_TEXT_FIELD_TYPES = TBL_NAMES['REF_TEXT_FIELD_TYPES']

class Model_RefTextFieldTypes(BaseModel):
    __tablename__ = REF_TEXT_FIELD_TYPES

    type_code = db.Column(db.String(30), primary_key=True)
