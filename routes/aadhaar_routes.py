from flask import Blueprint

from flask import request

from flask import jsonify

from services.ongrid.aadhaar_generate_qr_service import (
    AadhaarGenerateQRService
)

from services.ongrid.aadhaar_status_service import (
    AadhaarStatusService
)

from services.ongrid.aadhaar_verification_service import (
    AadhaarVerificationService
)
from services.ongrid.aadhaar_consent_service import (

AadhaarConsentService

)

from services.aadhaar_result_service import (
    AadhaarResultService
)

aadhaar_bp = Blueprint(

    "aadhaar",

    __name__
)


# ==========================================
# GENERATE QR
# ==========================================

@aadhaar_bp.route(

    "/aadhaar/generate-qr",

    methods=["POST"]

)
def generate_qr():

    try:

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "message":
                "Request body is required"

            }), 400

        candidate_id = data.get(
            "candidate_id"
        )

        bgv_id = data.get(
            "bgv_id"
        )

        if not candidate_id:

            return jsonify({

                "success": False,

                "message":
                "candidate_id is required"

            }), 400

        if not bgv_id:

            return jsonify({

                "success": False,

                "message":
                "bgv_id is required"

            }), 400

        result = (

            AadhaarGenerateQRService
            .generate_qr(

                candidate_id=
                candidate_id,

                bgv_id=
                bgv_id

            )

        )

        return jsonify(
            result
        )

    except Exception as error:

        return jsonify({

            "success": False,

            "message":
            str(error)

        }), 500


# ==========================================
# FETCH STATUS
# ==========================================

@aadhaar_bp.route(

    "/aadhaar/status/<int:candidate_id>",

    methods=["GET"]

)
def fetch_status(

    candidate_id

):

    try:

        result = (

            AadhaarStatusService
            .fetch_status(

                candidate_id

            )

        )

        return jsonify(
            result
        )

    except Exception as error:

        return jsonify({

            "success": False,

            "message":
            str(error)

        }), 500


# ==========================================
# VERIFY AADHAAR
# ==========================================

@aadhaar_bp.route(

    "/aadhaar/verify",

    methods=["POST"]

)
def verify_aadhaar():

    try:

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "message":
                "Request body is required"

            }), 400

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

                "message":
                "candidate_id is required"

            }), 400

        if not bgv_id:

            return jsonify({

                "success": False,

                "message":
                "bgv_id is required"

            }), 400

        if not document_id:

            return jsonify({

                "success": False,

                "message":
                "document_id is required"

            }), 400

        result = (

            AadhaarVerificationService
            .verify_aadhaar(

                candidate_id=
                candidate_id,

                bgv_id=
                bgv_id,

                document_id=
                document_id

            )

        )

        return jsonify(
            result
        )

    except Exception as error:

        return jsonify({

            "success": False,

            "message":
            str(error)

        }), 500
    
    
# ==========================================
# CONSENT LINK
# ==========================================

@aadhaar_bp.route(

    "/aadhaar/consent",

    methods=["POST"]

)
def aadhaar_consent():

    try:

        data = request.get_json()


        if not data:

            return jsonify({

                "success": False,

                "message":

                "Request body is required"

            }), 400


        candidate_id = (

            data.get(

                "candidate_id"

            )

        )


        bgv_id = (

            data.get(

                "bgv_id"

            )

        )


        if not candidate_id:

            return jsonify({

                "success": False,

                "message":

                "candidate_id is required"

            }), 400


        if not bgv_id:

            return jsonify({

                "success": False,

                "message":

                "bgv_id is required"

            }), 400


        result = (

            AadhaarConsentService
            .get_consent_qr(

                candidate_id,

                bgv_id

            )

        )


        return jsonify(

            result

        )


    except Exception as error:


        return jsonify({

            "success": False,

            "message":

            str(error)

        }), 500
    
    # ==========================================
# GET RESULT
# ==========================================

@aadhaar_bp.route(

    "/aadhaar/result/<int:candidate_id>",

    methods=["GET"]

)

def get_result(

    candidate_id

):


    try:


        result = (

            AadhaarResultService
            .get_result(

                candidate_id

            )

        )


        return jsonify(

            result

        )


    except Exception as error:


        return jsonify({


            "success": False,


            "message":

            str(error)

        }), 500

