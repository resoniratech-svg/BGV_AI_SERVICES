from flask import Blueprint
from flask import request
from flask import jsonify

from services.credit_bureau_verification_service import CreditBureauVerificationService

from services.credit_bureau_result_service import CreditBureauResultService


credit_bureau_bp = Blueprint("credit_bureau_bp", __name__)


###############################################################
# VERIFY CREDIT BUREAU
###############################################################


@credit_bureau_bp.route("/credit-bureau/verify", methods=["POST"])
def verify_credit_bureau():

    print("=" * 80)
    print("AI SERVICE RECEIVED")
    print(request.get_json())
    print("=" * 80)

    try:
        data = request.get_json()

        if not data:
            return jsonify(
                {"success": False, "message": "Request body is required."}
            ), 400

        candidate_id = data.get("candidate_id")
        bgv_id = data.get("bgv_id")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        phone = data.get("phone")

        required_fields = {
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "first_name": first_name,
            "phone": phone,
        }

        for field, value in required_fields.items():
            if value is None or str(value).strip() == "":
                return jsonify(
                    {"success": False, "message": f"{field} is required."}
                ), 400

        result = CreditBureauVerificationService.verify_credit_bureau(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )

        return jsonify(result), 200

    except Exception as error:
        message = str(error)

        ####################################################
        # GRIDLINES RATE LIMIT
        ####################################################

        if "rate limit" in message.lower():
            return jsonify({"success": False, "message": message}), 429

        ####################################################
        # AUTHENTICATION
        ####################################################

        if "authentication" in message.lower():
            return jsonify({"success": False, "message": message}), 401

        ####################################################
        # FORBIDDEN
        ####################################################

        if "forbidden" in message.lower():
            return jsonify({"success": False, "message": message}), 403

        ####################################################
        # VALIDATION
        ####################################################

        if "required" in message.lower():
            return jsonify({"success": False, "message": message}), 400

        ####################################################
        # DEFAULT
        ####################################################

        return jsonify({"success": False, "message": message}), 500


###############################################################
# GET CREDIT BUREAU RESULT
###############################################################


@credit_bureau_bp.route("/credit-bureau/result/<int:candidate_id>", methods=["GET"])
def get_credit_bureau_result(candidate_id):

    try:
        result = CreditBureauResultService.get_result(candidate_id)

        if not result:
            return jsonify(
                {"success": False, "message": "Credit Bureau result not found."}
            ), 404

        return jsonify({"success": True, "data": result}), 200

    except Exception as error:
        return jsonify({"success": False, "message": str(error)}), 500
