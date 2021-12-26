import datetime
from sqlalchemy import DDL, event, between, or_
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import ValidationError
from app.extensions import db
from app.shared import BaseModel

from .constants import TBL_NAMES, FACTOR_DECIMAL_PRECISION

REF_BENEFIT = TBL_NAMES['REF_BENEFIT']
REF_BENEFIT_DURATION = TBL_NAMES['REF_BENEFIT_DURATION']
REF_BENEFIT_DURATION_ITEMS = TBL_NAMES['REF_BENEFIT_DURATION_ITEMS']
REF_STATE = TBL_NAMES['REF_STATE']
REF_UNIT_CODE = TBL_NAMES['REF_UNIT_CODE']
CONFIG_BENEFIT = TBL_NAMES['CONFIG_BENEFIT']
CONFIG_BENEFIT_DURATION = TBL_NAMES['CONFIG_BENEFIT_DURATION']
CONFIG_BENEFIT_DURATION_ITEMS = TBL_NAMES['CONFIG_BENEFIT_DURATION_ITEMS']
CONFIG_BENEFIT_PRODUCT_VARIATION_APPLICABILITY = TBL_NAMES['CONFIG_BENEFIT_PRODUCT_VARIATION_APPLICABILITY']
CONFIG_BENEFIT_PROVISION_APPLICABILITY = TBL_NAMES['CONFIG_BENEFIT_PROVISION_APPLICABILITY']
CONFIG_BENEFIT_STATE_AVAILABILITY = TBL_NAMES['CONFIG_BENEFIT_STATE_AVAILABILITY']
CONFIG_COVERAGE = TBL_NAMES['CONFIG_COVERAGE']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
CONFIG_PRODUCT_VARIATIONS = TBL_NAMES['CONFIG_PRODUCT_VARIATIONS']
CONFIG_PROVISION = TBL_NAMES['CONFIG_PROVISION']
CONFIG_RATE_GROUP = TBL_NAMES['CONFIG_RATE_GROUP']


class Model_RefBenefit(BaseModel):
    __tablename__ = REF_BENEFIT

    benefit_code = db.Column(db.String(30), primary_key=True)
    benefit_label = db.Column(db.String(100))

    def __repr__(self):
        return f"<Benefit Code: {self.benefit_code}>"

    @classmethod
    def find(cls, code: str):
        return cls.query.filter(cls.benefit_code == code).first()


class Model_RefUnitCode(BaseModel):
    __tablename__ = REF_UNIT_CODE

    unit_code = db.Column(db.String(30), primary_key=True)
    unit_label = db.Column(db.String(100))

    def __repr__(self):
        return f"<Unit Code: {self.unit_code}>"

    @classmethod
    def find(cls, code: str):
        return cls.query.filter(cls.unit_code == code).first()


class Model_RefBenefitDuration(BaseModel):
    __tablename__ = REF_BENEFIT_DURATION

    duration_code = db.Column(db.String(30), primary_key=True)
    duration_label = db.Column(db.String(100))

    def __repr__(self):
        return f"<Duration Code: {self.duration_code}>"

    @classmethod
    def find(cls, code: str):
        return cls.query.filter(cls.duration_code == code).first()


class Model_RefBenefitDurationItems(BaseModel):
    __tablename__ = REF_BENEFIT_DURATION_ITEMS

    item_code = db.Column(db.String(30), primary_key=True)
    item_label = db.Column(db.String(100))

    def __repr__(self):
        return f"<Item Code: {self.item_code}>"

    @classmethod
    def find(cls, code: str):
        return cls.query.filter(cls.item_code == code).first()


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
    # parent_benefit = db.relationship("Model_ConfigBenefit", remote_side=[benefit_id])
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
    def find(cls, id):
        return cls.query.filter(cls.benefit_id == id).first()

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
        


