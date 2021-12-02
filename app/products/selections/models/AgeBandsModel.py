from app.extensions import db
from app.shared import BaseModel
import datetime


class AgeBandsModel(BaseModel):
    __tablename__ = "selections_age_bands"

    age_band_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('selections_plans.plan_id'))
    lower_age = db.Column(db.Integer, nullable=False)
    upper_age = db.Column(db.Integer, nullable=False)

    plan = db.relationship("PlanModel", back_populates="age_bands")

    def __repr__(self):
        return f"<Age Band Id: {self.age_band_id} -- Age Band: {self.lower_age}-{self.upper_age}>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.age_band_id == id).first()

    @classmethod
    def find_by_plan_id(cls, plan_id):
        return cls.query.filter(cls.plan_id == plan_id).all()

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
