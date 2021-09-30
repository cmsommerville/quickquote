from app.extensions import db
import datetime
from sqlalchemy import func

from .RateTableModel import RateTableModel
from .AgeBandsModel import AgeBandsModel


class BenefitAgeRateModel(db.Model):
    __tablename__ = "benefit_age_rates"

    benefit_age_rate_id = db.Column(db.Integer, primary_key=True)
    benefit_rate_id = db.Column(
        db.Integer, db.ForeignKey('benefit_rates.benefit_rate_id'))
    benefit_id = db.Column(db.Integer, db.ForeignKey('benefits.benefit_id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    family_code = db.Column(db.String(3), nullable=False)
    smoker_status = db.Column(db.String(1), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    age_weight = db.Column(db.Numeric(12, 5))
    benefit_age_rate_base_premium = db.Column(db.Numeric(12, 5))
    benefit_age_rate_product_factor = db.Column(db.Numeric(12, 5))
    benefit_age_rate_benefit_factor = db.Column(db.Numeric(12, 5))
    benefit_age_rate_final_premium = db.Column(db.Numeric(12, 5))

    created_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_dts = db.Column(db.DateTime, default=db.func.current_timestamp())

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
    def save_all_to_db(cls, benefit_age_rates):
        try:
            for benefit_age_rate in benefit_age_rates:
                db.session.add(benefit_age_rate)
            # db.session.bulk_save_objects(benefit_rates)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()

    @classmethod
    def delete_by_plan_id(cls, plan_id):
        try:
            cls.query.filter(
                cls.plan_id == plan_id).delete()
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()
