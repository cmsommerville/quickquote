from app.extensions import db
from app.shared import BaseModel

from ...__constants__ import TBL_NAMES

REF_BENEFIT = TBL_NAMES['REF_BENEFIT']



class Model_RefBenefit(BaseModel):
    __tablename__ = REF_BENEFIT

    benefit_code = db.Column(db.String(30), primary_key=True)
    benefit_label = db.Column(db.String(100))
