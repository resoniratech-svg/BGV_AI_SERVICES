from flask import Blueprint
from flask import request
from flask import jsonify

from services.driving_license_verification_service import (
    DrivingLicenseVerificationService
)

from services.driving_license_result_service import (
    DrivingLicenseResultService
)


driving_license_bp = Blueprint(

    "driving_license_bp",

    __name__

)


# =====================================================
# VERIFY DRIVING LICENSE
# =====================================================

@driving_license_bp.route(

    "/driving-license/verify",

    methods=["POST"]

)
def verify_driving_license():

    try:

        data = request.get_json()

        candidate_id = data.get(
            "candidate_id"
        )

        bgv_id = data.get(
            "bgv_id"
        )

        front_document_id = data.get(
            "front_document_id"
        )

        back_document_id = data.get(
            "back_document_id"
        )

        ###################################################
        # VALIDATIONS
        ###################################################

        if not candidate_id:

            return jsonify({

                "success": False,

                "message": "candidate_id is required"

            }), 400

        if not bgv_id:

            return jsonify({

                "success": False,

                "message": "bgv_id is required"

            }), 400

        if not front_document_id:

            return jsonify({

                "success": False,

                "message": "front_document_id is required"

            }), 400

        if not back_document_id:

            return jsonify({

                "success": False,

                "message": "back_document_id is required"

            }), 400

        ###################################################
        # VERIFY
        ###################################################

        result = (

            DrivingLicenseVerificationService

            .verify_driving_license(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                front_document_id=front_document_id,

                back_document_id=back_document_id

            )

        )

        return jsonify({

            "success": True,

            "message": "Driving License verification completed successfully",

            "data": result

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500


# =====================================================
# GET RESULT
# =====================================================

@driving_license_bp.route(

    "/driving-license/result/<int:candidate_id>",

    methods=["GET"]

)
def get_driving_license_result(

        candidate_id

):

    try:

        result = (

            DrivingLicenseResultService

            .get_result(

                candidate_id

            )

        )

        return jsonify({

            "success": True,

            "data": result

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500