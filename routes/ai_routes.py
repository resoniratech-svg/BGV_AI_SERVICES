from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required
# from services.aadhaar_pan_service import process_aadhaar_verification, process_aadhaar_verification
# from services.aadhaar_pan_service import process_pan_verification
from services.ocr_service import extract_text_from_image
from services.docx_service import extract_docx_text
from services.pdf_service import extract_pdf_text
from utils.auth import role_required
import os
from services.ocr_verification_service import verify_pan_fields
from utils.document_parser import parse_aadhaar_details, parse_pan_details
# from services.aadhaar_pan_service import (
#     process_pan_verification,
#     process_aadhaar_verification,
#     process_face_match
# )
from utils.document_parser import (
    parse_pan_details,
    parse_aadhaar_details
)
ai_bp = Blueprint("ai_bp", __name__)

UPLOAD_FOLDER = "uploads"


@ai_bp.route("/ocr", methods=["POST"])
@role_required([

    "SUPER_ADMIN"
])
def ocr_api():

    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "No file uploaded"
        }), 400

    file = request.files["file"]

    candidate_id = request.form.get("candidate_id")

    document_type = request.form.get("document_type")

    if not candidate_id:
        return jsonify({
            "success": False,
            "message": "candidate_id is required"
        }), 400

    if not document_type:
        return jsonify({
            "success": False,
            "message": "document_type is required"
        }), 400

    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "Empty filename"
        }), 400

    filename = secure_filename(file.filename)

    candidate_folder = os.path.join(
        UPLOAD_FOLDER,
        candidate_id
    )

    document_folder = os.path.join(
        candidate_folder,
        document_type
    )

    os.makedirs(document_folder, exist_ok=True)

    file_path = os.path.join(
        document_folder,
        filename
    )

    file.save(file_path)

    extension = filename.split(".")[-1].lower()

    try:

        if extension in ["png", "jpg", "jpeg"]:

            extracted_text = extract_text_from_image(file_path)
            if document_type.lower() == "pan":

                parsed_data = parse_pan_details(extracted_text)

            elif document_type.lower() == "aadhaar":

                parsed_data = parse_aadhaar_details(extracted_text)

            else:

                parsed_data = {}
        elif extension == "pdf":

            extracted_text = extract_pdf_text(file_path)

        elif extension in ["docx", "doc"]:

            extracted_text = extract_docx_text(file_path)

        else:

            return jsonify({
                "success": False,
                "message": "Unsupported file format"
            }), 400

        return jsonify({

            "success": True,

            "candidate_id": candidate_id,

            "document_type": document_type,

            "filename": filename,

            "stored_path": file_path,

            "extracted_data": parsed_data,

            "raw_text": extracted_text

        })
    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    from services.aadhaar_pan_service import (
    process_pan_verification,
    process_aadhaar_verification
)
# @ai_bp.route("/verify-pan", methods=["POST"])
# def verify_pan_api():

#     data = request.get_json()

#     result = process_pan_verification(data)

#     return jsonify(result)
# @ai_bp.route("/verify-aadhaar", methods=["POST"])
# def verify_aadhaar_api():

#     data = request.get_json()

#     result = process_aadhaar_verification(data)

#     return jsonify(result)
# @ai_bp.route("/face-match", methods=["POST"])
# def face_match_api():

#     data = request.get_json()

#     result = process_face_match(data)

#     return jsonify(result)

@ai_bp.route("/ocr/verify", methods=["POST"])
@jwt_required()
@role_required(["SUPER_ADMIN"])
def verify_ocr():

    try:

        data = request.get_json()

        extracted_data = data.get("extracted_data")

        expected_data = data.get("expected_data")

        verification_result = verify_pan_fields(
            extracted_data,
            expected_data
        )

        return jsonify({

            "success": True,
            "verification_result": verification_result

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,
            "message": str(e)

        }), 500
