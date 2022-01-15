from app.extensions import db
from app.products.selections.models.Model_SelectionProvision import CONFIG_PROVISION
from app.shared import BaseModel
import datetime

from ...__constants__ import TBL_NAMES

CONFIG_BENEFIT = TBL_NAMES['CONFIG_BENEFIT']
CONFIG_FACTOR = TBL_NAMES['CONFIG_FACTOR']
CONFIG_PROVISION = TBL_NAMES['CONFIG_PROVISION']
CONFIG_RATE_TABLE = TBL_NAMES['CONFIG_RATE_TABLE']
SELECTION_BENEFIT_FACTOR = TBL_NAMES['SELECTION_BENEFIT_FACTOR']
SELECTION_PROVISION = TBL_NAMES['SELECTION_PROVISION']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']

class Model_SelectionBenefitFactor(BaseModel):
    __tablename__ = SELECTION_BENEFIT_FACTOR
    __table_args__ = (
        db.UniqueConstraint('config_rate_table_id', 'config_provision_id'), 
    )

    selection_benefit_factor_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(db.ForeignKey(F'{SELECTION_PLAN}.selection_plan_id'))
    selection_provision_id = db.Column(db.ForeignKey(F'{SELECTION_PROVISION}.selection_provision_id'))
    config_rate_table_id = db.Column(db.ForeignKey(F'{CONFIG_RATE_TABLE}.rate_table_id'))
    config_benefit_id = db.Column(db.ForeignKey(F'{CONFIG_BENEFIT}.benefit_id'))
    config_provision_id = db.Column(db.ForeignKey(F'{CONFIG_PROVISION}.provision_id'))
    config_factor_id = db.Column(db.ForeignKey(F'{CONFIG_FACTOR}.factor_id'))
    factor_value = db.Column(db.Float, nullable=False)

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