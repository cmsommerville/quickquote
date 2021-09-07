from app.models import db
import datetime

from app.models.BenefitModel import BenefitModel


class CoverageModel(db.Model):
    __tablename__ = "coverages"

    coverage_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    coverage_code = db.Column(db.String(20), nullable=False)

    row_eff_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    row_exp_dts = db.Column(
        db.DateTime, default=datetime.datetime(9999, 12, 31, 0, 0, 0))
    active_record_indicator = db.Column(db.String(1), default='Y')

    plan = db.relationship("PlanModel", back_populates="coverages")
    benefits = db.relationship("BenefitModel", back_populates="coverage")

    def __repr__(self):
        return f"<Coverage Id: {self.coverage_id} -- Coverage Code: `{self.coverage_code}`>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.coverage_id == id).first()

    @classmethod
    def find_coverages(cls, plan_id):
        return cls.query.filter(cls.plan_id == plan_id, cls.active_record_indicator == 'Y').all()

    @classmethod
    def expire_coverages(cls, plan_id):
        coverages = cls.find_coverages(plan_id)
        if coverages:
            for coverage in coverages:
                coverage.row_exp_dts = db.func.current_timestamp()
                coverage.active_record_indicator = 'N'
                db.session.add(coverage)

    def save_to_db(self):
        try:
            db.session.add(self)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()

    @classmethod
    def save_all_to_db(cls, coverages, plan_id):
        try:
            cls.expire_coverages(plan_id)
            BenefitModel.expire_benefits(plan_id)
            for coverage in coverages:
                db.session.add(coverage)

        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()
