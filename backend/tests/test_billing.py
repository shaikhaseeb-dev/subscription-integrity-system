from datetime import date, timedelta
from tests.conftest import make_subscription
from utils import date_utils


class TestBillingEngine:

    def test_billing_processes_due_subscription(self, client):
        make_subscription(client)
        resp = client.post("/billing/run")
        data = resp.get_json()
        assert data["processed_count"] == 1
        assert data["skipped_count"] == 0

    def test_billing_skips_future_subscription(self, client):
        future = (date.today() + timedelta(days=10)).isoformat()
        make_subscription(client, next_billing_date=future)
        data = client.post("/billing/run").get_json()
        assert data["processed_count"] == 0
        assert data["skipped_count"] == 1

    def test_billing_creates_billing_event(self, client):
        make_subscription(client)
        client.post("/billing/run")
        events = client.get("/billing/events").get_json()
        assert len(events) == 1
        assert events[0]["amount"] == 15.99

    def test_no_event_when_nothing_due(self, client):
        future = (date.today() + timedelta(days=10)).isoformat()
        make_subscription(client, next_billing_date=future)
        client.post("/billing/run")
        assert client.get("/billing/events").get_json() == []

    def test_monthly_advances_30_days(self, client):
        today = date.today()
        make_subscription(client, billing_cycle="monthly", next_billing_date=today.isoformat())
        client.post("/billing/run")
        subs = client.get("/subscriptions").get_json()
        assert subs[0]["next_billing_date"] == (today + timedelta(days=30)).isoformat()

    def test_yearly_advances_365_days(self, client):
        today = date.today()
        make_subscription(client, billing_cycle="yearly", next_billing_date=today.isoformat(), cost=120.00)
        client.post("/billing/run")
        subs = client.get("/subscriptions").get_json()
        assert subs[0]["next_billing_date"] == (today + timedelta(days=365)).isoformat()

    def test_billing_idempotent_within_cycle(self, client):
        make_subscription(client)
        client.post("/billing/run")
        client.post("/billing/run")
        events = client.get("/billing/events").get_json()
        assert len(events) == 1

    def test_two_runs_on_different_dates(self, client):
        today = date.today()
        date_utils.set_mock_date(today)
        make_subscription(client, next_billing_date=today.isoformat())
        client.post("/billing/run")
        date_utils.set_mock_date(today + timedelta(days=31))
        client.post("/billing/run")
        events = client.get("/billing/events").get_json()
        assert len(events) == 2

    def test_empty_billing_run(self, client):
        data = client.post("/billing/run").get_json()
        assert data["processed_count"] == 0
        assert data["skipped_count"] == 0

    def test_billing_event_records_correct_next_date(self, client):
        today = date.today()
        make_subscription(client, billing_cycle="monthly", next_billing_date=today.isoformat())
        client.post("/billing/run")
        events = client.get("/billing/events").get_json()
        assert events[0]["next_billing_date_after"] == (today + timedelta(days=30)).isoformat()