from datetime import date
from extensions import db


class BillingEvent(db.Model):
    __tablename__ = "billing_events"

    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(
        db.Integer, db.ForeignKey("subscriptions.id"), nullable=False
    )
    amount = db.Column(db.Float, nullable=False)
    billed_on = db.Column(db.Date, nullable=False, default=date.today)
    billing_cycle = db.Column(db.String(20), nullable=False)
    next_billing_date_after = db.Column(db.Date, nullable=False)

    subscription = db.relationship("Subscription", back_populates="billing_events")

    def to_dict(self):
        return {
            "id": self.id,
            "subscription_id": self.subscription_id,
            "subscription_name": self.subscription.name if self.subscription else None,
            "amount": self.amount,
            "billed_on": self.billed_on.isoformat(),
            "billing_cycle": self.billing_cycle,
            "next_billing_date_after": self.next_billing_date_after.isoformat(),
        }