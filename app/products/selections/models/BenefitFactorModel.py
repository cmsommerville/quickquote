from app.extensions import db
from app.shared import VersionedTable
import datetime

from .BenefitAgeRateModel import BenefitAgeRateModel


class BenefitFactorModel(db.Model):
    __tablename__ = "benefit_factors"

    benefit_factor_id = db.Column(db.Integer, primary_key=True)
    benefit_age_rate_id = db.Column(db.Integer, db.ForeignKey(
        "benefit_age_rates.benefit_age_rate_id"))
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    provision_id = db.Column(
        db.Integer, db.ForeignKey('provisions.provision_id'))
    factor_type = db.Column(db.String(10), nullable=False)
    factor_name = db.Column(db.String(50), nullable=False)
    factor_selection = db.Column(db.String(36), nullable=False)
    factor_selection_type = db.Column(db.String(10), nullable=False)
    factor_value = db.Column(db.Float, nullable=False)

    row_eff_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    row_exp_dts = db.Column(db.DateTime, default='9999-12-31 00:00:00.000')
    active_record_indicator = db.Column(db.String(1), default='Y')

    created_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_dts = db.Column(db.DateTime, default=db.func.current_timestamp())

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

    def save_to_db(self):
        try:
            db.session.add(self)
        except:
            db.session.rollback()
        else:
            db.session.commit()

    @classmethod
    def save_all_to_db(cls, factors):
        try:
            # for factor in factors:
            #     db.session.add(factor)
            db.session.bulk_save_objects(factors)
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
