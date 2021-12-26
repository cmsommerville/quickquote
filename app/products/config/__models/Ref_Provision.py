from app.extensions import db
from app.shared import BaseModel

from .constants import TBL_NAMES

REF_PROVISION = TBL_NAMES['REF_PROVISION']


class Model_RefProvision(BaseModel):
    __tablename__ = REF_PROVISION

    provision_code = db.Column(db.String(30), primary_key=True)
    provision_label = db.Column(db.String(100))
