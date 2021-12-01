import datetime
from sqlalchemy import between
from app.extensions import db
from app.shared import BaseVersionedModel, BaseModel

from .constants import TBL_NAMES
from .Config_States import REF_STATE, Model_RefStates

REF_PLAN_VARIATIONS = TBL_NAMES['REF_PLAN_VARIATIONS']
REF_RATING_ALGORITHM = TBL_NAMES['REF_RATING_ALGORITHM']
REF_STATE = TBL_NAMES['REF_STATE']
CONFIG_AGE_BANDS = TBL_NAMES['CONFIG_AGE_BANDS']
CONFIG_AGE_BANDS_SET = TBL_NAMES['CONFIG_AGE_BANDS_SET']
CONFIG_PLAN = TBL_NAMES['CONFIG_PLAN']
CONFIG_PLAN_VARIATIONS = TBL_NAMES['CONFIG_PLAN_VARIATIONS']


class Model_RefPlanVariations(BaseModel):
    __tablename__ = REF_PLAN_VARIATIONS

    plan_variation_code = db.Column(db.String(30), primary_key=True)
    plan_variation_label = db.Column(db.String(100))

    def __repr__(self):
        return f"<Plan Variation Code: {self.plan_variation_code}>"

    @classmethod
    def find(cls, code: str):
        return cls.query.filter(cls.plan_variation_code == code).first()


class Model_RefRatingAlgorithm(BaseModel):
    __tablename__ = REF_RATING_ALGORITHM

    rating_algorithm_code = db.Column(db.String(30), primary_key=True)
    rating_algorithm_label = db.Column(db.String(100))
    rating_algorithm_description = db.Column(db.String(1000))

    def __repr__(self):
        return f"<Plan Variation Code: {self.rating_algorithm_code}>"

    @classmethod
    def find(cls, code: str):
        return cls.query.filter(cls.rating_algorithm_code == code).first()


class Model_ConfigPlanVariations(BaseVersionedModel):
    __tablename__ = CONFIG_PLAN_VARIATIONS

    plan_variation_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_PLAN}.plan_id"), nullable=False)
    plan_variation_code = db.Column(
        db.String(30), db.ForeignKey(f"{REF_PLAN_VARIATIONS}.plan_variation_code"), nullable=False)
    plan_variation_effective_date = db.Column(db.Date(), nullable=False)
    plan_variation_expiration_date = db.Column(db.Date(), nullable=False)
    is_gender_rated = db.Column(db.Boolean, nullable=False)
    is_age_rated = db.Column(db.Boolean, nullable=False)
    is_tobacco_rated = db.Column(db.Boolean, nullable=False)
    is_family_code_rated = db.Column(db.Boolean, nullable=False)
    family_code_rating_algorithm = db.Column(db.String(30), db.ForeignKey(
        f"{REF_RATING_ALGORITHM}.rating_algorithm_code"))
    min_issue_age = db.Column(db.Integer)
    max_issue_age = db.Column(db.Integer)

    plan_variation = db.relationship("Model_RefPlanVariations")
    plan = db.relationship(
        "Model_ConfigPlan", back_populates="plan_variations")
    age_band_sets = db.relationship(
        "Model_ConfigAgeBandsSet", back_populates="plan_variation")

    def __repr__(self):
        return f"<Plan Variation Id: {self.plan_variation_id}>"

    @classmethod
    def find(cls, id: int):
        return cls.query.filter(cls.plan_variation_id == id).first()


class Model_ConfigAgeBandsSet(BaseVersionedModel):
    __tablename__ = CONFIG_AGE_BANDS_SET

    age_band_set_id = db.Column(db.Integer, primary_key=True)
    plan_variation_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_PLAN_VARIATIONS}.plan_variation_id"))
    state_code = db.Column(
        db.String(2), db.ForeignKey(f"{REF_STATE}.state_code"))
    age_band_effective_date = db.Column(db.Date, nullable=False)
    age_band_expiration_date = db.Column(db.Date, nullable=False)

    age_bands = db.relationship('Model_ConfigAgeBands')
    plan_variation = db.relationship(
        "Model_ConfigPlanVariations", back_populates="age_band_sets")

    def __repr__(self):
        return f"<Age Band Set Id: {self.age_band_set_id}>"

    @classmethod
    def find_by_state(cls, state: str, effective_date: datetime.date, default_value: str = 'XX'):
        base_query = cls.query.filter(between(
            effective_date, cls.age_band_effective_date, cls.age_band_expiration_date))
        query = base_query.filter(cls.state_code == state)
        if query.first() is None:
            query = base_query.filter(cls.state_code == default_value)

        return query.all()

    @classmethod
    def find(cls, id: int):
        return cls.query.filter(cls.age_band_set_id == id).first()


class Model_ConfigAgeBands(BaseVersionedModel):
    __tablename__ = CONFIG_AGE_BANDS

    age_band_id = db.Column(db.Integer, primary_key=True)
    age_band_set_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_AGE_BANDS_SET}.age_band_set_id"))
    age_band_lower = db.Column(db.Integer, nullable=False)
    age_band_upper = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Age Band Id: {self.age_band_id}>"
