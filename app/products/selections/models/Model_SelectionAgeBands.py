from app.extensions import db
from app.shared import BaseModel
import datetime

from ...__constants__ import TBL_NAMES

SELECTION_AGE_BANDS = TBL_NAMES['SELECTION_AGE_BANDS']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']

class Model_SelectionAgeBands(BaseModel):
    __tablename__ = SELECTION_AGE_BANDS

    selection_age_band_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(db.Integer, db.ForeignKey(F'{SELECTION_PLAN}.selection_plan_id'))
    lower_age = db.Column(db.Integer, nullable=False)
    upper_age = db.Column(db.Integer, nullable=False)

    plan = db.relationship("Model_SelectionPlan", back_populates="age_bands")

    @classmethod
    def find_by_plan(cls, plan_id):
        return cls.query.filter(cls.selection_plan_id == plan_id).all()