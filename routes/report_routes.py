from flask import Blueprint
from flask import jsonify
from flask import request

from services.report_service import (
    ReportService
)

report_bp = Blueprint(

    "report_bp",
    __name__
)


@report_bp.route(

    "/reports/generate",
    methods=["POST"]
)
def generate_bgv_report():

    try:

        # ==========================================
        # GET REQUEST DATA
        # ==========================================

        data = request.get_json()

        candidate_id = data.get(
            "candidate_id"
        )

        if not candidate_id:

            return jsonify({

                "status": "failed",

                "message": (
                    "candidate_id required"
                )
            }), 400

        # ==========================================
        # GENERATE PDF
        # ==========================================

        file_path = (
            ReportService
            .generate_bgv_report(
                candidate_id
            )
        )

        # ==========================================
        # SUCCESS RESPONSE
        # ==========================================

        return jsonify({

            "status": "success",

            "candidate_id": candidate_id,

            "file_path": file_path
        }), 200

    except Exception as e:

        return jsonify({

            "status": "failed",

            "error": str(e)
        }), 500