from flask import Blueprint
from flask import request
from flask import jsonify

import os
import uuid

from werkzeug.utils import secure_filename

from config import Config

from services.rchilli_service import (
    RChilliService
)

rchilli_bp = Blueprint(
    "rchilli_bp",
    __name__
)


@rchilli_bp.route(
    "/resume/parse",
    methods=["POST"]
)
def parse_resume():

    try:

        # ==========================================
        # VALIDATE FILE
        # ==========================================

        if "resume" not in request.files:

            return jsonify({

                "success": False,

                "message": "Resume file missing"
            }), 400

        resume_file = request.files["resume"]

        if resume_file.filename == "":

            return jsonify({

                "success": False,

                "message": "Invalid resume file"
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

                "message": "candidate_id missing"
            }), 400

        # ==========================================
        # SECURE FILE NAME
        # ==========================================

        original_filename = secure_filename(
            resume_file.filename
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

        resume_file.save(file_path)

        # ==========================================
        # PARSE RESUME
        # ==========================================

        result = (
            RChilliService.parse_resume(

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
                ),

                "provider_response": result.get(
                    "provider_response"
                )
            }), 400

        # ==========================================
        # SUCCESS RESPONSE
        # ==========================================

        return jsonify({

            "success": True,

            "message": "Resume parsed successfully",

            "data": result
        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": "Resume parsing failed",

            "error": str(e)
        }), 500