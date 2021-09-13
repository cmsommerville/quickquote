from app.extensions import db
import datetime

from .BenefitModel import BenefitModel


class CoverageModel(db.Model):
    __tablename__ = "coverages"

    coverage_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    coverage_code = db.Column(db.String(20), nullable=False)

    created_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_dts = db.Column(db.DateTime, default=db.func.current_timestamp())

    plan = db.relationship("PlanModel", back_populates="coverages")
    benefits = db.relationship("BenefitModel", back_populates="coverage")

    def __repr__(self):
        return f"<Coverage Id: {self.coverage_id} -- Coverage Code: `{self.coverage_code}`>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.coverage_id == id).first()

    @classmethod
    def find_coverages(cls, plan_id):
        return cls.query.filter(cls.plan_id == plan_id).all()

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
            for coverage in coverages:
                db.session.add(coverage)

        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()
