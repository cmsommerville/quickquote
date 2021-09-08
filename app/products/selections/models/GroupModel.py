from app.extensions import db

from .PlanModel import PlanModel


class GroupModel(db.Model):
    __tablename__ = "groups"

    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(256), nullable=False)
    group_size = db.Column(db.Integer)
    sic_code = db.Column(db.String(6))
    tax_id = db.Column(db.String(10))
    row_add_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    # plans = db.relationship("PlanModel", back_populates="group")

    def __repr__(self):
        return f"<Group Id: {self.group_id} -- Group Name: `{self.group_name}`>"

    def reset(self, data):
        self.group_name = data.get("group_name")
        self.group_size = data.get("group_size")
        self.sic_code = data.get("sic_code")
        self.tax_id = data.get("tax_id")

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.group_id == id).first()

    def save_to_db(self):
        try:
            db.session.add(self)
        except:
            db.session.rollback()
        else:
            db.session.commit()
