import logging
from datetime import date
from typing import Optional

from extensions import db
from models.subscription import Subscription
from models.billing_event import BillingEvent
from utils.date_utils import get_current_date, advance_billing_date

logger = logging.getLogger(__name__)


class BillingService:

    @classmethod
    def run_billing(cls, mock_date: Optional[date] = None) -> dict:
        today = get_current_date(mock_date)
        logger.info("Billing run started. Reference date: %s", today)

        active_subscriptions = Subscription.query.filter_by(status="active").all()
        processed = []
        skipped = []

        for sub in active_subscriptions:
            if today >= sub.next_billing_date:
                event = cls._bill_subscription(sub, today)
                processed.append({
                    "subscription_id": sub.id,
                    "subscription_name": sub.name,
                    "amount_billed": event.amount,
                    "billed_on": event.billed_on.isoformat(),
                    "new_next_billing_date": sub.next_billing_date.isoformat(),
                })
            else:
                skipped.append({
                    "subscription_id": sub.id,
                    "subscription_name": sub.name,
                    "next_billing_date": sub.next_billing_date.isoformat(),
                })

        db.session.commit()
        logger.info("Billing run complete. Processed: %d, Skipped: %d", len(processed), len(skipped))

        return {
            "run_date": today.isoformat(),
            "processed_count": len(processed),
            "skipped_count": len(skipped),
            "processed": processed,
            "skipped": skipped,
        }

    @staticmethod
    def _bill_subscription(sub: Subscription, today: date) -> BillingEvent:
        new_next_date = advance_billing_date(sub.next_billing_date, sub.billing_cycle)

        event = BillingEvent(
            subscription_id=sub.id,
            amount=sub.cost,
            billed_on=today,
            billing_cycle=sub.billing_cycle,
            next_billing_date_after=new_next_date,
        )
        db.session.add(event)
        sub.next_billing_date = new_next_date

        logger.info(
            "Billed: id=%s name=%r amount=%.2f new_next=%s",
            sub.id, sub.name, sub.cost, new_next_date,
        )
        return event

    @staticmethod
    def get_billing_events(subscription_id: Optional[int] = None) -> list:
        query = BillingEvent.query
        if subscription_id is not None:
            query = query.filter_by(subscription_id=subscription_id)
        return query.order_by(BillingEvent.billed_on.desc()).all()