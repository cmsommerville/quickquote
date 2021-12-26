from app.extensions import db
from app.shared import BaseModel

from .__constants__ import TBL_NAMES

CONFIG_BENEFIT = TBL_NAMES['CONFIG_BENEFIT']
CONFIG_BENEFIT_PROVISION_APPLICABILITY = TBL_NAMES['CONFIG_BENEFIT_PROVISION_APPLICABILITY']
CONFIG_PROVISION = TBL_NAMES['CONFIG_PROVISION']



class Model_ConfigBenefitProvision(BaseModel):
    __tablename__ = CONFIG_BENEFIT_PROVISION_APPLICABILITY
    __table_args__ = (
        db.UniqueConstraint('benefit_id', 'provision_id'),
    )

    benefit_provision_id = db.Column(db.Integer, primary_key=True)
    benefit_id = db.Column(db.ForeignKey(
        f'{CONFIG_BENEFIT}.benefit_id'), nullable=False)
    provision_id = db.Column(db.ForeignKey(
        f'{CONFIG_PROVISION}.provision_id'), nullable=False)

    benefit = db.relationship("Model_ConfigBenefit")
    provisions = db.relationship("Model_ConfigProvision")

    @classmethod
    def find_provisions(cls, benefit_id):
        return cls.query.filter(cls.benefit_id == benefit_id).all()

    @classmethod
    def find_benefits(cls, provision_id):
        return cls.query.filter(cls.provision_id == provision_id).all()