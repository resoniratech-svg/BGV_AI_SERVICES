from flask import Blueprint
from flask import request
from flask import jsonify

import os
import uuid

from werkzeug.utils import secure_filename

from config import Config

from services.resume_verification_service import (
    ResumeVerificationService
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

        if not resume_file:

            return jsonify({

                "success": False,

                "message": "Resume file missing"
            }), 400

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
        # CONVERT CANDIDATE ID
        # ==========================================

        try:

            candidate_id = int(
                candidate_id
            )

        except Exception:

            return jsonify({

                "success": False,

                "message": "Invalid candidate_id"
            }), 400

        # ==========================================
        # SECURE FILE NAME
        # ==========================================

        original_filename = secure_filename(

            resume_file.filename
        )

        file_extension = os.path.splitext(

            original_filename
        )[1].lower()

        # ==========================================
        # ALLOWED FILE TYPES
        # ==========================================

        allowed_extensions = [

            ".pdf",
            ".doc",
            ".docx"
        ]

        if file_extension not in allowed_extensions:

            return jsonify({

                "success": False,

                "message": (
                    "Only PDF, DOC and DOCX files are allowed"
                )
            }), 400

        # ==========================================
        # GENERATE UNIQUE FILE NAME
        # ==========================================

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

        # ==========================================
        # FINAL FILE PATH
        # ==========================================

        file_path = os.path.join(

            Config.UPLOAD_FOLDER,

            unique_filename
        )

        # ==========================================
        # SAVE FILE
        # ==========================================

        resume_file.save(
            file_path
        )

        # ==========================================
        # PROCESS RESUME
        # ==========================================

        result = (
            ResumeVerificationService.process_resume(

                file=file_path,

                candidate_id=candidate_id
            )
        )

        # ==========================================
        # HANDLE FAILURE
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

            "message": (
                "Resume parsed successfully"
            ),

            "data": result
        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": (
                "Resume parsing failed"
            ),

            "error": str(e)
        }), 500