from app.models import db
import datetime


class CoverageModel(db.Model):
    __tablename__ = "coverages"

    coverage_id = db.Column(db.Integer, primary_key=True)
    plan_rate_id = db.Column(
        db.Integer, db.ForeignKey('plan_rates.plan_rate_id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    coverage_code = db.Column(db.String(20), nullable=False)
    coverage_value = db.Column(db.String(255), nullable=False)
    coverage_data_type = db.Column(db.String(20), nullable=False)
    is_coverage_rated = db.Column(db.String(1), default="N")
    coverage_base_rate_uuid = db.Column(db.String(36))
    coverage_annual_base_rate_per_unit = db.Column(db.Numeric(12, 5))
    coverage_annual_base_rate_unit_value = db.Column(db.Numeric(12, 2))
    coverage_annual_rate = db.Column(db.Numeric(12, 5))
    row_eff_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    row_exp_dts = db.Column(
        db.DateTime, default=datetime.datetime(9999, 12, 31, 0, 0, 0))
    active_record_indicator = db.Column(db.String(1), default='Y')

    plan = db.relationship("PlanModel", back_populates="coverages")
    plan_rate = db.relationship("PlanRateModel", back_populates="coverages")
    benefits = db.relationship("BenefitModel", back_populates="coverage")

    def __repr__(self):
        return f"<Coverage Id: {self.coverage_id} -- Coverage Code: `{self.coverage_code}`>"

    def getValue(self):
        if self.coverage_data_type == 'number':
            if '.' in self.coverage_value:
                return float(self.coverage_value)
            return int(self.coverage_value)
        if self.coverage_data_type == 'boolean':
            return self.coverage_value.lower() == 'true'
        return self.coverage_value

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
            for coverage in coverages:
                db.session.add(coverage)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()
