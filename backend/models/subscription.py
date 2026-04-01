from datetime import date
from extensions import db


class Subscription(db.Model):
    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    cost = db.Column(db.Float, nullable=False)
    billing_cycle = db.Column(db.String(20), nullable=False)
    next_billing_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="active")
    created_at = db.Column(db.Date, nullable=False, default=date.today)

    billing_events = db.relationship(
        "BillingEvent", back_populates="subscription", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cost": self.cost,
            "billing_cycle": self.billing_cycle,
            "next_billing_date": self.next_billing_date.isoformat(),
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }