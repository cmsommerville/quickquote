from app.models import db
import datetime

from app.models.ProvisionModel import ProvisionModel
from app.models.FactorModel import FactorModel
from app.models.CoverageModel import CoverageModel
from app.models.BenefitModel import BenefitModel


class PlanRateModel(db.Model):
    __tablename__ = "plan_rates"

    plan_rate_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    uuid = db.Column(db.String(36))
    family_code = db.Column(db.String(3), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    smoker_status = db.Column(db.String(1), nullable=False)

    row_eff_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    row_exp_dts = db.Column(
        db.DateTime, default=datetime.datetime(9999, 12, 31, 0, 0, 0))
    active_record_indicator = db.Column(db.String(1), default='Y')

    plan = db.relationship("PlanModel", back_populates="plan_rates")
    factors = db.relationship("FactorModel", back_populates="plan_rate")
    coverages = db.relationship("CoverageModel", back_populates="plan_rate")
    benefits = db.relationship("BenefitModel", back_populates="plan_rate")
    # provisions = db.relationship("ProvisionModel", back_populates="plan")

    def __repr__(self):
        return f"<Plan Rate Id: {self.plan_rate_id}>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.plan_rate_id == id).first()

    @classmethod
    def find_by_plan_id(cls, id):
        return cls.query.filter(cls.plan_id == id, cls.active_record_indicator == 'Y').all()

    @classmethod
    def expire_plan_rates(cls, plan_id):
        plan_rates = cls.find_by_plan_id(plan_id)
        if plan_rates:
            for plan_rate in plan_rates:
                plan_rate.row_exp_dts = db.func.current_timestamp()
                plan_rate.active_record_indicator = 'N'
                db.session.add(plan_rate)

    @classmethod
    def save_all_to_db(cls, plan_rates,  plan_id):
        try:
            cls.expire_plan_rates(plan_id)
            for plan_rate in plan_rates:
                db.session.add(plan_rate)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()
