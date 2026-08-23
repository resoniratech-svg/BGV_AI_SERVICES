from flask import Blueprint
from flask import request
from flask import jsonify

from services.ccrv_verification_service import CCRVVerificationService

from services.ccrv_result_service import CCRVResultService

ccrv_bp = Blueprint("ccrv", __name__)


# ==========================================================
# VERIFY CCRV
# ==========================================================


@ccrv_bp.route("/ccrv/verify", methods=["POST"])
def verify_ccrv():

    try:
        data = request.get_json()

        result = CCRVVerificationService.verify_ccrv(
            candidate_id=data["candidate_id"], bgv_id=data["bgv_id"]
        )

        return jsonify(
            {
                "status": "success",
                "message": "CCRV request submitted successfully",
                "data": result,
            }
        ), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ==========================================================
# GET CCRV RESULT
# ==========================================================


@ccrv_bp.route("/ccrv/result/<int:candidate_id>", methods=["GET"])
def get_ccrv_result(candidate_id):

    try:
        result = CCRVResultService.get_result(candidate_id)

        return jsonify({"status": "success", "data": result}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
