from app.models import db


class ClaimCostModel(db.Model):
    __tablename__ = "claim_costs"

    claim_cost_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        "products.product_id"), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey(
        "states.state_id"), nullable=False)
    benefit_id = db.Column(db.Integer, db.ForeignKey(
        "benefits.benefit_id"), nullable=False)
    provision_id = db.Column(db.Integer, db.ForeignKey(
        "provisions.provision_id"), nullable=False)
    unit_value = db.Column(db.Float, nullable=False)
    modal_rate_per_unit = db.Column(db.Float, nullable=False)
    modes_per_year = db.Column(db.Integer, nullable=False)

    product = db.relationship("ProductModel")
    state = db.relationship("StateModel")
    benefit = db.relationship("BenefitModel")
    provision = db.relationship("ProvisionModel")

    @classmethod
    def find_by_id(cls, id):
        return db.session.query(cls).filter(claim_cost_id=id).first()
