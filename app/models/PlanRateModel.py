from app.models import db
import datetime

from app.models.ProvisionModel import ProvisionModel
from app.models.FactorModel import FactorModel


class PlanRateModel(db.Model):
    __tablename__ = "plan_rates"

    plan_rate_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    family_code = db.Column(db.String(3), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    smoker_status = db.Column(db.String(1), nullable=False)

    row_add_dts = db.Column(db.DateTime, default=db.func.current_timestamp())

    plan = db.relationship("PlanModel", back_populates="plan_rates")
    factors = db.relationship("FactorModel", back_populates="plan_rate")
    # coverages = db.relationship("CoverageModel", back_populates="plan")
    # benefits = db.relationship("BenefitModel", back_populates="plan")
    # provisions = db.relationship("ProvisionModel", back_populates="plan")

    def __repr__(self):
        return f"<Plan Rate Id: {self.plan_rate_id}>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.plan_rate_id == id).first()

    @classmethod
    def find_by_plan_id(cls, id):
        return cls.query.filter(cls.plan_id == id).all()

    @classmethod
    def save_all_to_db(cls, plan_rates):
        try:
            for plan_rate in plan_rates:
                db.session.add(plan_rate)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()
