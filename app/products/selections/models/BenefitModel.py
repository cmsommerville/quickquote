from app.extensions import db
from app.shared import BaseModel
import datetime

from ..utils.helpers import stateValidator


class BenefitModel(BaseModel):
    __tablename__ = "selections_benefits"

    benefit_id = db.Column(db.Integer, primary_key=True)
    coverage_id = db.Column(db.Integer, db.ForeignKey('selections_coverages.coverage_id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('selections_plans.plan_id'))
    benefit_code = db.Column(db.String(20), nullable=False)
    plan_rate_code = db.Column(db.String(20), nullable=False)
    benefit_uuid = db.Column(db.String(36))
    benefit_value = db.Column(db.Numeric(12, 4), nullable=False)

    plan = db.relationship("PlanModel", back_populates="benefits")
    coverage = db.relationship("CoverageModel", back_populates="benefits")
    durations = db.relationship("BenefitDurationModel", back_populates="benefit")
    benefit_rates = db.relationship(
        "BenefitRateModel", back_populates="benefit")

    def __repr__(self):
        return f"<Benefit Id: {self.benefit_id} -- Benefit Code: `{self.benefit_code}` -- Benefit Rates: {len(self.benefit_rates)}>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.benefit_id == id).first()

    @classmethod
    def find_benefits(cls, plan_id):
        return cls.query.filter(cls.plan_id == plan_id).all()
