from datetime import date
from dataclasses import dataclass

VALID_BILLING_CYCLES = {"monthly", "yearly"}


class ValidationError(Exception):
    def __init__(self, message: str, code: str):
        super().__init__(message)
        self.message = message
        self.code = code

    def to_dict(self):
        return {"error": self.message, "code": self.code}


@dataclass
class CreateSubscriptionSchema:
    name: str
    cost: float
    billing_cycle: str
    next_billing_date: date

    @classmethod
    def from_dict(cls, data: dict) -> "CreateSubscriptionSchema":
        name = data.get("name", "").strip()
        if not name:
            raise ValidationError("Field 'name' is required.", "VAL_001")

        raw_cost = data.get("cost")
        if raw_cost is None:
            raise ValidationError("Field 'cost' is required.", "VAL_002")
        try:
            cost = float(raw_cost)
        except (TypeError, ValueError):
            raise ValidationError("Field 'cost' must be a number.", "VAL_003")
        if cost <= 0:
            raise ValidationError("cost must be greater than 0.", "VAL_004")

        billing_cycle = data.get("billing_cycle", "").strip().lower()
        if billing_cycle not in VALID_BILLING_CYCLES:
            raise ValidationError(
                f"billing_cycle must be one of {sorted(VALID_BILLING_CYCLES)}.",
                "VAL_005",
            )

        raw_date = data.get("next_billing_date")
        if not raw_date:
            raise ValidationError("Field 'next_billing_date' is required.", "VAL_006")
        try:
            next_billing_date = (
                raw_date if isinstance(raw_date, date)
                else date.fromisoformat(str(raw_date))
            )
        except ValueError:
            raise ValidationError(
                "next_billing_date must be a valid ISO date (YYYY-MM-DD).", "VAL_007"
            )

        return cls(name=name, cost=cost, billing_cycle=billing_cycle,
                   next_billing_date=next_billing_date)