class Model_ConfigBenefitProductVariation(BaseModel):
    __tablename__ = CONFIG_BENEFIT_PRODUCT_VARIATION_APPLICABILITY

    benefit_id = db.Column(db.ForeignKey(f"{CONFIG_BENEFIT}.benefit_id"), primary_key=True)
    product_variation_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT_VARIATIONS}.product_variation_id"), primary_key=True)

    benefit = db.relationship(
        "Model_ConfigBenefit", back_populates="product_variations")
    product_variation = db.relationship(
        "Model_ConfigProductVariations", back_populates="benefits")

    def __repr__(self):
        return f"<Benefit Id: {self.benefit_id} - Variation ID: {self.product_variation_id}>"
    
    @classmethod
    def find(cls, benefit_id, product_variation_id):
        return cls.query.filter(
            cls.benefit_id == benefit_id, 
            cls.product_variation_id == product_variation_id).first()

    @classmethod
    def find_benefits(cls, id):
        return cls.query.filter(cls.benefit_id == id).all()

    @classmethod
    def find_product_variations(cls, id):
        return cls.query.filter(cls.product_variation_id == id).all()



class Model_ConfigBenefitProvisionApplicability(BaseModel):
    __tablename__ = CONFIG_BENEFIT_PROVISION_APPLICABILITY

    benefit_id = db.Column(db.ForeignKey(
        f'{CONFIG_BENEFIT}.benefit_id'), primary_key=True)
    provision_id = db.Column(db.ForeignKey(
        f'{CONFIG_PROVISION}.provision_id'), primary_key=True)

    @classmethod
    def find(cls, benefit_id, provision_id):
        return cls.query.filter(
            cls.benefit_id == benefit_id, 
            cls.provision_id == provision_id).first()

    @classmethod
    def find_provisions(cls, benefit_id):
        return cls.query.filter(cls.benefit_id == benefit_id).all()

    @classmethod
    def find_benefits(cls, provision_id):
        return cls.query.filter(cls.provision_id == provision_id).all()


class Model_ConfigBenefitDuration(BaseModel):
    __tablename__ = CONFIG_BENEFIT_DURATION
    __table_args__ = (
        db.UniqueConstraint('benefit_id', 'benefit_duration_code'),
    )

    benefit_duration_id = db.Column(db.Integer, primary_key=True)
    benefit_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_BENEFIT}.benefit_id"))
    benefit_duration_code = db.Column(
        db.String(30), db.ForeignKey(f"{REF_BENEFIT_DURATION}.duration_code"))

    benefit = db.relationship("Model_ConfigBenefit",
                              back_populates="durations")
    duration = db.relationship("Model_RefBenefitDuration")
    duration_items = db.relationship(
        "Model_ConfigBenefitDurationItems", back_populates="duration", lazy="joined")

    def __repr__(self):
        return f"<Benefit Duration Id: {self.benefit_duration_id}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.benefit_duration_id == id).first()

    @classmethod
    def find_by_benefit(cls, id):
        return cls.query.filter(cls.benefit_id == id).all()


class Model_ConfigBenefitDurationItems(BaseModel):
    __tablename__ = CONFIG_BENEFIT_DURATION_ITEMS
    __table_args__ = (
        db.UniqueConstraint('benefit_duration_id', 'item_code'),
    )

    benefit_duration_item_id = db.Column(db.Integer, primary_key=True)
    benefit_duration_id = db.Column(db.ForeignKey(f"{CONFIG_BENEFIT_DURATION}.benefit_duration_id"), nullable=False)
    item_code = db.Column(db.ForeignKey(f"{REF_BENEFIT_DURATION_ITEMS}.item_code"), nullable=False)
    benefit_duration_factor = db.Column(
        db.Numeric(FACTOR_DECIMAL_PRECISION + 3, FACTOR_DECIMAL_PRECISION), nullable=False)

    duration = db.relationship(
        "Model_ConfigBenefitDuration", back_populates="duration_items")

    duration_item = db.relationship("Model_RefBenefitDurationItems")
        
    def __repr__(self):
        return f"<Benefit Duration Item Id: {self.benefit_duration_item_id}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.benefit_duration_item_id == id).first()
