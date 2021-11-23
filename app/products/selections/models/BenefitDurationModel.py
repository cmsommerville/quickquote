from app.extensions import db
from app.shared import VersionedTable
import datetime


class BenefitDurationModel(db.Model, VersionedTable):
    __tablename__ = "benefit_durations"

    benefit_duration_id = db.Column(db.Integer, primary_key=True)
    benefit_id = db.Column(db.Integer, db.ForeignKey('benefits.benefit_id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    duration_code = db.Column(db.String(50), nullable=False)
    duration_data_type = db.Column(db.String(20), nullable=False)
    duration_value = db.Column(db.String(100), nullable=False)
    duration_factor = db.Column(db.Numeric(12, 7), nullable=False)

    row_eff_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    row_exp_dts = db.Column(db.DateTime, default='9999-12-31 00:00:00.000')
    active_record_indicator = db.Column(db.String(1), default='Y')

    created_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_dts = db.Column(db.DateTime, default=db.func.current_timestamp())

    plan = db.relationship("PlanModel")
    benefit = db.relationship("BenefitModel", back_populates="durations")

    def __repr__(self):
        return f"<Benefit Duration Id: {self.benefit_duration_id} -- `{self.duration_code}`: {self.duration_value}>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.benefit_id == id).first()

    @classmethod
    def find_benefits(cls, plan_id):
        return cls.query.filter(cls.plan_id == plan_id).all()

    def validate(self) -> bool:
        """
        Validate the plan
        """
        return True

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
