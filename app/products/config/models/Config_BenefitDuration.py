from app.extensions import db
from app.shared import BaseModel

from ...__constants__ import TBL_NAMES

CONFIG_BENEFIT = TBL_NAMES['CONFIG_BENEFIT']
CONFIG_BENEFIT_DURATION = TBL_NAMES['CONFIG_BENEFIT_DURATION']
CONFIG_BENEFIT_DURATION_ITEMS = TBL_NAMES['CONFIG_BENEFIT_DURATION_ITEMS']
REF_BENEFIT_DURATION = TBL_NAMES['REF_BENEFIT_DURATION']


class Model_ConfigBenefitDuration(BaseModel):
    __tablename__ = CONFIG_BENEFIT_DURATION
    __table_args__ = (
        db.UniqueConstraint('benefit_id', 'benefit_duration_code'),
    )

    benefit_duration_id = db.Column(db.Integer, primary_key=True)
    benefit_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_BENEFIT}.benefit_id"))
    benefit_duration_code = db.Column(
        db.String(30), db.ForeignKey(f"{REF_BENEFIT_DURATION}.duration_code"))
    default_duration_item_code = db.Column(db.String(30))

    benefit = db.relationship(
        "Model_ConfigBenefit",back_populates="durations")
    duration = db.relationship("Model_RefBenefitDuration")
    duration_items = db.relationship(
        "Model_ConfigBenefitDurationItem", back_populates="duration")
    selected_duration_item = db.relationship(
        "Model_SelectionBenefitDuration", 
        primaryjoin="Model_ConfigBenefitDuration.benefit_duration_id==Model_SelectionBenefitDuration.config_benefit_duration_id")
    
    @classmethod
    def find_by_benefit(cls, id):
        return cls.query.filter(cls.benefit_id == id).all()
