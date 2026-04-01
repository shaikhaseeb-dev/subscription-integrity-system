from flask import Blueprint, jsonify

from services.subscription_service import SubscriptionService

summary_bp = Blueprint("summary", __name__)


@summary_bp.route("/summary/monthly-cost", methods=["GET"])
def monthly_cost():
    return jsonify(SubscriptionService.monthly_cost_summary()), 200