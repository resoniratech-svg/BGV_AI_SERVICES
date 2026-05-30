from flask import Blueprint
from flask import request
from flask import jsonify

from services.court_record_service import (
    CourtRecordService
)

indiankanoon_bp = Blueprint(

    "indiankanoon_bp",

    __name__
)


@indiankanoon_bp.route(

    "/court-record/search",

    methods=["POST"]
)
def search_court_records():

    try:

        data = request.get_json()

        candidate_id = data.get(
            "candidate_id"
        )

        full_name = data.get(
            "full_name"
        )

        if not candidate_id:

            return jsonify({

                "success": False,

                "message": (
                    "candidate_id missing"
                )
            }), 400

        if not full_name:

            return jsonify({

                "success": False,

                "message": (
                    "full_name missing"
                )
            }), 400

        result = (
            CourtRecordService
            .search_court_records(

                candidate_id=candidate_id,

                full_name=full_name
            )
        )

        return jsonify(result)

    except Exception as e:

        return jsonify({

            "success": False,

            "message": (
                "Court verification failed"
            ),

            "error": str(e)
        }), 500