import datetime
from sqlalchemy import between
from sqlalchemy.orm import contains_eager
from app.extensions import db
from app.shared import BaseModel

from .constants import TBL_NAMES
from .Config_States import Model_RefStates

REF_RATING_ALGORITHM = TBL_NAMES['REF_RATING_ALGORITHM']
REF_STATE = TBL_NAMES['REF_STATE']
CONFIG_AGE_BANDS = TBL_NAMES['CONFIG_AGE_BANDS']
CONFIG_AGE_BANDS_SET = TBL_NAMES['CONFIG_AGE_BANDS_SET']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
CONFIG_PRODUCT_VARIATIONS = TBL_NAMES['CONFIG_PRODUCT_VARIATIONS']



class Model_RefRatingAlgorithm(BaseModel):
    __tablename__ = REF_RATING_ALGORITHM

    rating_algorithm_code = db.Column(db.String(30), primary_key=True)
    rating_algorithm_label = db.Column(db.String(100))
    rating_algorithm_description = db.Column(db.String(1000))

    def __repr__(self):
        return f"<Rating Algorithm Code: {self.rating_algorithm_code}>"

    @classmethod
    def find(cls, code: str):
        return cls.query.filter(cls.rating_algorithm_code == code).first()


class Model_ConfigProductVariations(BaseModel):
    __tablename__ = CONFIG_PRODUCT_VARIATIONS
    __table_args__ = (
        db.UniqueConstraint('product_id', 'product_variation_code'),
        db.CheckConstraint('product_variation_effective_date <= product_variation_expiration_date')
    )

    product_variation_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT}.product_id"))
    product_variation_code = db.Column(db.String(30), nullable=False)

    product_variation_effective_date = db.Column(db.Date(), nullable=False)
    product_variation_expiration_date = db.Column(db.Date(), nullable=False)
    product_variation_label = db.Column(db.String(100), nullable=False)
    is_gender_rated = db.Column(db.Boolean, nullable=False)
    is_age_rated = db.Column(db.Boolean, nullable=False)
    is_tobacco_rated = db.Column(db.Boolean, nullable=False)
    is_family_code_rated = db.Column(db.Boolean, nullable=False)
    family_code_rating_algorithm_code = db.Column(db.String(30), db.ForeignKey(
        f"{REF_RATING_ALGORITHM}.rating_algorithm_code"))
    min_issue_age = db.Column(db.Integer)
    max_issue_age = db.Column(db.Integer)

    rating_algorithm = db.relationship("Model_RefRatingAlgorithm")
    product = db.relationship(
        "Model_ConfigProduct", back_populates="product_variations")
    age_band_sets = db.relationship(
        "Model_ConfigAgeBandsSet", back_populates="product_variation")

    def __repr__(self):
        return f"<Product Variation: {self.product_variation_id} - {self.product_variation_code}>"

    @classmethod
    def find(cls, id: int):
        return cls.query.filter(cls.product_variation_id == id).first()


class Model_ConfigAgeBandsSet(BaseModel):
    __tablename__ = CONFIG_AGE_BANDS_SET
    __table_args__ = (
        db.UniqueConstraint('product_variation_id', 'state_id'),
        db.CheckConstraint('age_band_effective_date <= age_band_expiration_date')
    )

    age_band_set_id = db.Column(db.Integer, primary_key = True)
    product_variation_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT_VARIATIONS}.product_variation_id"), nullable=False)
    state_id = db.Column(db.ForeignKey(f"{REF_STATE}.state_id"), nullable=False)

    age_band_effective_date = db.Column(db.Date, nullable=False)
    age_band_expiration_date = db.Column(db.Date, nullable=False)

    age_bands = db.relationship('Model_ConfigAgeBands')
    state = db.relationship("Model_RefStates")
    product_variation = db.relationship(
        "Model_ConfigProductVariations", back_populates="age_band_sets")

    def __repr__(self):
        return f"<Age Band Set: {self.age_band_set_id}>"
    
    @classmethod
    def find_by_state(
        cls, 
        state: str, 
        effective_date: datetime.date, 
        product_variation_id: int
        ): 

        # filter for product variation ID
        qry = db.session.query(cls)\
            .filter(cls.product_variation_id == product_variation_id)\
            .filter(between(
                effective_date, 
                cls.age_band_effective_date, 
                cls.age_band_expiration_date))\
            .filter(Model_RefStates.state_code == state)\
            .options(contains_eager(cls.state)).populate_existing()

        return qry.all()


class Model_ConfigAgeBands(BaseModel):
    __tablename__ = CONFIG_AGE_BANDS
    __table_args__ = (
        db.UniqueConstraint('age_band_set_id', 'age_band_lower'),
        db.CheckConstraint('age_band_lower <= age_band_upper')
    )

    age_band_id = db.Column(db.Integer, primary_key=True)
    age_band_set_id = db.Column(db.ForeignKey(f"{CONFIG_AGE_BANDS_SET}.age_band_set_id"),nullable=False)
    age_band_lower = db.Column(db.Integer, primary_key=True)
    age_band_upper = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<{str(self.age_band_lower)}-{str(self.age_band_upper)}: {self.age_band_set_id}>"
