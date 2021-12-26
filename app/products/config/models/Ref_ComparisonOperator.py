from app.extensions import db
from app.shared import BaseModel

from .__constants__ import TBL_NAMES

REF_COMPARISON_OPERATOR = TBL_NAMES['REF_COMPARISON_OPERATOR']

class Model_RefComparisonOperator(BaseModel):
    __tablename__ = REF_COMPARISON_OPERATOR

    comparison_operator_code = db.Column(db.String(10), primary_key=True)
    comparison_operator_label = db.Column(db.String(100))
    comparison_operator_symbol = db.Column(db.String(100))
