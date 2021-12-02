from sqlalchemy import event
from app.extensions import db
from app.shared import BaseModel
import datetime

from .BenefitModel import BenefitModel


class CoverageModel(BaseModel):
    __tablename__ = "selections_coverages"

    coverage_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('selections_plans.plan_id'))
    coverage_code = db.Column(db.String(20), nullable=False)

    plan = db.relationship("PlanModel", back_populates="coverages")
    benefits = db.relationship("BenefitModel", back_populates="coverage")

    def __repr__(self):
        return f"<Coverage Id: {self.coverage_id} -- Coverage Code: `{self.coverage_code}`>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.coverage_id == id).first()

    @classmethod
    def find_coverages(cls, plan_id):
        return cls.query.filter(cls.plan_id == plan_id).all()
