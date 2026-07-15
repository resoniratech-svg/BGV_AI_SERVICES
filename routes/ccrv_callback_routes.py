from flask import Blueprint
from flask import request
from flask import jsonify

from services.ccrv_callback_service import (
    CCRVCallbackService
)


ccrv_callback_bp = Blueprint(

    "ccrv_callback_bp",

    __name__

)


###############################################################
# CCRV CALLBACK
###############################################################

@ccrv_callback_bp.route(

    "/ccrv/callback",

    methods=["POST"]

)
def ccrv_callback():

    try:

        payload = request.get_json()

        print("=" * 80)
        print("CCRV CALLBACK RECEIVED")
        print(payload)
        print("=" * 80)

        if not payload:

            return jsonify({

                "success": False,

                "message": "Callback payload is required."

            }), 400

        result = (

            CCRVCallbackService
            .process_callback(

                payload

            )

        )

        return jsonify(result), 200

    except Exception as error:

        print("=" * 80)
        print("CCRV CALLBACK ERROR")
        print(error)
        print("=" * 80)

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500