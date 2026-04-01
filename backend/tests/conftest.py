import pytest
from datetime import date

from app import create_app
from extensions import db as _db
from utils import date_utils


@pytest.fixture(scope="function")
def app():
    application = create_app("testing")
    with application.app_context():
        _db.create_all()
        yield application
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def reset_mock_date():
    yield
    date_utils.set_mock_date(None)


def make_subscription(
    client,
    name="Netflix",
    cost=15.99,
    billing_cycle="monthly",
    next_billing_date=None,
):
    if next_billing_date is None:
        next_billing_date = date.today().isoformat()
    return client.post(
        "/subscriptions",
        json={
            "name": name,
            "cost": cost,
            "billing_cycle": billing_cycle,
            "next_billing_date": next_billing_date,
        },
    )