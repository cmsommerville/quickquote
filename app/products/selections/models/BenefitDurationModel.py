from app.extensions import db
from app.shared import BaseModel
import datetime


class BenefitDurationModel(BaseModel):
    __tablename__ = "selections_benefit_durations"

    benefit_duration_id = db.Column(db.Integer, primary_key=True)
    benefit_id = db.Column(db.Integer, db.ForeignKey('selections_benefits.benefit_id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('selections_plans.plan_id'))
    duration_code = db.Column(db.String(50), nullable=False)
    duration_data_type = db.Column(db.String(20), nullable=False)
    duration_value = db.Column(db.String(100), nullable=False)
    duration_factor = db.Column(db.Numeric(12, 7), nullable=False)

    plan = db.relationship("PlanModel")
    benefit = db.relationship("BenefitModel", back_populates="durations")

    def __repr__(self):
        return f"<Benefit Duration Id: {self.benefit_duration_id} -- `{self.duration_code}`: {self.duration_value}>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.benefit_id == id).first()

    @classmethod
    def find_benefits(cls, plan_id):
        return cls.query.filter(cls.plan_id == plan_id).all()

    def validate(self) -> bool:
        """
        Validate the plan
        """
        return True
