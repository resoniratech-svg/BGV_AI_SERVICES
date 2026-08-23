from flask import Blueprint
from flask import request
from flask import jsonify

from services.ongrid.passport_verification_service import (
    PassportVerificationService,
)

from services.passport_result_service import PassportResultService
from services.ocr.passport_ocr_service import PassportOCRService


passport_bp = Blueprint("passport", __name__)


# ======================================================
# VERIFY PASSPORT
# ======================================================


@passport_bp.route("/passport/verify", methods=["POST"])
def verify_passport():

    try:
        data = request.get_json()

        if not data:
            return jsonify(
                {
                    "status": "error",
                    "message": "Request body is required",
                }
            ), 400

        candidate_id = data.get("candidate_id")
        bgv_id = data.get("bgv_id")

        # Passport now requires FRONT + BACK
        front_document_id = data.get("front_document_id")
        back_document_id = data.get("back_document_id")

        # --------------------------------------------------
        # Required fields
        # --------------------------------------------------

        if not candidate_id:
            return jsonify(
                {
                    "status": "error",
                    "message": "candidate_id is required",
                }
            ), 400

        if not bgv_id:
            return jsonify(
                {
                    "status": "error",
                    "message": "bgv_id is required",
                }
            ), 400

        if not front_document_id:
            return jsonify(
                {
                    "status": "error",
                    "message": "front_document_id is required",
                }
            ), 400

        if not back_document_id:
            return jsonify(
                {
                    "status": "error",
                    "message": "back_document_id is required",
                }
            ), 400

        # --------------------------------------------------
        # Passport Verification
        # --------------------------------------------------

        result = PassportVerificationService.verify_passport(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            front_document_id=front_document_id,
            back_document_id=back_document_id,
        )

        return jsonify(
            {
                "status": "success",
                "message": "Passport verification completed",
                "data": result,
            }
        ), 200

    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify(
            {
                "status": "error",
                "message": str(e),
            }
        ), 500


# ======================================================
# GET PASSPORT RESULT
# ======================================================


@passport_bp.route(
    "/passport/result/<int:candidate_id>",
    methods=["GET"],
)
def get_passport_result(candidate_id):

    try:
        result = PassportResultService.get_result(candidate_id)

        return jsonify(
            {
                "status": "success",
                "data": result,
            }
        ), 200

    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify(
            {
                "status": "error",
                "message": str(e),
            }
        ), 500


# ======================================================
# PASSPORT OCR
# ======================================================


@passport_bp.route("/passport/ocr", methods=["POST"])
def passport_ocr():

    try:
        data = request.get_json()

        if not data:
            return jsonify(
                {
                    "status": "error",
                    "message": "Request body is required",
                }
            ), 400

        candidate_id = data.get("candidate_id")
        bgv_id = data.get("bgv_id")

        # Passport OCR requires TWO documents
        front_document_id = data.get("front_document_id")
        back_document_id = data.get("back_document_id")

        # --------------------------------------------------
        # Required fields
        # --------------------------------------------------

        if not candidate_id:
            return jsonify(
                {
                    "status": "error",
                    "message": "candidate_id is required",
                }
            ), 400

        if not bgv_id:
            return jsonify(
                {
                    "status": "error",
                    "message": "bgv_id is required",
                }
            ), 400

        if not front_document_id:
            return jsonify(
                {
                    "status": "error",
                    "message": "front_document_id is required",
                }
            ), 400

        if not back_document_id:
            return jsonify(
                {
                    "status": "error",
                    "message": "back_document_id is required",
                }
            ), 400

        # --------------------------------------------------
        # Passport OCR
        # --------------------------------------------------

        result = PassportOCRService.extract_passport_data(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            front_document_id=front_document_id,
            back_document_id=back_document_id,
        )

        return jsonify(
            {
                "status": "success",
                "message": "Passport OCR completed",
                "data": result,
            }
        ), 200

    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify(
            {
                "status": "error",
                "message": str(e),
            }
        ), 500
