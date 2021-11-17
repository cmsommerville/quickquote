from app.extensions import db
from app.shared import VersionedTable
import datetime

from ..utils.helpers import stateValidator


class BenefitModel(db.Model, VersionedTable):
    __tablename__ = "benefits"

    benefit_id = db.Column(db.Integer, primary_key=True)
    coverage_id = db.Column(db.Integer, db.ForeignKey('coverages.coverage_id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    benefit_code = db.Column(db.String(20), nullable=False)
    plan_rate_code = db.Column(db.String(20), nullable=False)
    benefit_uuid = db.Column(db.String(36))
    benefit_value = db.Column(db.Numeric(12, 4), nullable=False)

    row_eff_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    row_exp_dts = db.Column(db.DateTime, default='9999-12-31 00:00:00.000')
    active_record_indicator = db.Column(db.String(1), default='Y')

    created_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_dts = db.Column(db.DateTime, default=db.func.current_timestamp())

    plan = db.relationship("PlanModel", back_populates="benefits")
    coverage = db.relationship("CoverageModel", back_populates="benefits")
    benefit_rates = db.relationship(
        "BenefitRateModel", back_populates="benefit",
        primaryjoin="and_(BenefitModel.benefit_id == BenefitRateModel.benefit_id, BenefitRateModel.active_record_indicator == 'Y')")

    def __repr__(self):
        return f"<Benefit Id: {self.benefit_id} -- Benefit Code: `{self.benefit_code}` -- Benefit Rates: {len(self.benefit_rates)}>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.benefit_id == id).first()

    @classmethod
    def find_benefits(cls, plan_id):
        return cls.query.filter(cls.plan_id == plan_id).all()

    def validate(self, policy: dict, config: dict) -> bool:
        """
        Validate the plan
        """
        configIsValid = stateValidator(self.plan.rating_state,
                                       self.plan.plan_effective_date,
                                       config['states'])

        policyIsValid = stateValidator(self.rating_state,
                                       self.plan_effective_date,
                                       policy['states'])

        return configIsValid and policyIsValid

    def save_to_db(self):
        try:
            db.session.add(self)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()

    @classmethod
    def save_all_to_db(cls, benefits, plan_id):
        try:
            for benefit in benefits:
                db.session.add(benefit)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()
