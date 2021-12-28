from app.extensions import db
from app.shared import BaseModel

from ...__constants__ import TBL_NAMES

CONFIG_AGE_BANDS_SET = TBL_NAMES['CONFIG_AGE_BANDS_SET']
CONFIG_PRODUCT_VARIATIONS = TBL_NAMES['CONFIG_PRODUCT_VARIATIONS']
REF_STATE = TBL_NAMES['REF_STATE']

class Model_ConfigAgeBandSet(BaseModel):
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

    age_bands = db.relationship('Model_ConfigAgeBand')
    state = db.relationship("Model_RefStates")
    product_variation = db.relationship(
        "Model_ConfigProductVariation", back_populates="age_band_sets")

    @classmethod
    def find_by_variation(cls, id):
        return cls.query.filter(cls.product_variation_id == id).all()