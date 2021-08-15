from app.models import db


class StateModel(db.Model):
    __tablename__ = "states"

    state_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state_code = db.Column(db.String(2), nullable=False)
    state_name = db.Column(db.String(50), nullable=False)

    @classmethod
    def find_by_id(cls, id):
        return db.session.query(cls).filter(cls.state_id == id).first()

    @classmethod
    def find_all(cls, num_rows=1000):
        return db.session.query(cls).limit(num_rows).all()

    def save_to_db(self):
        try:
            db.session.add(self)
        except:
            db.session.rollback()
        else:
            db.session.commit()
