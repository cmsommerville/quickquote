from app.extensions import db
import datetime
from sqlalchemy import func

from .RateTableModel import RateTableModel
from .AgeBandsModel import AgeBandsModel


class BenefitRateModel(db.Model):
    __tablename__ = "benefit_rates"

    benefit_rate_id = db.Column(db.Integer, primary_key=True)
    benefit_id = db.Column(db.Integer, db.ForeignKey('benefits.benefit_id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    age_band_id = db.Column(db.Integer, db.ForeignKey('age_bands.age_band_id'))
    family_code = db.Column(db.String(3), nullable=False)
    smoker_status = db.Column(db.String(1), nullable=False)
    benefit_rate_premium = db.Column(db.Numeric(12, 5))

    created_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_dts = db.Column(db.DateTime, default=db.func.current_timestamp())

    plan = db.relationship("PlanModel")
    benefit = db.relationship("BenefitModel", back_populates="benefit_rates")
    age_band = db.relationship("AgeBandsModel")

    def __repr__(self):
        return f"<Benefit Rate Id: {self.benefit_rate_id}>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.benefit_rate_id == id).first()

    @classmethod
    def find_benefit_rates_by_plan(cls, plan_id):
        return cls.query.filter(cls.plan_id == plan_id).options(db.joinedload(cls.benefit)).all()

    @classmethod
    def find_benefit_rates_by_benefit(cls, benefit_id):
        return cls.query.filter(cls.benefit_id == benefit_id).options(db.joinedload(cls.benefit)).all()

    @classmethod
    def agg_benefit_rates_by_age_band(cls, plan_id):
        qry = db.session.query(
            cls.plan_id, cls.benefit_id, cls.age_band_id,
            cls.smoker_status, cls.family_code,
            func.sum(cls.benefit_rate_final_premium).label("benefit_rate_final_premium")) \
            .filter(cls.plan_id == plan_id, cls.age_band_id != None)\
            .group_by(
                cls.plan_id, cls.benefit_id, cls.age_band_id,
                cls.smoker_status, cls.family_code)
        return qry.all()

    def save_to_db(self):
        try:
            db.session.add(self)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()

    @classmethod
    def save_all_to_db(cls, benefit_rates):
        try:
            # for benefit_rate in benefit_rates:
            #     db.session.add(benefit_rate)
            db.session.bulk_save_objects(benefit_rates)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()

    @classmethod
    def delete_by_benefit_id(cls, benefit_id, commit=False):
        try:
            # benefits_for_delete = cls.query.filter(
            #     cls.benefit_id == benefit_id).all()
            # for bnft in benefits_for_delete:
            #     db.session.delete(bnft)
            cls.query.filter(
                cls.benefit_id == benefit_id).delete()
        except:
            db.session.rollback()
            raise
        else:
            if commit:
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
