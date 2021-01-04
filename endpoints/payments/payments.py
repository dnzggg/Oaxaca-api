from flask import Flask, request, jsonify, Blueprint
from . import validate_data

bp = Blueprint("payments blueprint", __name__)


# endpoint to validate all the payment details
@bp.route("/verify_payment", methods=["POST"])
def verify_payment():
    error = validate_data.validate_payments(request)
    if error:
        return error

    return jsonify(data={"success": True})
