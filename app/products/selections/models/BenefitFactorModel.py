from app.extensions import db
from app.shared import BaseModel
import datetime

from .BenefitAgeRateModel import BenefitAgeRateModel


class BenefitFactorModel(BaseModel):
    __tablename__ = "selections_benefit_factors"

    benefit_factor_id = db.Column(db.Integer, primary_key=True)
    benefit_age_rate_id = db.Column(db.Integer, db.ForeignKey(
        "selections_benefit_age_rates.benefit_age_rate_id"))
    plan_id = db.Column(db.Integer, db.ForeignKey('selections_plans.plan_id'))
    provision_id = db.Column(
        db.Integer, db.ForeignKey('selections_provisions.provision_id'))
    factor_type = db.Column(db.String(10), nullable=False)
    factor_name = db.Column(db.String(50), nullable=False)
    factor_selection = db.Column(db.String(36), nullable=False)
    factor_selection_type = db.Column(db.String(10), nullable=False)
    factor_value = db.Column(db.Float, nullable=False)

    benefit_age_rate = db.relationship(
        "BenefitAgeRateModel", back_populates="benefit_factors")

    def __repr__(self):
        return f"<Benefit Factor Id: {self.factor_id} -- Factor Name: `{self.factor_name}`>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.factor_id == id).first()

    @classmethod
    def find_plan_factors(cls, plan_id):
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
