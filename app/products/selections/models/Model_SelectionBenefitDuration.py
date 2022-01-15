from app.extensions import db
from app.shared import BaseModel
import datetime

from ...__constants__ import TBL_NAMES

CONFIG_BENEFIT_DURATION = TBL_NAMES['CONFIG_BENEFIT_DURATION']
CONFIG_BENEFIT_DURATION_ITEMS = TBL_NAMES['CONFIG_BENEFIT_DURATION_ITEMS']
SELECTION_BENEFIT_DURATION = TBL_NAMES['SELECTION_BENEFIT_DURATION']
SELECTION_BENEFIT = TBL_NAMES['SELECTION_BENEFIT']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']

class Model_SelectionBenefitDuration(BaseModel):
    __tablename__ = SELECTION_BENEFIT_DURATION

    selection_benefit_duration_id = db.Column(db.Integer, primary_key=True)
    selection_benefit_id = db.Column(db.ForeignKey(f'{SELECTION_BENEFIT}.selection_benefit_id'))
    selection_plan_id = db.Column(db.ForeignKey(f'{SELECTION_PLAN}.selection_plan_id'))
    config_benefit_duration_id = db.Column(db.ForeignKey(f'{CONFIG_BENEFIT_DURATION}.benefit_duration_id'))
    config_benefit_duration_item_id = db.Column(db.ForeignKey(f'{CONFIG_BENEFIT_DURATION_ITEMS}.benefit_duration_item_id'))
    duration_data_type = db.Column(db.String(20), nullable=False)
    duration_value = db.Column(db.String(100), nullable=False)
    duration_factor = db.Column(db.Numeric(12, 7), nullable=False)

    plan = db.relationship("Model_SelectionPlan")
    benefit = db.relationship("Model_SelectionBenefit", back_populates="durations")
    
    @classmethod
    def find_by_plan(cls, plan_id):
        return cls.query.filter(cls.selection_plan_id == plan_id).all()

    @classmethod
    def find_by_benefit(cls, benefit_id):
        return cls.query.filter(cls.selection_benefit_id == benefit_id).all()

    def validate(self) -> bool:
        """
        Validate the plan
        """
        return True
