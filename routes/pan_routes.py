from flask import Blueprint
from flask import request
from flask import jsonify

from services.ongrid.pan_verification_service import (
    OnGridPANVerificationService
)

from services.pan_result_service import (

    PANResultService

)

pan_bp = Blueprint(

    "pan",

    __name__
)


@pan_bp.route(

    "/pan/verify",

    methods=["POST"]
)
def verify_pan():

    try:

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "message": (
                    "Request body is required"
                )

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

            OnGridPANVerificationService
            .verify_pan(

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
        ), 200

    except Exception as error:

        print(
            "PAN VERIFICATION ERROR:",
            str(error)
        )

        return jsonify({

            "success": False,

            "message": str(
                error
            )

        }), 500
    
@pan_bp.route(


"/pan/result/<int:candidate_id>",


methods=["GET"]

)

def get_pan_result(

candidate_id

):


    try:


        result=(


            PANResultService


            .get_result(


                candidate_id

            )

        )


        return jsonify(

            result

        )


    except Exception as error:


        return jsonify({


            "success":False,


            "message":str(error)


        }),500