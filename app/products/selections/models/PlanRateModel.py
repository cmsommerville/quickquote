from app.extensions import db
from app.shared import VersionedTable
import datetime
from sqlalchemy import func

from .AgeBandsModel import AgeBandsModel


class PlanRateModel(db.Model):
    __tablename__ = "plan_rates"

    plan_rate_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    age_band_id = db.Column(db.Integer, db.ForeignKey('age_bands.age_band_id'))
    plan_rate_code = db.Column(db.String(10), nullable=False)
    family_code = db.Column(db.String(3), nullable=False)
    smoker_status = db.Column(db.String(1), nullable=False)
    plan_rate_premium = db.Column(db.Numeric(12, 5))

    row_eff_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    row_exp_dts = db.Column(db.DateTime, default='9999-12-31 00:00:00.000')
    active_record_indicator = db.Column(db.String(1), default='Y')

    created_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_dts = db.Column(db.DateTime, default=db.func.current_timestamp())

    plan = db.relationship("PlanModel")
    age_band = db.relationship("AgeBandsModel")
    benefit_rates = db.relationship(
        "BenefitRateModel", back_populates="plan_rate",
        primaryjoin="and_(PlanRateModel.plan_rate_id == BenefitRateModel.plan_rate_id, BenefitRateModel.active_record_indicator == 'Y')")

    def __repr__(self):
        return f"<Plan Rate ID: {self.plan_rate_id}>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.plan_rate_id == id).first()

    @classmethod
    def find_by_plan(cls, plan_id):
        return cls.query.filter(cls.plan_id == plan_id).all()

    @classmethod
    def save_all_to_db(cls, plan_rates):
        try:
            for plan_rate in plan_rates:
                db.session.add(plan_rate)
            # db.session.bulk_save_objects(benefit_rates)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()

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
