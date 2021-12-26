from app.extensions import db
from app.shared import BaseModel

from .__constants__ import TBL_NAMES

REF_UNIT_CODE = TBL_NAMES['REF_UNIT_CODE']


class Model_RefUnitCode(BaseModel):
    __tablename__ = REF_UNIT_CODE

    unit_code = db.Column(db.String(30), primary_key=True)
    unit_label = db.Column(db.String(100))
