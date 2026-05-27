from flask import Blueprint
from flask import request
from flask import jsonify

from services.aml_service import (
    AMLService
)

dilisense_bp = Blueprint(

    "dilisense_bp",
    __name__
)


@dilisense_bp.route(

    "/watchlist/screen",

    methods=["POST"]
)
def screen_watchlist():

    try:

        data = request.get_json()

        result = AMLService.screen_candidate(

            candidate_id=data.get(
                "candidate_id"
            ),

            full_name=data.get(
                "full_name"
            ),

            country=data.get(
                "country"
            )
        )

        return jsonify(result)

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)
        }), 500
    
   
dilisense_bp = Blueprint(

    "dilisense_bp",

    __name__
)


@dilisense_bp.route(

    "/watchlist/screen",

    methods=["POST"]
)
def screen_watchlist():

    try:

        data = request.json

        full_name = data.get(
            "full_name"
        )

        dob = data.get(
            "dob"
        )

        gender = data.get(
            "gender"
        )

        if not full_name:

            return jsonify({

                "success": False,

                "message": (
                    "full_name required"
                )
            }), 400

        result = (
            AMLService.screen_individual(

                full_name=full_name,

                dob=dob,

                gender=gender
            )
        )

        return jsonify({

            "success": True,

            "data": result
        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": (
                "AML screening failed"
            ),

            "error": str(e)
        }), 500