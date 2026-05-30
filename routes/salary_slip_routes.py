from flask import Blueprint
from flask import request
from flask import jsonify

import os
import uuid

from werkzeug.utils import secure_filename

from config import Config

from services.salary_slip_service import (
    SalarySlipService
)

salary_slip_bp = Blueprint(

    "salary_slip_bp",

    __name__
)


@salary_slip_bp.route(

    "/salary-slip/verify",

    methods=["POST"]
)
def verify_salary_slip():

    try:

        # ==========================================
        # VALIDATE FILE
        # ==========================================

        if "file" not in request.files:

            return jsonify({

                "success": False,

                "message": (
                    "Salary slip file missing"
                )
            }), 400

        salary_slip_file = request.files[
            "file"
        ]

        if salary_slip_file.filename == "":

            return jsonify({

                "success": False,

                "message": (
                    "Invalid salary slip file"
                )
            }), 400

        # ==========================================
        # VALIDATE CANDIDATE ID
        # ==========================================

        candidate_id = request.form.get(
            "candidate_id"
        )

        if not candidate_id:

            return jsonify({

                "success": False,

                "message": (
                    "candidate_id missing"
                )
            }), 400

        # ==========================================
        # SECURE FILE NAME
        # ==========================================

        original_filename = secure_filename(

            salary_slip_file.filename
        )

        file_extension = os.path.splitext(

            original_filename
        )[1]

        unique_filename = (

            f"{uuid.uuid4()}"
            f"{file_extension}"
        )

        # ==========================================
        # CREATE UPLOAD DIRECTORY
        # ==========================================

        os.makedirs(

            Config.UPLOAD_FOLDER,

            exist_ok=True
        )

        file_path = os.path.join(

            Config.UPLOAD_FOLDER,

            unique_filename
        )

        # ==========================================
        # SAVE FILE
        # ==========================================

        salary_slip_file.save(

            file_path
        )

        # ==========================================
        # VERIFY SALARY SLIP
        # ==========================================

        result = (
            SalarySlipService
            .verify_salary_slip(

                file_path=file_path,

                candidate_id=candidate_id
            )
        )

        # ==========================================
        # API FAILURE
        # ==========================================

        if not result.get("success"):

            return jsonify({

                "success": False,

                "message": result.get(
                    "message"
                ),

                "error": result.get(
                    "error"
                )
            }), 400

        # ==========================================
        # SUCCESS RESPONSE
        # ==========================================

        return jsonify({

            "success": True,

            "message": (
                "Salary slip verified successfully"
            ),

            "data": result
        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": (
                "Salary slip verification failed"
            ),

            "error": str(e)
        }), 500