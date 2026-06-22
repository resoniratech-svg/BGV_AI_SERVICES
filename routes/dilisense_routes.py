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

        candidate_id = data.get(
            "candidate_id"
        )

        full_name = data.get(
            "full_name"
        )

        dob = data.get("dob")
        gender = data.get("gender")

        if not candidate_id:

            return jsonify({

                "success": False,

                "message": "candidate_id required"
            }), 400

        if not full_name:

            return jsonify({

                "success": False,

                "message": "full_name required"
            }), 400

        # Fixed: Updated call to match AMLService.screen_watchlist
        from datetime import datetime

        if dob and "-" in dob:
            dob = datetime.strptime(
                dob,
                "%Y-%m-%d"
            ).strftime("%d/%m/%Y")
        result = AMLService.screen_watchlist(
            candidate_id=candidate_id,
            full_name=full_name,
            dob=dob,
            gender=gender
        )

        return jsonify(result)

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)
        }), 500