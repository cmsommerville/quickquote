from app.extensions import db
from app.shared import BaseModel

from .constants import TBL_NAMES

REF_RATE_TYPE = TBL_NAMES['REF_RATE_TYPE']

class Model_RefRateType(BaseModel):
    __tablename__ = REF_RATE_TYPE

    rate_type_code = db.Column(db.String(30), primary_key=True)
    rate_type_label = db.Column(db.String(100))
