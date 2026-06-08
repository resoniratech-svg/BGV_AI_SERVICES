from flask import Blueprint
from flask import request
from flask import jsonify

from services.driving_license_verification_service import (
    DrivingLicenseVerificationService
)

driving_license_bp = Blueprint(

    "driving_license_bp",
    __name__
)


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

        # ======================================
        # VALIDATIONS
        # ======================================

        if not candidate_id:

            return jsonify({

                "success": False,

                "message": (
                    "candidate_id is required"
                )
            }), 400

        if not bgv_id:

            return jsonify({

                "success": False,

                "message": (
                    "bgv_id is required"
                )
            }), 400

        if not front_document_id:

            return jsonify({

                "success": False,

                "message": (
                    "front_document_id is required"
                )
            }), 400

        if not back_document_id:

            return jsonify({

                "success": False,

                "message": (
                    "back_document_id is required"
                )
            }), 400

        result = (

            DrivingLicenseVerificationService
            .verify_driving_license(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                front_document_id=front_document_id,

                back_document_id=back_document_id
            )
        )

        return jsonify(
            result
        ), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)
        }), 500