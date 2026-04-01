from datetime import date, timedelta

_mock_date: date | None = None


def set_mock_date(mock_date: date | None) -> None:
    global _mock_date
    _mock_date = mock_date


def get_current_date(mock_date: date | None = None) -> date:
    if mock_date is not None:
        return mock_date
    if _mock_date is not None:
        return _mock_date
    return date.today()


def advance_billing_date(current: date, billing_cycle: str) -> date:
    if billing_cycle == "monthly":
        return current + timedelta(days=30)
    elif billing_cycle == "yearly":
        return current + timedelta(days=365)
    raise ValueError(f"Unknown billing_cycle: {billing_cycle!r}")


def days_until(target: date, today: date | None = None) -> int:
    today = today or get_current_date()
    return (target - today).days