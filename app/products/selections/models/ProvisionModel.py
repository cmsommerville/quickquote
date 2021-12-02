from app.extensions import db
from app.shared import BaseModel
import datetime


class ProvisionModel(BaseModel):
    __tablename__ = "selections_provisions"

    provision_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('selections_plans.plan_id'))
    provision_code = db.Column(db.String(20), nullable=False)
    provision_value = db.Column(db.String(255), nullable=False)
    provision_data_type = db.Column(db.String(20), nullable=False)

    plan = db.relationship("PlanModel", back_populates="provisions")

    def __repr__(self):
        return f"<Provision Id: {self.provision_id} -- Provision Code: `{self.provision_code}`>"

    def getValue(self):
        if self.provision_data_type == 'number':
            if '.' in self.provision_value:
                return float(self.provision_value)
            return int(self.provision_value)
        if self.provision_data_type == 'boolean':
            return self.provision_value.lower() == 'true'
        return self.provision_value

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.provision_id == id).first()

    @classmethod
    def find_plan_provisions(cls, plan_id):
        return cls.query.filter(cls.plan_id == plan_id).all()
