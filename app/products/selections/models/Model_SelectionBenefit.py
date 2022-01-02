from app.extensions import db
from app.shared import BaseModel
import datetime

from ...__constants__ import TBL_NAMES

CONFIG_BENEFIT = TBL_NAMES['CONFIG_BENEFIT']
CONFIG_RATE_GROUP = TBL_NAMES['CONFIG_RATE_GROUP']
SELECTION_BENEFIT = TBL_NAMES['SELECTION_BENEFIT']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']



class Model_SelectionBenefit(BaseModel):
    __tablename__ = SELECTION_BENEFIT

    selection_benefit_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(db.Integer, db.ForeignKey(f'{SELECTION_PLAN}.selection_plan_id'))
    config_benefit_id = db.Column(db.ForeignKey(f'{CONFIG_BENEFIT}.benefit_id'), nullable=False)
    config_rate_group_id = db.Column(db.ForeignKey(f'{CONFIG_RATE_GROUP}.rate_group_id'), nullable=False)
    benefit_value = db.Column(db.Numeric(12, 4), nullable=False)

    plan = db.relationship("Model_SelectionPlan", back_populates="benefits")
    durations = db.relationship("Model_SelectionBenefitDuration", back_populates="benefit")
    benefit_rates = db.relationship(
        "Model_SelectionBenefitRate", back_populates="benefit")
    config_benefit = db.relationship(
        "Model_ConfigBenefit", back_populates="selected_benefit")

    @classmethod
    def find_by_plan(cls, plan_id):
        return cls.query.filter(cls.selection_plan_id == plan_id).all()
