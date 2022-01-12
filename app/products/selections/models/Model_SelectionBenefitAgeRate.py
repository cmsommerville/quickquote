from app.extensions import db
from app.shared import BaseModel
import datetime
from sqlalchemy import func

from ...__constants__ import TBL_NAMES

SELECTION_BENEFIT_AGE_RATE = TBL_NAMES['SELECTION_BENEFIT_AGE_RATE']
SELECTION_BENEFIT_RATE = TBL_NAMES['SELECTION_BENEFIT_RATE']
SELECTION_BENEFIT = TBL_NAMES['SELECTION_BENEFIT']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']


class Model_SelectionBenefitAgeRate(BaseModel):
    __tablename__ = SELECTION_BENEFIT_AGE_RATE

    selection_benefit_age_rate_id = db.Column(db.Integer, primary_key=True)
    selection_benefit_rate_id = db.Column(db.ForeignKey(F'{SELECTION_BENEFIT_RATE}.selection_benefit_rate_id'))
    selection_benefit_id = db.Column(db.ForeignKey(F'{SELECTION_BENEFIT}.selection_benefit_id'))
    selection_plan_id = db.Column(db.ForeignKey(F'{SELECTION_PLAN}.selection_plan_id'))
    family_code = db.Column(db.String(3), nullable=False)
    smoker_status = db.Column(db.String(1), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Numeric(12, 5))
    base_premium = db.Column(db.Numeric(12, 5))
    provision_factor = db.Column(db.Numeric(12, 5))
    duration_factor = db.Column(db.Numeric(12, 5))
    discretionary_factor = db.Column(db.Numeric(12, 5))
    final_premium = db.Column(db.Numeric(12, 5))

    plan = db.relationship("Model_SelectionPlan")
    benefit = db.relationship("Model_SelectionBenefit")
    benefit_rate = db.relationship(
        "Model_SelectionBenefitRate", back_populates="benefit_age_rates")
    benefit_factors = db.relationship(
        "Model_SelectionBenefitFactor", back_populates="benefit_age_rate")

    @classmethod
    def find_by_plan(cls, plan_id):
        return cls.query.filter(cls.selection_plan_id == plan_id).all()
        
    @classmethod
    def delete_by_plan(cls, plan_id):
        try: 
            cls.query.filter(cls.selection_plan_id == plan_id).delete()
            db.session.commit()
        except Exception as e: 
            db.session.rollback()
            raise e