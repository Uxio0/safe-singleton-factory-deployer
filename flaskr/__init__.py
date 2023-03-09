import json

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from .services import deploy_contract


def create_app(test_config=None) -> Flask:
    app = Flask(__name__)

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps(
            {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        )
        response.content_type = "application/json"
        return response

    @app.route("/", methods=["POST"])
    def deploy():
        request_data = request.get_json()
        tx_hash = deploy_contract(request_data["rpc"])
        return jsonify(txHash=tx_hash.hex())

    return app
