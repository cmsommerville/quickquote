from app.extensions import db
from app.shared import BaseModel

from ...__constants__ import TBL_NAMES

CONFIG_PROVISION_UI_COMPONENT = TBL_NAMES['CONFIG_PROVISION_UI_COMPONENT']
CONFIG_PROVISION = TBL_NAMES['CONFIG_PROVISION']
REF_COMPONENT_TYPES = TBL_NAMES['REF_COMPONENT_TYPES']
REF_TEXT_FIELD_TYPES = TBL_NAMES['REF_TEXT_FIELD_TYPES']


class Model_ConfigProvisionUIComponent(BaseModel):
    __tablename__ = CONFIG_PROVISION_UI_COMPONENT
    __table_args__ = (
        db.UniqueConstraint('provision_id'),
    )

    provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION}.provision_id"), primary_key=True)
    component_type  = db.Column(db.String(50), nullable=False)
    component_type_code = db.Column(
        db.String(50), db.ForeignKey(f"{REF_COMPONENT_TYPES}.component_type_code"), nullable=False)
    ui_label = db.Column(db.String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'BASE',
        'polymorphic_on': component_type
    }

    @classmethod
    def find_one(cls, id: int):
        res = cls.query.filter(cls.provision_id == id).first()
        if res is None:
            return
        if res.component_type == "INPUT":
            return Model_ConfigProvisionUIComponent_TextField.find_one(id)
        if res.component_type == "CHECKBOX": 
            return Model_ConfigProvisionUIComponent_CheckboxField.find_one(id)
        if res.component_type == "SELECT": 
            return Model_ConfigProvisionUIComponent_SelectField.find_one(id)


class Model_ConfigProvisionUIComponent_CheckboxField(Model_ConfigProvisionUIComponent):
    __tablename__ = f"{CONFIG_PROVISION_UI_COMPONENT}__checkbox"
    
    provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION_UI_COMPONENT}.provision_id"), primary_key=True)
    true_value = db.Column(db.String(100))
    false_value = db.Column(db.String(100))
    hint_value = db.Column(db.String(255))
    is_switch = db.Column(db.Boolean, default=False)

    __mapper_args__ = {
        'polymorphic_identity': 'CHECKBOX',
    }

    @classmethod
    def find_one(cls, id: int):
        return cls.query.filter(cls.provision_id == id).first()

class Model_ConfigProvisionUIComponent_TextField(Model_ConfigProvisionUIComponent):
    __tablename__ = f"{CONFIG_PROVISION_UI_COMPONENT}__text_field"

    provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION_UI_COMPONENT}.provision_id"), primary_key=True)
    input_type = db.Column(db.String(30), db.ForeignKey(
        f"{REF_TEXT_FIELD_TYPES}.type_code"), default="input")
    min_value = db.Column(db.Float)
    max_value = db.Column(db.Float)
    step_value = db.Column(db.Float)

    __mapper_args__ = {
        'polymorphic_identity': 'INPUT',
    }

    @classmethod
    def find_one(cls, id: int):
        return cls.query.filter(cls.provision_id == id).first()


class Model_ConfigProvisionUIComponent_SelectField(Model_ConfigProvisionUIComponent):
    __tablename__ = f"{CONFIG_PROVISION_UI_COMPONENT}__select"
    
    provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION_UI_COMPONENT}.provision_id"), primary_key=True)
    item_text = db.Column(db.String(100))
    item_value = db.Column(db.String(100))
    hint_value = db.Column(db.String(100))
    is_radio = db.Column(db.Boolean, default=False)

    items = db.relationship(
        "Model_ConfigProvisionUIComponent_SelectItemField")

    __mapper_args__ = {
        'polymorphic_identity': 'SELECT',
    }

    @classmethod
    def find_one(cls, id: int):
        return cls.query.filter(cls.provision_id == id).first()


class Model_ConfigProvisionUIComponent_SelectItemField(BaseModel):
    __tablename__ = f"{CONFIG_PROVISION_UI_COMPONENT}__select_items"

    ui_component_item_id = db.Column(db.Integer, primary_key=True)
    provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION_UI_COMPONENT}.provision_id"))
    item_code = db.Column(db.String(30))
    item_label = db.Column(db.String(100))

