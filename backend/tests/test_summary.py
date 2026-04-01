from datetime import date, timedelta
from tests.conftest import make_subscription


class TestMonthlySummary:

    def test_empty_summary(self, client):
        data = client.get("/summary/monthly-cost").get_json()
        assert data["total_monthly_cost"] == 0.0
        assert data["subscription_count"] == 0

    def test_monthly_full_cost(self, client):
        make_subscription(client, cost=15.99, billing_cycle="monthly")
        data = client.get("/summary/monthly-cost").get_json()
        assert data["total_monthly_cost"] == 15.99

    def test_yearly_normalised(self, client):
        future = (date.today() + timedelta(days=5)).isoformat()
        make_subscription(client, cost=120.00, billing_cycle="yearly", next_billing_date=future)
        data = client.get("/summary/monthly-cost").get_json()
        assert data["total_monthly_cost"] == 10.00

    def test_mixed_total(self, client):
        today = date.today().isoformat()
        future = (date.today() + timedelta(days=5)).isoformat()
        make_subscription(client, name="Netflix", cost=15.99, billing_cycle="monthly", next_billing_date=today)
        make_subscription(client, name="AWS", cost=120.00, billing_cycle="yearly", next_billing_date=future)
        data = client.get("/summary/monthly-cost").get_json()
        assert data["total_monthly_cost"] == 25.99
        assert data["subscription_count"] == 2

    def test_breakdown_has_monthly_equivalent(self, client):
        future = (date.today() + timedelta(days=5)).isoformat()
        make_subscription(client, name="Adobe", cost=600.00, billing_cycle="yearly", next_billing_date=future)
        data = client.get("/summary/monthly-cost").get_json()
        assert data["breakdown"][0]["monthly_equivalent"] == 50.00


class TestUpcomingBilling:

    def test_empty(self, client):
        assert client.get("/subscriptions/upcoming").get_json() == []

    def test_due_today_is_upcoming(self, client):
        make_subscription(client)
        data = client.get("/subscriptions/upcoming").get_json()
        assert len(data) == 1

    def test_due_in_7_days_is_upcoming(self, client):
        in_7 = (date.today() + timedelta(days=7)).isoformat()
        make_subscription(client, next_billing_date=in_7)
        assert len(client.get("/subscriptions/upcoming").get_json()) == 1

    def test_due_in_8_days_not_upcoming(self, client):
        in_8 = (date.today() + timedelta(days=8)).isoformat()
        make_subscription(client, next_billing_date=in_8)
        assert len(client.get("/subscriptions/upcoming").get_json()) == 0

    def test_upcoming_ordered_by_date(self, client):
        make_subscription(client, name="Late", next_billing_date=(date.today() + timedelta(days=5)).isoformat())
        make_subscription(client, name="Soon", next_billing_date=(date.today() + timedelta(days=2)).isoformat())
        data = client.get("/subscriptions/upcoming").get_json()
        assert data[0]["name"] == "Soon"
        assert data[1]["name"] == "Late"
