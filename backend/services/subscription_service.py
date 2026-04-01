import logging
from datetime import date, timedelta
from typing import Optional

from extensions import db
from models.subscription import Subscription
from schemas.subscription_schema import CreateSubscriptionSchema, ValidationError
from utils.date_utils import get_current_date

logger = logging.getLogger(__name__)

UPCOMING_WINDOW_DAYS = 7


class SubscriptionService:

    @staticmethod
    def _assert_no_duplicate_active(name: str) -> None:
        existing = Subscription.query.filter_by(name=name, status="active").first()
        if existing:
            raise ValidationError(
                f"An active subscription named '{name}' already exists.",
                "SUB_001",
            )

    @staticmethod
    def _assert_future_or_today(next_billing_date: date, today: date) -> None:
        if next_billing_date < today:
            raise ValidationError(
                "next_billing_date must be today or in the future.",
                "SUB_002",
            )

    @classmethod
    def create(cls, raw_data: dict, mock_date: Optional[date] = None) -> Subscription:
        schema = CreateSubscriptionSchema.from_dict(raw_data)
        today = get_current_date(mock_date)

        cls._assert_no_duplicate_active(schema.name)
        cls._assert_future_or_today(schema.next_billing_date, today)

        subscription = Subscription(
            name=schema.name,
            cost=schema.cost,
            billing_cycle=schema.billing_cycle,
            next_billing_date=schema.next_billing_date,
            status="active",
            created_at=today,
        )
        db.session.add(subscription)
        db.session.commit()

        logger.info(
            "Subscription created: id=%s name=%r cost=%.2f cycle=%s next=%s",
            subscription.id, subscription.name, subscription.cost,
            subscription.billing_cycle, subscription.next_billing_date,
        )
        return subscription

    @staticmethod
    def list_all() -> list:
        return Subscription.query.order_by(Subscription.next_billing_date.asc()).all()

    @staticmethod
    def get_upcoming(mock_date: Optional[date] = None) -> list:
        today = get_current_date(mock_date)
        cutoff = today + timedelta(days=UPCOMING_WINDOW_DAYS)
        return (
            Subscription.query.filter(
                Subscription.status == "active",
                Subscription.next_billing_date >= today,
                Subscription.next_billing_date <= cutoff,
            )
            .order_by(Subscription.next_billing_date.asc())
            .all()
        )

    @staticmethod
    def monthly_cost_summary() -> dict:
        subscriptions = Subscription.query.filter_by(status="active").all()
        total_monthly = 0.0
        breakdown = []

        for sub in subscriptions:
            monthly_equiv = sub.cost if sub.billing_cycle == "monthly" else round(sub.cost / 12, 2)
            total_monthly += monthly_equiv
            breakdown.append({
                "id": sub.id,
                "name": sub.name,
                "billing_cycle": sub.billing_cycle,
                "cost": sub.cost,
                "monthly_equivalent": round(monthly_equiv, 2),
            })

        return {
            "total_monthly_cost": round(total_monthly, 2),
            "subscription_count": len(subscriptions),
            "breakdown": breakdown,
        }