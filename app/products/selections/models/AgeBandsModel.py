from app.extensions import db
from app.shared import VersionedTable
import datetime


class AgeBandsModel(db.Model, VersionedTable):
    __tablename__ = "age_bands"

    age_band_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    lower_age = db.Column(db.Integer, nullable=False)
    upper_age = db.Column(db.Integer, nullable=False)

    row_eff_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    row_exp_dts = db.Column(db.DateTime, default='9999-12-31 00:00:00.000')
    active_record_indicator = db.Column(db.String(1), default='Y')

    created_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_dts = db.Column(db.DateTime, default=db.func.current_timestamp())

    plan = db.relationship("PlanModel", back_populates="age_bands")

    def __repr__(self):
        return f"<Age Band Id: {self.age_band_id} -- Age Band: {self.lower_age}-{self.upper_age}>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.age_band_id == id).first()

    @classmethod
    def find_by_plan_id(cls, plan_id):
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
    def save_all_to_db(cls, age_bands, plan_id):
        try:
            for age_band in age_bands:
                db.session.add(age_band)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()

    @classmethod
    def delete_by_plan_id(cls, plan_id):
        try:
            age_bands_for_delete = cls.find_by_plan_id(plan_id)
            for band in age_bands_for_delete:
                db.session.delete(band)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()
