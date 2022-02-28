from app.extensions import db
from app.products.config.models.Config_AgeDistributionSet import CONFIG_AGE_DISTRIBUTION_SET
from app.shared import BaseModel

from ...__constants__ import TBL_NAMES

CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
CONFIG_PRODUCT_VARIATIONS = TBL_NAMES['CONFIG_PRODUCT_VARIATIONS']
CONFIG_AGE_DISTRIBUTION_SET = TBL_NAMES['CONFIG_AGE_DISTRIBUTION_SET']
CONFIG_ATTRIBUTE_DISTRIBUTION_SET = TBL_NAMES['CONFIG_ATTRIBUTE_DISTRIBUTION_SET']
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
    product_variation_label = db.Column(db.String(100), nullable=False)
    product_variation_effective_date = db.Column(db.Date(), nullable=False)
    product_variation_expiration_date = db.Column(db.Date(), nullable=False)
    is_gender_rated = db.Column(db.Boolean, nullable=False)
    is_age_rated = db.Column(db.Boolean, nullable=False)
    is_tobacco_rated = db.Column(db.Boolean, nullable=False)
    is_family_code_rated = db.Column(db.Boolean, nullable=False)
    vary_by_gender = db.Column(db.Boolean, nullable=False)
    vary_by_tobacco = db.Column(db.Boolean, nullable=False)

    age_distribution_set_id = db.Column(db.ForeignKey(F"{CONFIG_AGE_DISTRIBUTION_SET}.age_distribution_set_id"))
    sex_distinct_distribution_set_id = db.Column(db.ForeignKey(F"{CONFIG_ATTRIBUTE_DISTRIBUTION_SET}.attr_distribution_set_id"))
    unisex_distribution_set_id = db.Column(db.ForeignKey(F"{CONFIG_ATTRIBUTE_DISTRIBUTION_SET}.attr_distribution_set_id"))
    smoker_distinct_distribution_set_id = db.Column(db.ForeignKey(F"{CONFIG_ATTRIBUTE_DISTRIBUTION_SET}.attr_distribution_set_id"))
    unismoker_distribution_set_id = db.Column(db.ForeignKey(F"{CONFIG_ATTRIBUTE_DISTRIBUTION_SET}.attr_distribution_set_id"))
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

    age_distribution = db.relationship("Model_ConfigAgeDistributionSet")
    sex_distinct_distribution = db.relationship("Model_ConfigAttributeDistributionSet", 
        primaryjoin="Model_ConfigProductVariation.sex_distinct_distribution_set_id == Model_ConfigAttributeDistributionSet.attr_distribution_set_id")
    unisex_distribution = db.relationship("Model_ConfigAttributeDistributionSet", 
        primaryjoin="Model_ConfigProductVariation.unisex_distribution_set_id == Model_ConfigAttributeDistributionSet.attr_distribution_set_id")
    smoker_distinct_distribution = db.relationship("Model_ConfigAttributeDistributionSet", 
        primaryjoin="Model_ConfigProductVariation.smoker_distinct_distribution_set_id == Model_ConfigAttributeDistributionSet.attr_distribution_set_id")
    unismoker_distribution = db.relationship("Model_ConfigAttributeDistributionSet", 
        primaryjoin="Model_ConfigProductVariation.unismoker_distribution_set_id == Model_ConfigAttributeDistributionSet.attr_distribution_set_id")

    @classmethod
    def find_by_product(cls, id: int):
        return cls.query.filter(cls.product_id == id).all()

