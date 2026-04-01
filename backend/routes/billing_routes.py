from flask import Blueprint, jsonify

from services.billing_service import BillingService

billing_bp = Blueprint("billing", __name__)


@billing_bp.route("/billing/run", methods=["POST"])
def run_billing():
    return jsonify(BillingService.run_billing()), 200


@billing_bp.route("/billing/events", methods=["GET"])
def billing_events():
    return jsonify([e.to_dict() for e in BillingService.get_billing_events()]), 200