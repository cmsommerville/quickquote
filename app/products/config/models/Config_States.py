from app.extensions import db
from app.shared import BaseModel

from .constants import TBL_NAMES

REF_STATE = TBL_NAMES['REF_STATE']


class Model_RefStates(BaseModel):
    __tablename__ = REF_STATE

    state_code = db.Column(db.String(2), primary_key=True)
    state_name = db.Column(db.String(100))

    def __repr__(self):
        return f"<{self.state_code}: {self.state_name}>"

    @classmethod
    def find(cls, code):
        return cls.query.filter(cls.state_code == code).first()
