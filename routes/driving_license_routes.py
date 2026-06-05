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

        document_id = data.get(
            "document_id"
        )

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

        if not document_id:

            return jsonify({

                "success": False,

                "message": (
                    "document_id is required"
                )
            }), 400

        result = (

            DrivingLicenseVerificationService
            .verify_driving_license(

                candidate_id=(
                    candidate_id
                ),

                bgv_id=(
                    bgv_id
                ),

                document_id=(
                    document_id
                )
            )
        )

        return jsonify(result), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)
        }), 500