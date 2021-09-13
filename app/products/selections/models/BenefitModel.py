from app.extensions import db
import datetime


class BenefitModel(db.Model):
    __tablename__ = "benefits"

    benefit_id = db.Column(db.Integer, primary_key=True)
    coverage_id = db.Column(db.Integer, db.ForeignKey('coverages.coverage_id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    benefit_code = db.Column(db.String(20), nullable=False)
    benefit_uuid = db.Column(db.String(36))
    benefit_value = db.Column(db.Numeric(12, 4), nullable=False)

    created_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_dts = db.Column(db.DateTime, default=db.func.current_timestamp())

    plan = db.relationship("PlanModel", back_populates="benefits")
    coverage = db.relationship("CoverageModel", back_populates="benefits")
    benefit_rates = db.relationship(
        "BenefitRateModel", back_populates="benefit")

    def __repr__(self):
        return f"<Benefit Id: {self.benefit_id} -- Benefit Code: `{self.benefit_code}` -- Benefit Rates: {len(self.benefit_rates)}>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.benefit_id == id).first()

    @classmethod
    def find_benefits(cls, plan_id):
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
    def save_all_to_db(cls, benefits, plan_id):
        try:
            for benefit in benefits:
                db.session.add(benefit)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()
