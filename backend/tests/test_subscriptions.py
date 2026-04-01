import pytest
from datetime import date, timedelta
from tests.conftest import make_subscription


class TestCreateSubscriptionValidation:

    def test_create_valid_monthly(self, client):
        resp = make_subscription(client)
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["name"] == "Netflix"
        assert data["status"] == "active"

    def test_create_valid_yearly(self, client):
        future = (date.today() + timedelta(days=10)).isoformat()
        resp = make_subscription(client, billing_cycle="yearly", next_billing_date=future)
        assert resp.status_code == 201

    def test_duplicate_active_rejected(self, client):
        make_subscription(client, name="Spotify")
        resp = make_subscription(client, name="Spotify")
        assert resp.status_code == 422
        assert resp.get_json()["code"] == "SUB_001"

    def test_duplicate_case_sensitive(self, client):
        make_subscription(client, name="spotify")
        resp = make_subscription(client, name="Spotify")
        assert resp.status_code == 201

    def test_zero_cost_rejected(self, client):
        resp = make_subscription(client, cost=0)
        assert resp.status_code == 422
        assert resp.get_json()["code"] == "VAL_004"

    def test_negative_cost_rejected(self, client):
        resp = make_subscription(client, cost=-5.00)
        assert resp.status_code == 422
        assert resp.get_json()["code"] == "VAL_004"

    def test_non_numeric_cost_rejected(self, client):
        resp = client.post("/subscriptions", json={
            "name": "X", "cost": "free",
            "billing_cycle": "monthly",
            "next_billing_date": date.today().isoformat(),
        })
        assert resp.status_code == 422

    def test_invalid_billing_cycle_rejected(self, client):
        resp = make_subscription(client, billing_cycle="weekly")
        assert resp.status_code == 422
        assert resp.get_json()["code"] == "VAL_005"

    def test_past_date_rejected(self, client):
        past = (date.today() - timedelta(days=1)).isoformat()
        resp = make_subscription(client, next_billing_date=past)
        assert resp.status_code == 422
        assert resp.get_json()["code"] == "SUB_002"

    def test_today_date_accepted(self, client):
        resp = make_subscription(client, next_billing_date=date.today().isoformat())
        assert resp.status_code == 201

    def test_future_date_accepted(self, client):
        future = (date.today() + timedelta(days=30)).isoformat()
        resp = make_subscription(client, next_billing_date=future)
        assert resp.status_code == 201

    def test_missing_name_rejected(self, client):
        resp = client.post("/subscriptions", json={
            "cost": 10, "billing_cycle": "monthly",
            "next_billing_date": date.today().isoformat(),
        })
        assert resp.status_code == 422

    def test_non_json_body_rejected(self, client):
        resp = client.post("/subscriptions", data="not json", content_type="text/plain")
        assert resp.status_code == 400