from app.extensions import db
from app.shared import BaseModel

from .__constants__ import TBL_NAMES

REF_COMPARISON_OPERATOR = TBL_NAMES['REF_COMPARISON_OPERATOR']
CONFIG_FACTOR = TBL_NAMES['CONFIG_FACTOR']
CONFIG_FACTOR_RULE = TBL_NAMES['CONFIG_FACTOR_RULE']


class Model_ConfigFactorRule(BaseModel):
    __tablename__ = CONFIG_FACTOR_RULE

    factor_rule_id = db.Column(db.Integer, primary_key=True)
    factor_id = db.Column(db.ForeignKey(f"{CONFIG_FACTOR}.factor_id"))
    class_name = db.Column(db.String(100))
    field_name = db.Column(db.String(100), nullable=False)
    comparison_operator_code = db.Column(db.String(10), db.ForeignKey(
        f"{REF_COMPARISON_OPERATOR}.comparison_operator_code"), nullable=False)
    field_value = db.Column(db.String(100), nullable=False)
    field_value_data_type = db.Column(db.String(100), nullable=False)

    factor = db.relationship('Model_ConfigFactor', back_populates="factor_rules")