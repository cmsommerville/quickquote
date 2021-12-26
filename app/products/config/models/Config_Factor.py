from app.extensions import db
from app.shared import BaseModel

from .__constants__ import TBL_NAMES, FACTOR_DECIMAL_PRECISION

REF_COMPARISON_OPERATOR = TBL_NAMES['REF_COMPARISON_OPERATOR']
REF_INTERPOLATION_RULE = TBL_NAMES['REF_INTERPOLATION_RULE']
REF_PROVISION = TBL_NAMES['REF_PROVISION']
REF_STATE = TBL_NAMES['REF_STATE']
CONFIG_BENEFIT = TBL_NAMES['CONFIG_BENEFIT']
CONFIG_FACTOR = TBL_NAMES['CONFIG_FACTOR']
CONFIG_FACTOR_RULE = TBL_NAMES['CONFIG_FACTOR_RULE']
CONFIG_PROVISION = TBL_NAMES['CONFIG_PROVISION']


class Model_ConfigFactor(BaseModel):
    __tablename__ = CONFIG_FACTOR

    factor_id = db.Column(db.Integer, primary_key=True)
    provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION}.provision_id"), nullable=False)
    factor_priority = db.Column(db.Integer, nullable=False)
    factor_value = db.Column(db.Numeric(
        FACTOR_DECIMAL_PRECISION + 3, FACTOR_DECIMAL_PRECISION), nullable=False)
    factor_interpolation_low_value = db.Column(
        db.Numeric(FACTOR_DECIMAL_PRECISION + 3, FACTOR_DECIMAL_PRECISION))
    factor_interpolation_high_value = db.Column(
        db.Numeric(FACTOR_DECIMAL_PRECISION + 3, FACTOR_DECIMAL_PRECISION))
    factor_interpolation_rule_code = db.Column(db.String(30), db.ForeignKey(
        f"{REF_INTERPOLATION_RULE}.interpolation_rule_code"))

    factor_rules = db.relationship("Model_ConfigFactorRule", back_populates="factor")

    @classmethod
    def find_by_provision(cls, id):
        return cls.query.filter(cls.provision_id == id).all()