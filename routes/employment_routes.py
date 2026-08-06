from flask import Blueprint
from flask import request
from flask import jsonify

from services.employment_verification_service import (
    EmploymentVerificationService
)

from services.employment_result_service import (
    EmploymentResultService
)

employment_bp = Blueprint(

    "employment",

    __name__

)

###############################################################
# VERIFY EMPLOYMENT
###############################################################

@employment_bp.route(

    "/employment/verify",

    methods=["POST"]

)
def verify_employment():

    try:

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "message": "Request body is required."

            }), 400

        result = (

            EmploymentVerificationService
            .verify_employment(

                candidate_id=data.get(

                    "candidate_id"

                ),

                bgv_id=data.get(

                    "bgv_id"

                ),

                mobile_number=data.get(

                    "mobile_number"

                )

            )

        )

        return jsonify({

            "success": True,

            "message": "Employment verification completed successfully.",

            "data": result

        }), 200

    except Exception as error:

        print("=" * 80)
        print("EMPLOYMENT VERIFICATION ERROR")
        print(error)
        print("=" * 80)

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500


###############################################################
# GET EMPLOYMENT RESULT
###############################################################

@employment_bp.route(

    "/employment/result/<int:candidate_id>",

    methods=["GET"]

)
def get_employment_result(

        candidate_id

):

    try:

        result = (

            EmploymentResultService
            .get_result(

                candidate_id

            )

        )

        return jsonify({

            "success": True,

            "data": result

        }), 200

    except Exception as error:

        print("=" * 80)
        print("EMPLOYMENT RESULT ERROR")
        print(error)
        print("=" * 80)

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500