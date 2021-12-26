from app.extensions import db
from app.shared import BaseModel

from .__constants__ import TBL_NAMES

REF_RATE_GROUP = TBL_NAMES['REF_RATE_GROUP']

class Model_RefRateGroup(BaseModel):
    __tablename__ = REF_RATE_GROUP

    rate_group_code = db.Column(db.String(30), primary_key=True)
    rate_group_label = db.Column(db.String(100))
