from app.extensions import db
from app.shared import BaseModel

from .constants import TBL_NAMES, FACTOR_DECIMAL_PRECISION

CONFIG_BENEFIT_DURATION_ITEMS = TBL_NAMES['CONFIG_BENEFIT_DURATION_ITEMS']
CONFIG_BENEFIT_DURATION = TBL_NAMES['CONFIG_BENEFIT_DURATION']
REF_BENEFIT_DURATION_ITEMS = TBL_NAMES['REF_BENEFIT_DURATION_ITEMS']

class Model_ConfigBenefitDurationItem(BaseModel):
    __tablename__ = CONFIG_BENEFIT_DURATION_ITEMS
    __table_args__ = (
        db.UniqueConstraint('benefit_duration_id', 'item_code'),
    )

    benefit_duration_item_id = db.Column(db.Integer, primary_key=True)
    benefit_duration_id = db.Column(db.ForeignKey(f"{CONFIG_BENEFIT_DURATION}.benefit_duration_id"), nullable=False)
    item_code = db.Column(db.ForeignKey(f"{REF_BENEFIT_DURATION_ITEMS}.item_code"), nullable=False)
    benefit_duration_factor = db.Column(
        db.Numeric(FACTOR_DECIMAL_PRECISION + 3, FACTOR_DECIMAL_PRECISION), nullable=False)

    duration = db.relationship(
        "Model_ConfigBenefitDuration", back_populates="duration_items")

    duration_item = db.relationship("Model_RefBenefitDurationItem")
   