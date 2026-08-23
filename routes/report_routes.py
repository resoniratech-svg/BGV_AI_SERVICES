from flask import Blueprint
from flask import jsonify
from flask import request
from flask import send_file
import os
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


@report_bp.route(

    "/reports/history",
    methods=["GET"]
)
def get_report_history():

    try:

        reports = (
            ReportService
            .get_report_history()
        )

        return jsonify({

            "status": "success",

            "reports": reports
        }), 200

    except Exception as e:

        return jsonify({

            "status": "failed",

            "error": str(e)
        }), 500

@report_bp.route(
    "/reports/download/<int:candidate_id>",
    methods=["GET"]
)
def download_report(candidate_id):

    try:

        report = (
            ReportService
            .get_latest_report(
                candidate_id
            )
        )

        if not report:

            return jsonify({
                "status": "failed",
                "message": "Report not found"
            }), 404

        file_path = report["file_path"]

        if not os.path.exists(file_path):

            return jsonify({
                "status": "failed",
                "message": "PDF file missing"
            }), 404

        return send_file(
            file_path,
            as_attachment=True
        )

    except Exception as e:

        return jsonify({
            "status": "failed",
            "error": str(e)
        }), 500