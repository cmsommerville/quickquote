from app.extensions import db
from app.shared import BaseModel
import datetime

from ...__constants__ import TBL_NAMES

CONFIG_FACTOR = TBL_NAMES['CONFIG_FACTOR']
SELECTION_BENEFIT_AGE_RATE = TBL_NAMES['SELECTION_BENEFIT_AGE_RATE']
SELECTION_BENEFIT_FACTOR = TBL_NAMES['SELECTION_BENEFIT_FACTOR']
SELECTION_PROVISION = TBL_NAMES['SELECTION_PROVISION']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']

class Model_SelectionBenefitFactor(BaseModel):
    __tablename__ = SELECTION_BENEFIT_FACTOR

    selection_benefit_factor_id = db.Column(db.Integer, primary_key=True)
    selection_benefit_age_rate_id = db.Column(db.ForeignKey(
        f"{SELECTION_BENEFIT_AGE_RATE}.selection_benefit_age_rate_id"))
    selection_plan_id = db.Column(db.ForeignKey(F'{SELECTION_PLAN}.selection_plan_id'))
    selection_provision_id = db.Column(db.ForeignKey(F'{SELECTION_PROVISION}.selection_provision_id'))
    config_factor_id = db.Column(db.ForeignKey(F'{CONFIG_FACTOR}.factor_id'))
    factor_value = db.Column(db.Float, nullable=False)

    benefit_age_rate = db.relationship(
        "Model_SelectionBenefitAgeRate", back_populates="benefit_factors")

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