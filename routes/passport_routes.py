from flask import Blueprint
from flask import request
from flask import jsonify

from services.passport_verification_service import (
    PassportVerificationService
)

passport_bp = Blueprint(

    "passport_bp",
    __name__
)


@passport_bp.route(

    "/passport/verify",

    methods=["POST"]
)
def verify_passport():

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

        if not document_id:

            return jsonify({

                "success": False,

                "message": (
                    "document_id is required"
                )
            }), 400

        # ======================================
        # VERIFY PASSPORT
        # ======================================

        result = (

            PassportVerificationService
            .verify_passport(

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