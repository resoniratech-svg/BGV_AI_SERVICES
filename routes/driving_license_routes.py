# from flask import Blueprint
# from flask import request
# from flask import jsonify

# from services.driving_license_verification_service import (
#     DrivingLicenseVerificationService,
# )

# from services.driving_license_result_service import DrivingLicenseResultService


# driving_license_bp = Blueprint("driving_license_bp", __name__)


# # =====================================================
# # VERIFY DRIVING LICENSE
# # =====================================================


# @driving_license_bp.route("/driving-license/verify", methods=["POST"])
# def verify_driving_license():

#     try:
#         data = request.get_json()

#         candidate_id = data.get("candidate_id")

#         bgv_id = data.get("bgv_id")

#         front_document_id = data.get("front_document_id")

#         back_document_id = data.get("back_document_id")

#         ###################################################
#         # VALIDATIONS
#         ###################################################

#         if not candidate_id:
#             return jsonify(
#                 {"success": False, "message": "candidate_id is required"}
#             ), 400

#         if not bgv_id:
#             return jsonify({"success": False, "message": "bgv_id is required"}), 400

#         if not front_document_id:
#             return jsonify(
#                 {"success": False, "message": "front_document_id is required"}
#             ), 400

#         if not back_document_id:
#             return jsonify(
#                 {"success": False, "message": "back_document_id is required"}
#             ), 400

#         ###################################################
#         # VERIFY
#         ###################################################

#         result = DrivingLicenseVerificationService.verify_driving_license(
#             candidate_id=candidate_id,
#             bgv_id=bgv_id,
#             front_document_id=front_document_id,
#             back_document_id=back_document_id,
#         )

#         return jsonify(
#             {
#                 "success": True,
#                 "message": "Driving License verification completed successfully",
#                 "data": result,
#             }
#         ), 200

#     except Exception as e:
#         return jsonify({"success": False, "message": str(e)}), 500


# # =====================================================
# # GET RESULT
# # =====================================================


# @driving_license_bp.route("/driving-license/result/<int:candidate_id>", methods=["GET"])
# def get_driving_license_result(candidate_id):

#     try:
#         result = DrivingLicenseResultService.get_result(candidate_id)

#         return jsonify({"success": True, "data": result}), 200

#     except Exception as e:
#         return jsonify({"success": False, "message": str(e)}), 500


from flask import Blueprint
from flask import request
from flask import jsonify

from services.driving_license_verification_service import (
    DrivingLicenseVerificationService,
)

from services.driving_license_result_service import (
    DrivingLicenseResultService,
)


driving_license_bp = Blueprint(
    "driving_license_bp",
    __name__,
)


# =====================================================
# VERIFY DRIVING LICENSE
# =====================================================


@driving_license_bp.route(
    "/driving-license/verify",
    methods=["POST"],
)
def verify_driving_license():

    try:
        data = request.get_json()

        if not data:
            return jsonify(
                {
                    "success": False,
                    "message": "Request body is required",
                }
            ), 400

        # =================================================
        # REQUEST DATA
        # =================================================

        candidate_id = data.get("candidate_id")

        bgv_id = data.get("bgv_id")

        front_document_id = data.get("front_document_id")

        back_document_id = data.get("back_document_id")

        print("=" * 80)
        print("DRIVING LICENSE VERIFY REQUEST")
        print("=" * 80)

        print(
            "candidate_id       :",
            candidate_id,
        )

        print(
            "bgv_id             :",
            bgv_id,
        )

        print(
            "front_document_id :",
            front_document_id,
        )

        print(
            "back_document_id  :",
            back_document_id,
        )

        print("=" * 80)

        # =================================================
        # VALIDATE CANDIDATE ID
        # =================================================

        if not candidate_id:
            return jsonify(
                {
                    "success": False,
                    "message": "candidate_id is required",
                }
            ), 400

        # =================================================
        # VALIDATE BGV ID
        # =================================================

        if not bgv_id:
            return jsonify(
                {
                    "success": False,
                    "message": "bgv_id is required",
                }
            ), 400

        # =================================================
        # VALIDATE FRONT DOCUMENT
        # =================================================

        if not front_document_id:
            return jsonify(
                {
                    "success": False,
                    "message": "front_document_id is required",
                }
            ), 400

        # =================================================
        # VALIDATE BACK DOCUMENT
        # =================================================

        if not back_document_id:
            return jsonify(
                {
                    "success": False,
                    "message": "back_document_id is required",
                }
            ), 400

        # =================================================
        # VERIFY DRIVING LICENSE
        # =================================================

        result = DrivingLicenseVerificationService.verify_driving_license(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            front_document_id=front_document_id,
            back_document_id=back_document_id,
        )

        # =================================================
        # SUCCESS RESPONSE
        # =================================================

        return jsonify(
            {
                "success": True,
                "message": ("Driving License verification completed successfully"),
                "data": result,
            }
        ), 200

    except Exception as e:
        print("=" * 80)
        print("DRIVING LICENSE VERIFY ERROR")
        print(str(e))
        print("=" * 80)

        return jsonify(
            {
                "success": False,
                "message": str(e),
            }
        ), 500


# =====================================================
# GET DRIVING LICENSE RESULT
# =====================================================


@driving_license_bp.route(
    "/driving-license/result/<int:candidate_id>",
    methods=["GET"],
)
def get_driving_license_result(
    candidate_id,
):

    try:
        print("=" * 80)
        print("GET DRIVING LICENSE RESULT")
        print(
            "CANDIDATE ID:",
            candidate_id,
        )
        print("=" * 80)

        # =================================================
        # GET RESULT
        # =================================================

        result = DrivingLicenseResultService.get_result(candidate_id)

        # =================================================
        # RESULT NOT FOUND
        # =================================================

        if not result:
            return jsonify(
                {
                    "success": False,
                    "message": ("Driving License verification result not found"),
                    "data": None,
                }
            ), 404

        # =================================================
        # SUCCESS RESPONSE
        # =================================================

        return jsonify(
            {
                "success": True,
                "data": result,
            }
        ), 200

    except Exception as e:
        print("=" * 80)
        print("DRIVING LICENSE RESULT ERROR")
        print(str(e))
        print("=" * 80)

        return jsonify(
            {
                "success": False,
                "message": str(e),
            }
        ), 500
