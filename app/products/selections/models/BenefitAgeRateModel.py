from app.extensions import db
from app.shared import BaseModel
import datetime
from sqlalchemy import func

from .RateTableModel import RateTableModel
from .AgeBandsModel import AgeBandsModel


class BenefitAgeRateModel(BaseModel):
    __tablename__ = "selections_benefit_age_rates"

    benefit_age_rate_id = db.Column(db.Integer, primary_key=True)
    benefit_rate_id = db.Column(
        db.Integer, db.ForeignKey('selections_benefit_rates.benefit_rate_id'))
    benefit_id = db.Column(db.Integer, db.ForeignKey('selections_benefits.benefit_id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('selections_plans.plan_id'))
    family_code = db.Column(db.String(3), nullable=False)
    smoker_status = db.Column(db.String(1), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    age_weight = db.Column(db.Numeric(12, 5))
    benefit_age_rate_base_premium = db.Column(db.Numeric(12, 5))
    benefit_age_rate_product_factor = db.Column(db.Numeric(12, 5))
    benefit_age_rate_benefit_factor = db.Column(db.Numeric(12, 5))
    benefit_age_rate_final_premium = db.Column(db.Numeric(12, 5))

    plan = db.relationship("PlanModel")
    benefit = db.relationship("BenefitModel")
    benefit_rate = db.relationship(
        "BenefitRateModel", back_populates="benefit_age_rates")
    benefit_factors = db.relationship(
        "BenefitFactorModel", back_populates="benefit_age_rate")

    def __repr__(self):
        return f"<Benefit Age Rate Id: {self.benefit_rate_id}>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.benefit_rate_id == id).first()

    @classmethod
    def find_benefit_age_rates_by_plan(cls, plan_id):
        return cls.query.filter(cls.plan_id == plan_id).all()

    @classmethod
    def delete_by_plan_id(cls, plan_id):
        try:
            cls.query.filter(cls.plan_id == plan_id).update({
                cls.row_exp_dts: db.func.current_timestamp(),
                cls.active_record_indicator: "N"
            })
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()
