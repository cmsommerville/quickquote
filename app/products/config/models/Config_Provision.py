import datetime
from sqlalchemy import between
from app.extensions import db
from app.shared import BaseModel, BaseModel

from .constants import TBL_NAMES

REF_COMPONENT_TYPES = TBL_NAMES["REF_COMPONENT_TYPES"]
REF_PROVISION = TBL_NAMES['REF_PROVISION']
REF_STATE = TBL_NAMES['REF_STATE']
REF_TEXT_FIELD_TYPES = TBL_NAMES['REF_TEXT_FIELD_TYPES']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
CONFIG_PROVISION = TBL_NAMES['CONFIG_PROVISION']
CONFIG_PROVISION_STATE_AVAILABILITY = TBL_NAMES['CONFIG_PROVISION_STATE_AVAILABILITY']
CONFIG_PROVISION_UI_COMPONENT = TBL_NAMES['CONFIG_PROVISION_UI_COMPONENT']


class Model_RefProvision(BaseModel):
    __tablename__ = REF_PROVISION

    provision_code = db.Column(db.String(30), primary_key=True)
    provision_label = db.Column(db.String(100))

    def __repr__(self):
        return f"<Provision Code: {self.provision_code}>"

    @classmethod
    def find(cls, code: str):
        return cls.query.filter(cls.provision_code == code).first()


class Model_ConfigProvision(BaseModel):
    __tablename__ = CONFIG_PROVISION
    __table_args__ = (
        db.UniqueConstraint('product_id', 'provision_code'),
        db.CheckConstraint('provision_effective_date <= provision_expiration_date')
    )

    provision_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT}.product_id"), nullable=False)
    provision_code = db.Column(db.ForeignKey(f"{REF_PROVISION}.provision_code"), nullable=False)
    provision_effective_date = db.Column(db.Date(), nullable=False)
    provision_expiration_date = db.Column(db.Date(), nullable=False)

    product = db.relationship(
        "Model_ConfigProduct", back_populates="provisions")
    provision = db.relationship("Model_RefProvision")
    states = db.relationship(
        "Model_ConfigProvisionStateAvailability", back_populates="provision")
    factors = db.relationship(
        "Model_ConfigFactor", back_populates="provision")

    def __repr__(self):
        return f"<Provision Id: {self.provision_id}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.provision_id == id).first()


class Model_ConfigProvisionStateAvailability(BaseModel):
    __tablename__ = CONFIG_PROVISION_STATE_AVAILABILITY
    __table_args__ = (
        db.UniqueConstraint('provision_id', 'state_id'),
        db.CheckConstraint('state_effective_date <= state_expiration_date')
    )

    provision_state_availability_id = db.Column(db.Integer, primary_key=True)
    provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION}.provision_id"), nullable=False)
    state_id = db.Column(db.ForeignKey(f"{REF_STATE}.state_code"), nullable=False)
    state_effective_date = db.Column(db.Date, nullable=False)
    state_expiration_date = db.Column(db.Date, nullable=False)

    provision = db.relationship(
        "Model_ConfigProvision", back_populates="states")

    def __repr__(self):
        return f"<Provision State Availability Id: {self.provision_state_availability_id} - State: {self.state_code}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.provision_state_availability_id == id).first()

class Model_RefComponentTypes(BaseModel):
    __tablename__ = REF_COMPONENT_TYPES

    component_type = db.Column(db.String(50), primary_key=True)

    def __repr__(self):
        return f"<Component Type: {self.component_type}>"

    @classmethod
    def find(cls, type: str):
        return cls.query.filter(cls.component_type == type).first()


class Model_RefTextFieldTypes(BaseModel):
    __tablename__ = REF_TEXT_FIELD_TYPES

    type_code = db.Column(db.String(30), primary_key=True)

    def __repr__(self):
        return f"<Type Code: {self.type_code}>"

    @classmethod
    def find(cls, type: str):
        return cls.query.filter(cls.type_code == type).first()


class Model_ConfigProvisionUIComponent(BaseModel):
    __tablename__ = CONFIG_PROVISION_UI_COMPONENT
    __table_args__ = (
        db.UniqueConstraint('provision_id'),
    )

    provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION}.provision_id"), primary_key=True)
    component_type = db.Column(
        db.String(50), db.ForeignKey(f"{REF_COMPONENT_TYPES}.component_type"))
    ui_label = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity': 'base_component',
        'polymorphic_on': component_type
    }

    def __repr__(self):
        return f"<Provision UI ID: {self.provision_id} - {self.component_type}>"

    @classmethod
    def find(cls, id: int):
        return cls.query.filter(cls.provision_id == id).first()


class Model_ConfigProvisionUIComponent_CheckboxField(Model_ConfigProvisionUIComponent):
    __tablename__ = f"{CONFIG_PROVISION_UI_COMPONENT}__checkbox"
    
    provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION_UI_COMPONENT}.provision_id"), primary_key=True)
    true_value = db.Column(db.String(100))
    false_value = db.Column(db.String(100))
    hint_value = db.Column(db.String(255))
    is_switch = db.Column(db.Boolean, default=False)

    __mapper_args__ = {
        'polymorphic_identity': 'checkbox',
    }


class Model_ConfigProvisionUIComponent_TextField(Model_ConfigProvisionUIComponent):
    __tablename__ = f"{CONFIG_PROVISION_UI_COMPONENT}__text_field"

    provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION_UI_COMPONENT}.provision_id"), primary_key=True)
    input_type = db.Column(db.String(30), db.ForeignKey(
        f"{REF_TEXT_FIELD_TYPES}.type_code"), default="input")
    min_value = db.Column(db.Float)
    max_value = db.Column(db.Float)
    step_value = db.Column(db.Float)

    __mapper_args__ = {
        'polymorphic_identity': 'text_field',
    }


class Model_ConfigProvisionUIComponent_SelectField(Model_ConfigProvisionUIComponent):
    __tablename__ = f"{CONFIG_PROVISION_UI_COMPONENT}__select"
    
    provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION_UI_COMPONENT}.provision_id"), primary_key=True)
    item_text = db.Column(db.String(100))
    item_value = db.Column(db.String(100))
    hint_value = db.Column(db.String(100))
    is_radio = db.Column(db.Boolean, default=False)

    __mapper_args__ = {
        'polymorphic_identity': 'select',
    }


class Model_ConfigProvisionUIComponent_SelectItemField(BaseModel):
    __tablename__ = f"{CONFIG_PROVISION_UI_COMPONENT}__select_items"

    ui_component_item_id = db.Column(db.Integer, primary_key=True)
    provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION_UI_COMPONENT}.provision_id"), primary_key=True)
    item_code = db.Column(db.String(30))
    item_label = db.Column(db.String(100))
