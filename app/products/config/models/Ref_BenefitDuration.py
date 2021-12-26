from app.extensions import db
from app.shared import BaseModel

from .__constants__ import TBL_NAMES

REF_BENEFIT_DURATION = TBL_NAMES['REF_BENEFIT_DURATION']

class Model_RefBenefitDuration(BaseModel):
    __tablename__ = REF_BENEFIT_DURATION

    duration_code = db.Column(db.String(30), primary_key=True)
    duration_label = db.Column(db.String(100))

