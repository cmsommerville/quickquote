import datetime
from sqlalchemy import between
from sqlalchemy.orm import aliased
from app.extensions import db
from app.shared import BaseModel, BaseModel

from .constants import TBL_NAMES, COVERAGE_SECTION_DEFAULT
from .Config_States import Model_RefStates

REF_COVERAGE = TBL_NAMES['REF_COVERAGE']
REF_STATE = TBL_NAMES['REF_STATE']
CONFIG_COVERAGE = TBL_NAMES['CONFIG_COVERAGE']
CONFIG_COVERAGE_STATE_AVAILABILITY = TBL_NAMES['CONFIG_COVERAGE_STATE_AVAILABILITY']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']


class Model_ConfigCoverage(BaseModel):
    __tablename__ = CONFIG_COVERAGE
    __table_args__ = (
        db.UniqueConstraint('coverage_code', 'product_id'),
        db.CheckConstraint('coverage_effective_date <= coverage_expiration_date')
    )

    coverage_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT}.product_id"), nullable=False)
    coverage_code = db.Column(db.String(30), nullable=False)
    coverage_label = db.Column(db.String(100), nullable=False)
    coverage_effective_date = db.Column(db.Date(), nullable=False)
    coverage_expiration_date = db.Column(db.Date(), nullable=False)
    section_code = db.Column(db.String(30), default=COVERAGE_SECTION_DEFAULT)

    product = db.relationship(
        "Model_ConfigProduct", back_populates="coverages")
    states = db.relationship("Model_ConfigCoverageStateAvailability", back_populates="coverage")
    benefits = db.relationship("Model_ConfigBenefit", back_populates="coverage")

    def __repr__(self):
        return f"<Coverage ID: {self.coverage_id} - {self.coverage_code}>"


class Model_ConfigCoverageStateAvailability(BaseModel):
    __tablename__ = CONFIG_COVERAGE_STATE_AVAILABILITY
    __table_args__ = (
        db.UniqueConstraint('coverage_id', 'state_id', 'state_effective_date'),
        db.CheckConstraint('state_effective_date <= state_expiration_date')
    )

    coverage_state_availability_id = db.Column(db.Integer, primary_key=True)
    coverage_id = db.Column(db.ForeignKey(f"{CONFIG_COVERAGE}.coverage_id"), nullable=False)
    state_id = db.Column(db.ForeignKey(f"{REF_STATE}.state_id"), nullable=False)
    state_effective_date = db.Column(db.Date, nullable=False)
    state_expiration_date = db.Column(db.Date, nullable=False)

    coverage = db.relationship("Model_ConfigCoverage", back_populates="states")
