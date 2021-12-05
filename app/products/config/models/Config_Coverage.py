import datetime
from sqlalchemy import between
from sqlalchemy.orm import contains_eager, aliased
from app.extensions import db
from app.shared import BaseModel, BaseModel

from .constants import TBL_NAMES, COVERAGE_SECTION_DEFAULT
from .Config_States import Model_RefStates
from .Config_Benefit import Model_ConfigBenefit, Model_ConfigBenefitStateAvailability

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


    @classmethod
    def find_by_state(
        cls, 
        state: str, 
        effective_date: datetime.date, 
        product_id: int
        ): 

        CSA = aliased(Model_ConfigCoverageStateAvailability, name='CSA')
        BSA = aliased(Model_ConfigBenefitStateAvailability, name='BSA')
        RefStateCov = aliased(Model_RefStates)
        RefStateBnft = aliased(Model_RefStates)

        # filter effective dates on product
        qry = db.session.query(cls)\
            .filter(between(
                effective_date, 
                cls.coverage_effective_date, 
                cls.coverage_expiration_date))

        # filter for product ID
        qry = qry.filter(cls.product_id == product_id)
    
        # filter coverage and benefit state availability
        qry = qry.join(cls.states)\
            .join(RefStateCov, CSA.state)\
            .join(RefStateBnft, BSA.state)\
            .filter(
                RefStateCov.state_code == state, 
                between(
                    effective_date, 
                    CSA.state_effective_date, 
                    CSA.state_expiration_date)
                )\
            .filter(
                RefStateBnft.state_code == state, 
                between(
                    effective_date, 
                    BSA.state_effective_date, 
                    BSA.state_expiration_date)
            ).options(contains_eager(cls.states)).populate_existing()

        return qry.all()



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

    state = db.relationship("Model_RefStates")
    coverage = db.relationship("Model_ConfigCoverage", back_populates="states")
