from app.extensions import db
from app.shared import BaseModel

from .__constants__ import TBL_NAMES

CONFIG_PROVISION_STATE_AVAILABILITY = TBL_NAMES['CONFIG_PROVISION_STATE_AVAILABILITY']
CONFIG_PROVISION = TBL_NAMES['CONFIG_PROVISION']
REF_STATE = TBL_NAMES['REF_STATE']


class Model_ConfigProvisionStateAvailability(BaseModel):
    __tablename__ = CONFIG_PROVISION_STATE_AVAILABILITY
    __table_args__ = (
        db.UniqueConstraint('provision_id', 'state_id'),
        db.CheckConstraint('state_effective_date <= state_expiration_date')
    )

    provision_state_id = db.Column(db.Integer, primary_key=True)
    provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION}.provision_id"), nullable=False)
    state_id = db.Column(db.ForeignKey(f"{REF_STATE}.state_id"), nullable=False)
    state_effective_date = db.Column(db.Date, nullable=False)
    state_expiration_date = db.Column(db.Date, nullable=False)

    provision = db.relationship(
        "Model_ConfigProvision", back_populates="states")
    state = db.relationship("Model_RefStates")

    @classmethod
    def find_by_provision(cls, id):
        return cls.query.filter(cls.provision_id == id).all()

