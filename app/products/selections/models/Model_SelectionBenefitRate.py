from app.extensions import db
from app.shared import BaseModel
from sqlalchemy import func

from ...__constants__ import TBL_NAMES

CONFIG_RATE_GROUP = TBL_NAMES['CONFIG_RATE_GROUP']
SELECTION_AGE_BANDS = TBL_NAMES['SELECTION_AGE_BANDS']
SELECTION_BENEFIT = TBL_NAMES['SELECTION_BENEFIT']
SELECTION_BENEFIT_RATE = TBL_NAMES['SELECTION_BENEFIT_RATE']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']


class Model_SelectionBenefitRate(BaseModel):
    __tablename__ = SELECTION_BENEFIT_RATE

    selection_benefit_rate_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(db.ForeignKey(f'{SELECTION_PLAN}.selection_plan_id'))
    selection_benefit_id = db.Column(db.ForeignKey(f'{SELECTION_BENEFIT}.selection_benefit_id'))
    selection_age_band_id = db.Column(db.ForeignKey(f'{SELECTION_AGE_BANDS}.selection_age_band_id'))
    config_rate_group_id = db.Column(db.ForeignKey(f'{CONFIG_RATE_GROUP}.rate_group_id'))
    family_code = db.Column(db.String(3), nullable=False)
    smoker_status = db.Column(db.String(1), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    benefit_rate_premium = db.Column(db.Numeric(12, 5), nullable=False)

    benefit = db.relationship(
        "Model_SelectionBenefit", back_populates="benefit_rates")

    @classmethod
    def find_by_plan(cls, plan_id):
        return cls.query.filter(cls.selection_plan_id == plan_id).all()

    @classmethod
    def find_by_benefit(cls, benefit_id):
        return cls.query.filter(cls.selection_benefit_id == benefit_id).all()

    @classmethod
    def delete_by_benefit_id(cls, benefit_id, commit=False):
        try:
            cls.query.filter(
                cls.selection_benefit_id == benefit_id).delete()
        except:
            db.session.rollback()
            raise
        else:
            if commit:
                db.session.commit()

    @classmethod
    def delete_by_plan(cls, plan_id):
        try: 
            cls.query.filter(cls.selection_plan_id == plan_id).delete()
            db.session.commit()
        except Exception as e: 
            db.session.rollback()
            raise e
