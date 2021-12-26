from app.extensions import db
from app.shared import BaseModel

from .__constants__ import TBL_NAMES

REF_INTERPOLATION_RULE = TBL_NAMES['REF_INTERPOLATION_RULE']


class Model_RefInterpolationRule(BaseModel):
    __tablename__ = REF_INTERPOLATION_RULE

    interpolation_rule_code = db.Column(db.String(30), primary_key=True)
