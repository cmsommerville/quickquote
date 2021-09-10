from app.extensions import db
import datetime


class PlanRatingAttributeModel(db.Model):
    __tablename__ = "plan_rating_attributes"

    plan_rating_attribute_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    plan_attribute_code = db.Column(db.String(20), nullable=False)
    plan_attribute_value = db.Column(db.String(100), nullable=False)
    plan_attribute_data_type = db.Column(db.String(10), nullable=False)

    row_eff_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    row_exp_dts = db.Column(
        db.DateTime, default=datetime.datetime(9999, 12, 31, 0, 0, 0))
    active_record_indicator = db.Column(db.String(1), default="Y")

    plan = db.relationship(
        "PlanModel", back_populates="plan_rating_attributes")

    def __repr__(self):
        return f"<Plan Rating Attribute Id: {self.plan_rating_attribute_id} -- Attribute Code: `{self.plan_attribute_code}`>"

    def getValue(self):
        if self.plan_attribute_data_type == 'number':
            if '.' in self.plan_attribute_value:
                return float(self.plan_attribute_value)
            return int(self.plan_attribute_value)
        if self.plan_attribute_data_type == 'boolean':
            return self.plan_attribute_value.lower() == 'true'
        return self.plan_attribute_value

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.plan_id == id).first()

    @classmethod
    def find_plan_rating_attributes(cls, plan_id):
        return cls.query.filter(cls.plan_id == plan_id, cls.active_record_indicator == 'Y').all()

    def save_to_db(self):
        try:
            db.session.add(self)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()
