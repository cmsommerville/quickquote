from app.extensions import db
from app.shared import BaseModel
import datetime
from sqlalchemy import func

from .AgeBandsModel import AgeBandsModel


class PlanRateModel(BaseModel):
    __tablename__ = "selections_plan_rates"

    plan_rate_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('selections_plans.plan_id'))
    age_band_id = db.Column(db.Integer, db.ForeignKey('selections_age_bands.age_band_id'))
    plan_rate_code = db.Column(db.String(10), nullable=False)
    family_code = db.Column(db.String(3), nullable=False)
    smoker_status = db.Column(db.String(1), nullable=False)
    plan_rate_premium = db.Column(db.Numeric(12, 5))

    plan = db.relationship("PlanModel")
    age_band = db.relationship("AgeBandsModel")
    benefit_rates = db.relationship(
        "BenefitRateModel", back_populates="plan_rate")

    def __repr__(self):
        return f"<Plan Rate ID: {self.plan_rate_id}>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.plan_rate_id == id).first()

    @classmethod
    def find_by_plan(cls, plan_id):
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
