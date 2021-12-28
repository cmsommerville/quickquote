from app.extensions import db
from app.shared import BaseModel

from ...__constants__ import TBL_NAMES

CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
CONFIG_PRODUCT_VARIATIONS = TBL_NAMES['CONFIG_PRODUCT_VARIATIONS']
REF_RATING_ALGORITHM = TBL_NAMES['REF_RATING_ALGORITHM']



class Model_ConfigProductVariation(BaseModel):
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
        "Model_ConfigAgeBandSet", back_populates="product_variation")
    benefits = db.relationship(
        "Model_ConfigBenefitProductVariation", back_populates="product_variation")

    @classmethod
    def find_by_product(cls, id: int):
        return cls.query.filter(cls.product_id == id).all()

