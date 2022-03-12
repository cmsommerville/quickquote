from app.extensions import db
from app.shared import BaseModel

from ...__constants__ import TBL_NAMES

CONFIG_RATE_TABLE = TBL_NAMES['CONFIG_RATE_TABLE']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
CONFIG_PRODUCT_VARIATIONS = TBL_NAMES['CONFIG_PRODUCT_VARIATIONS']
CONFIG_BENEFIT = TBL_NAMES['CONFIG_BENEFIT']
REF_STATE = TBL_NAMES['REF_STATE']


class Model_ConfigRateTable(BaseModel):
    __tablename__ = CONFIG_RATE_TABLE

    __table_args__ = (
        db.UniqueConstraint('product_id', 'product_variation_id', 'benefit_id', 'state_id', 'age', 'smoker_status_code', 'gender_code', 'family_code'),
    )

    rate_table_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT}.product_id"), nullable=False)
    product_variation_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT_VARIATIONS}.product_variation_id"), nullable=False)
    benefit_id = db.Column(db.ForeignKey(f"{CONFIG_BENEFIT}.benefit_id"), nullable=False)
    state_id = db.Column(db.ForeignKey(f"{REF_STATE}.state_id"), nullable=False)

    age = db.Column(db.Integer, nullable=False)
    smoker_status_code = db.Column(db.String(30), nullable=False)
    gender_code = db.Column(db.String(30), nullable=False)
    family_code = db.Column(db.String(30), nullable=False)

    annual_rate_per_unit = db.Column(db.Numeric(12, 5))
    unit_value = db.Column(db.Numeric(12, 2))


    product = db.relationship(
        "Model_ConfigProduct")
    product_variation = db.relationship(
        "Model_ConfigProductVariation")
    state = db.relationship("Model_RefStates")
    benefit = db.relationship("Model_ConfigBenefit")
