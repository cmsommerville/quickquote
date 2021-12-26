from sqlalchemy import between, or_
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import ValidationError
from app.extensions import db
from app.shared import BaseModel

from .__constants__ import TBL_NAMES

CONFIG_BENEFIT = TBL_NAMES['CONFIG_BENEFIT']
CONFIG_COVERAGE = TBL_NAMES['CONFIG_COVERAGE']
CONFIG_RATE_GROUP = TBL_NAMES['CONFIG_RATE_GROUP']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
REF_BENEFIT = TBL_NAMES['REF_BENEFIT']
REF_STATE = TBL_NAMES['REF_STATE']
REF_UNIT_CODE = TBL_NAMES['REF_UNIT_CODE']


class Model_ConfigBenefit(BaseModel):
    __tablename__ = CONFIG_BENEFIT

    __table_args__ = (
        db.UniqueConstraint('benefit_code', 'product_id', 'state_id', 'benefit_effective_date'),
        db.CheckConstraint('benefit_effective_date <= benefit_expiration_date'),
    )

    benefit_id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, 
        db.ForeignKey(f"{CONFIG_BENEFIT}.benefit_id"))
    product_id = db.Column(db.ForeignKey(
        f"{CONFIG_PRODUCT}.product_id"), nullable=False)
    state_id = db.Column(db.ForeignKey(
        f"{REF_STATE}.state_id"), nullable=False)
    benefit_code = db.Column(db.ForeignKey(
        f"{REF_BENEFIT}.benefit_code"), nullable=False)
    benefit_effective_date = db.Column(db.Date(), nullable=False)
    benefit_expiration_date = db.Column(db.Date(), nullable=False)
    coverage_id = db.Column(db.ForeignKey(
        f"{CONFIG_COVERAGE}.coverage_id"))
    rate_group_id = db.Column(db.ForeignKey(
        f"{CONFIG_RATE_GROUP}.rate_group_id"))
    min_value = db.Column(db.Numeric(12, 2))
    max_value = db.Column(db.Numeric(12, 2))
    step_value = db.Column(db.Numeric(12, 4))
    unit_code = db.Column(db.String(30), db.ForeignKey(
        f"{REF_UNIT_CODE}.unit_code"))
    is_durational = db.Column(db.Boolean)

    state = db.relationship("Model_RefStates")
    child_states = db.relationship("Model_ConfigBenefit",  
        backref=db.backref('parent_benefit', remote_side=[benefit_id]))

    product = db.relationship(
        "Model_ConfigProduct", back_populates="benefits")
    product_variations = db.relationship(
        "Model_ConfigBenefitProductVariation", back_populates="benefit")
    coverage = db.relationship(
        "Model_ConfigCoverage", back_populates="benefits")
    ref_benefit = db.relationship("Model_RefBenefit")
    rate_group = db.relationship("Model_ConfigRateGroup")
    durations = db.relationship(
        "Model_ConfigBenefitDuration", back_populates="benefit")
    state = db.relationship("Model_RefStates")

    @hybrid_property
    def benefit(self):
        if self.parent_id:
            return self.parent_benefit
        return self

    @classmethod
    def find_by_product(cls, id):
        return cls.query.filter(cls.product_id == id, cls.parent_id == None).all()

    @classmethod
    def find_child_states(cls, id):
        if cls.query.filter(cls.parent_id == id).count() == 0:
            return cls.query.filter(cls.benefit_id == id, cls.state_id > 0).order_by(cls.state_id).all()
        return cls.query.filter(cls.parent_id == id).order_by(cls.state_id).all()

    def isOverlappingInterval(self):
        """
        Check if there is another record for the same state/benefit
        that overlaps by effective interval. 
        """
        return Model_ConfigBenefit.query.filter(
            Model_ConfigBenefit.benefit_code == self.benefit_code, 
            Model_ConfigBenefit.product_id == self.product_id, 
            Model_ConfigBenefit.state_id == self.state_id, 
            or_(
                between(self.benefit_effective_date, Model_ConfigBenefit.benefit_effective_date, Model_ConfigBenefit.benefit_expiration_date), 
                between(self.benefit_expiration_date, Model_ConfigBenefit.benefit_effective_date, Model_ConfigBenefit.benefit_expiration_date)
            ) 
        ).count() > 0

    def save_to_db(self):
        if self.benefit_id is not None: 
            super().save_to_db()
            return
        if self.isOverlappingInterval(): 
            raise ValidationError("Benefit already exists in this state")
        super().save_to_db()
        
