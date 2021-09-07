from app.models import db
import datetime


class BenefitModel(db.Model):
    __tablename__ = "benefits"

    benefit_id = db.Column(db.Integer, primary_key=True)
    coverage_id = db.Column(db.Integer, db.ForeignKey('coverages.coverage_id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    benefit_code = db.Column(db.String(20), nullable=False)
    benefit_uuid = db.Column(db.String(36))
    benefit_value = db.Column(db.Numeric(12, 4), nullable=False)
    row_eff_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    row_exp_dts = db.Column(
        db.DateTime, default=datetime.datetime(9999, 12, 31, 0, 0, 0))
    active_record_indicator = db.Column(db.String(1), default='Y')

    plan = db.relationship("PlanModel", back_populates="benefits")
    coverage = db.relationship("CoverageModel", back_populates="benefits")

    def __repr__(self):
        return f"<Benefit Id: {self.benefit_id} -- Benefit Code: `{self.benefit_code}`>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.benefit_id == id).first()

    @classmethod
    def find_benefits(cls, plan_id):
        return cls.query.filter(cls.plan_id == plan_id, cls.active_record_indicator == 'Y').all()

    @classmethod
    def expire_benefits(cls, plan_id):
        benefits = cls.find_benefits(plan_id)
        if benefits:
            for benefit in benefits:
                benefit.row_exp_dts = db.func.current_timestamp()
                benefit.active_record_indicator = 'N'
                db.session.add(benefit)

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
            cls.expire_benefits(plan_id)
            for benefit in benefits:
                db.session.add(benefit)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()
