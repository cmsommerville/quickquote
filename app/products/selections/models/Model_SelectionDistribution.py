from app.extensions import db
from app.shared import BaseModel
import datetime

from ...__constants__ import TBL_NAMES

SELECTION_DISTRIBUTION = TBL_NAMES['SELECTION_DISTRIBUTION']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']

class Model_SelectionDistribution(BaseModel):
    __tablename__ = SELECTION_DISTRIBUTION

    selection_distribution_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(db.Integer, db.ForeignKey(F'{SELECTION_PLAN}.selection_plan_id'))
    attr_type_code = db.Column(db.String(30))
    attr_value = db.Column(db.String(30))
    weight = db.Column(db.Numeric(12,5))

    @classmethod
    def find_by_plan(cls, plan_id):
        return cls.query.filter(cls.selection_plan_id == plan_id).all()

    @classmethod
    def delete_by_plan(cls, plan_id: int, attr_type_code: str = None):
        try: 
            qry = cls.query.filter(cls.selection_plan_id == plan_id)
            if attr_type_code: 
                qry = qry.filter(cls.attr_type_code == attr_type_code)

            qry.delete()
            db.session.commit()
        except: 
            db.session.rollback()