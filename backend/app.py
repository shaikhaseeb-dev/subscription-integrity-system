import logging
import os

from flask import Flask, jsonify
from flask_cors import CORS

from config import config_map
from extensions import db


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    CORS(app, resources={r"/*": {"origins": "*"}})

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    db.init_app(app)

    from routes.subscription_routes import subscriptions_bp
    from routes.billing_routes import billing_bp
    from routes.summary_routes import summary_bp

    app.register_blueprint(subscriptions_bp)
    app.register_blueprint(billing_bp)
    app.register_blueprint(summary_bp)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"error": "Endpoint not found.", "code": "HTTP_404"}), 404

    @app.errorhandler(405)
    def method_not_allowed(_):
        return jsonify({"error": "Method not allowed.", "code": "HTTP_405"}), 405

    @app.errorhandler(500)
    def internal_error(exc):
        logging.getLogger(__name__).exception("Unhandled exception: %s", exc)
        return jsonify({"error": "Internal server error.", "code": "HTTP_500"}), 500

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    env = os.environ.get("FLASK_ENV", "default")
    application = create_app(env)
    application.run(host="0.0.0.0", port=5000, debug=(env != "default"))