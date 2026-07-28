from flask import Blueprint
from flask import request
from flask import jsonify

from services.ongrid.passport_verification_service import (
    PassportVerificationService
)

from services.passport_result_service import (
    PassportResultService
)
from services.ocr.passport_ocr_service import PassportOCRService

passport_bp = Blueprint(
    "passport",
    __name__
)


# ======================================================
# VERIFY PASSPORT
# ======================================================

@passport_bp.route(
    "/passport/verify",
    methods=["POST"]
)
def verify_passport():

    try:

        data = request.get_json()

        if not data:

            return jsonify({

                "status": "error",

                "message": "Request body is required"

            }), 400


        candidate_id = data.get("candidate_id")
        bgv_id = data.get("bgv_id")
        document_id = data.get("document_id")


        if not candidate_id:

            return jsonify({

                "status": "error",

                "message": "candidate_id is required"

            }), 400


        if not bgv_id:

            return jsonify({

                "status": "error",

                "message": "bgv_id is required"

            }), 400


        if not document_id:

            return jsonify({

                "status": "error",

                "message": "document_id is required"

            }), 400


        result = (

            PassportVerificationService

            .verify_passport(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                document_id=document_id

            )

        )


        return jsonify({

            "status": "success",

            "message": "Passport verification completed",

            "data": result

        })


    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


# ======================================================
# GET PASSPORT RESULT
# ======================================================


@passport_bp.route(
    "/passport/result/<int:candidate_id>",
    methods=["GET"]
)
def get_passport_result(candidate_id):

    try:

        result = (
            PassportResultService
            .get_result(
                candidate_id
            )
        )

        return jsonify({

            "status": "success",

            "data": result

        }), 200

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500
    
    
@passport_bp.route(
    "/passport/ocr",
    methods=["POST"]
)
def passport_ocr():

    data = request.get_json()

    result = PassportOCRService.extract_passport_data(
        candidate_id=data["candidate_id"],
        bgv_id=data["bgv_id"],
        document_id=data["document_id"]
    )

    return jsonify(result)