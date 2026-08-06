from flask import Blueprint
from flask import request
from flask import jsonify

from services.consent_service import (
    ConsentService
)

consent_bp = Blueprint(

    "consent_bp",

    __name__

)


############################################################
# SAVE / UPDATE CANDIDATE CONSENT
############################################################

@consent_bp.route(

    "/candidate-consent",

    methods=["POST"]

)
def save_candidate_consent():

    try:

        data = request.get_json()

        candidate_id = data.get(
            "candidate_id"
        )

        bgv_id = data.get(
            "bgv_id"
        )

        verification_type = data.get(
            "verification_type"
        )

        consent_status = data.get(
            "consent_status"
        )

        consent_text = data.get(
            "consent_text"
        )

        consent_version = data.get(
            "consent_version"
        )

        consent_source = data.get(
            "consent_source",
            "PORTAL"
        )

        ip_address = request.remote_addr

        user_agent = request.headers.get(
            "User-Agent"
        )

        ####################################################
        # VALIDATIONS
        ####################################################

        if not candidate_id:

            return jsonify({

                "success": False,

                "message": "candidate_id is required."

            }), 400

        if not bgv_id:

            return jsonify({

                "success": False,

                "message": "bgv_id is required."

            }), 400

        if not verification_type:

            return jsonify({

                "success": False,

                "message": "verification_type is required."

            }), 400

        if not consent_status:

            return jsonify({

                "success": False,

                "message": "consent_status is required."

            }), 400

        if not consent_text:

            return jsonify({

                "success": False,

                "message": "consent_text is required."

            }), 400

        ####################################################
        # SAVE CONSENT
        ####################################################

        result = (

            ConsentService
            .save_candidate_consent(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                verification_type=verification_type,

                consent_status=consent_status,

                consent_text=consent_text,

                consent_version=consent_version,

                consent_source=consent_source,

                ip_address=ip_address,

                user_agent=user_agent

            )

        )

        return jsonify(result), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500


############################################################
# GET CANDIDATE CONSENT
############################################################

@consent_bp.route(

    "/candidate-consent/<int:candidate_id>",

    methods=["GET"]

)
def get_candidate_consent(candidate_id):

    try:

        verification_type = request.args.get(

            "verification_type"

        )

        bgv_id = request.args.get(

            "bgv_id"

        )

        if not verification_type:

            return jsonify({

                "success": False,

                "message": "verification_type is required."

            }), 400

        result = (

            ConsentService
            .get_candidate_consent(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                verification_type=verification_type

            )

        )

        if not result:

            return jsonify({

                "success": False,

                "message": "Consent not found."

            }), 404

        return jsonify({

            "success": True,

            "data": result

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500