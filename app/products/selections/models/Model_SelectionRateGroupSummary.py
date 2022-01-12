from app.extensions import db
from app.shared import BaseModel

from ...__constants__ import TBL_NAMES

CONFIG_RATE_GROUP = TBL_NAMES['CONFIG_RATE_GROUP']
SELECTION_AGE_BANDS = TBL_NAMES['SELECTION_AGE_BANDS']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']
SELECTION_RATE_GROUP_SUMMARY = TBL_NAMES['SELECTION_RATE_GROUP_SUMMARY']

class Model_SelectionRateGroupSummary(BaseModel):
    __tablename__ = SELECTION_RATE_GROUP_SUMMARY

    selection_rate_group_summary_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(db.ForeignKey(f'{SELECTION_PLAN}.selection_plan_id'))
    selection_age_band_id = db.Column(db.ForeignKey(f'{SELECTION_AGE_BANDS}.selection_age_band_id'))
    config_rate_group_id = db.Column(db.ForeignKey(f'{CONFIG_RATE_GROUP}.rate_group_id'), nullable=False)
    family_code = db.Column(db.String(3), nullable=False)
    smoker_status = db.Column(db.String(1), nullable=False)
    gender=db.Column(db.String(1), nullable=False)
    rate_group_premium = db.Column(db.Numeric(12, 5), nullable=False)

    plan = db.relationship("Model_SelectionPlan")
    age_band = db.relationship("Model_SelectionAgeBands")
    benefit_rates = db.relationship(
        "Model_SelectionBenefitRate", back_populates="rate_group_summary")

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