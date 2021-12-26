from app.extensions import db
from app.shared import BaseModel

from .constants import TBL_NAMES

REF_BENEFIT_DURATION_ITEMS = TBL_NAMES['REF_BENEFIT_DURATION_ITEMS']



class Model_RefBenefitDurationItem(BaseModel):
    __tablename__ = REF_BENEFIT_DURATION_ITEMS

    item_code = db.Column(db.String(30), primary_key=True)
    item_label = db.Column(db.String(100))
