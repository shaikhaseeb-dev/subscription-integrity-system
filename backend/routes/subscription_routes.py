from flask import Blueprint, request, jsonify

from schemas.subscription_schema import ValidationError
from services.subscription_service import SubscriptionService

subscriptions_bp = Blueprint("subscriptions", __name__)


@subscriptions_bp.route("/subscriptions", methods=["POST"])
def create_subscription():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON.", "code": "REQ_001"}), 400
    try:
        subscription = SubscriptionService.create(data)
        return jsonify(subscription.to_dict()), 201
    except ValidationError as exc:
        return jsonify(exc.to_dict()), 422


@subscriptions_bp.route("/subscriptions", methods=["GET"])
def list_subscriptions():
    return jsonify([s.to_dict() for s in SubscriptionService.list_all()]), 200


@subscriptions_bp.route("/subscriptions/upcoming", methods=["GET"])
def upcoming_billing():
    return jsonify([s.to_dict() for s in SubscriptionService.get_upcoming()]), 200