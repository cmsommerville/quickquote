from app.extensions import db
from app.shared import BaseModel
import datetime

from ...__constants__ import TBL_NAMES

CONFIG_PROVISION = TBL_NAMES['CONFIG_PROVISION']
SELECTION_PROVISION = TBL_NAMES['SELECTION_PROVISION']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']

class Model_SelectionProvision(BaseModel):
    __tablename__ = SELECTION_PROVISION

    selection_provision_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(db.ForeignKey(f'{SELECTION_PLAN}.selection_plan_id'))
    config_provision_id = db.Column(db.ForeignKey(f'{CONFIG_PROVISION}.provision_id'), nullable=False)
    provision_value = db.Column(db.String(255), nullable=False)
    provision_data_type = db.Column(db.String(20), nullable=False)

    plan = db.relationship("Model_SelectionPlan", back_populates="provisions")

    def getValue(self):
        if self.provision_data_type == 'number':
            if '.' in self.provision_value:
                return float(self.provision_value)
            return int(self.provision_value)
        if self.provision_data_type == 'boolean':
            return self.provision_value.lower() == 'true'
        return self.provision_value

    @classmethod
    def find_by_plan(cls, plan_id: int):
        return cls.query.filter(cls.selection_plan_id == plan_id).all()
