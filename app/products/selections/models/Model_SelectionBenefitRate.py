from app.extensions import db
from app.shared import BaseModel
from sqlalchemy import func

from ...__constants__ import TBL_NAMES

SELECTION_AGE_BANDS = TBL_NAMES['SELECTION_AGE_BANDS']
SELECTION_BENEFIT = TBL_NAMES['SELECTION_BENEFIT']
SELECTION_BENEFIT_RATE = TBL_NAMES['SELECTION_BENEFIT_RATE']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']
SELECTION_RATE_GROUP_SUMMARY = TBL_NAMES['SELECTION_RATE_GROUP_SUMMARY']


class Model_SelectionBenefitRate(BaseModel):
    __tablename__ = SELECTION_BENEFIT_RATE

    selection_benefit_rate_id = db.Column(db.Integer, primary_key=True)
    selection_benefit_id = db.Column(db.ForeignKey(f'{SELECTION_BENEFIT}.selection_benefit_id'))
    selection_plan_id = db.Column(db.ForeignKey(f'{SELECTION_PLAN}.selection_plan_id'))
    selection_rate_group_summary_id = db.Column(
        db.ForeignKey(f'{SELECTION_RATE_GROUP_SUMMARY}.selection_rate_group_summary_id'))
    selection_age_band_id = db.Column(db.ForeignKey(f'{SELECTION_AGE_BANDS}.selection_age_band_id'))
    family_code = db.Column(db.String(3), nullable=False)
    smoker_status = db.Column(db.String(1), nullable=False)
    benefit_rate_premium = db.Column(db.Numeric(12, 5))

    plan = db.relationship("Model_SelectionPlan")
    benefit = db.relationship("Model_SelectionBenefit", back_populates="benefit_rates")
    age_band = db.relationship("Model_SelectionAgeBands")
    rate_group_summary = db.relationship(
        "Model_SelectionRateGroupSummary", back_populates="benefit_rates")
    benefit_age_rates = db.relationship(
        "Model_SelectionBenefitAgeRate", back_populates="benefit_rate")

    @classmethod
    def find_by_plan(cls, plan_id):
        return cls.query.filter(cls.selection_plan_id == plan_id).all()

    @classmethod
    def find_by_benefit(cls, benefit_id):
        return cls.query.filter(cls.selection_benefit_id == benefit_id).all()

    @classmethod
    def agg_benefit_rates_by_age_band(cls, plan_id):
        qry = db.session.query(
            cls.selection_plan_id, cls.selection_benefit_id, cls.selection_age_band_id,
            cls.smoker_status, cls.family_code,
            func.sum(cls.benefit_rate_final_premium).label("benefit_rate_final_premium")) \
            .filter(cls.selection_plan_id == plan_id, cls.selection_age_band_id != None)\
            .group_by(
                cls.selection_plan_id, cls.selection_benefit_id, cls.selection_age_band_id,
                cls.smoker_status, cls.family_code)
        return qry.all()

    @classmethod
    def delete_by_benefit_id(cls, benefit_id, commit=False):
        try:
            cls.query.filter(
                cls.selection_benefit_id == benefit_id).delete()
        except:
            db.session.rollback()
            raise
        else:
            if commit:
                db.session.commit()

    # @classmethod
    # def delete_by_plan_id(cls, plan_id):
    #     try:
    #         cls.query.filter(cls.selection_plan_id == plan_id).update({
    #             cls.row_exp_dts: db.func.current_timestamp(),
    #             cls.active_record_indicator: "N"
    #         })
    #     except:
    #         db.session.rollback()
    #         raise
    #     else:
    #         db.session.commit()
