import os
import uuid

from flask import Blueprint
from flask import request
from flask import jsonify
from werkzeug.utils import secure_filename

from db import get_connection
from config import Config

document_bp = Blueprint(
    "document_bp",
    __name__
)



UPLOAD_FOLDER = Config.UPLOAD_FOLDER
print("\n" + "=" * 80)
print("DOCUMENT ROUTES CONFIG")
print("UPLOAD_FOLDER =", UPLOAD_FOLDER)
print("=" * 80)

@document_bp.route(
    "/document/upload",
    methods=["POST"]
)
def upload_document():

    try:

        secure_token = request.form.get(
            "secure_token"
        )

        bgv_id = request.form.get(
            "bgv_id"
        )

        document_type = request.form.get(
            "document_type"
        )

        file = request.files.get(
            "file"
        )

        if not secure_token:

            return jsonify({
                "success": False,
                "message": "secure_token is required"
            }), 400

        if not bgv_id:

            return jsonify({
                "success": False,
                "message": "bgv_id is required"
            }), 400

        if not document_type:

            return jsonify({
                "success": False,
                "message": "document_type is required"
            }), 400

        if not file:

            return jsonify({
                "success": False,
                "message": "file is required"
            }), 400

        # ======================================
        # GET CANDIDATE FROM TOKEN
        # ======================================

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT candidate_id, id

            FROM candidate_access_links

            WHERE secure_token = %s

            LIMIT 1
            """,
            (
                secure_token,
            )
        )

        access_data = cursor.fetchone()

        if not access_data:

            cursor.close()
            connection.close()

            return jsonify({
                "success": False,
                "message": "Invalid secure token"
            }), 400

        candidate_id = access_data.get(
            "candidate_id"
        )

        access_link_id = access_data.get(
            "id"
        )

        # ======================================
        # CREATE CANDIDATE FOLDER
        # ======================================

        candidate_folder = os.path.join(
            UPLOAD_FOLDER,
            f"candidate_{candidate_id}",
            document_type
        )

        os.makedirs(
            candidate_folder,
            exist_ok=True
        )

        # ======================================
        # SAVE FILE
        # ======================================

        original_filename = secure_filename(
            file.filename
        )

        file_extension = os.path.splitext(
            original_filename
        )[1]

        unique_filename = (
            f"{uuid.uuid4()}{file_extension}"
        )

        file_path = os.path.join(
            candidate_folder,
            unique_filename
        )
        print("\n" + "=" * 80)
        print("UPLOAD DEBUG")
        print("FILE NAME =", original_filename)
        print("FINAL SAVE PATH =", file_path)
        print("=" * 80)
        file.save(
            file_path
        )
        print("FILE EXISTS AFTER SAVE =", os.path.exists(file_path))

        if os.path.exists(file_path):
            print("FILE SIZE AFTER SAVE =", os.path.getsize(file_path))

        # Verify file saved successfully

        if not os.path.exists(
            file_path
        ):
            raise Exception(
                "File save failed"
            )

        file_size = os.path.getsize(
            file_path
        )

        if file_size == 0:

            os.remove(
                file_path
            )

            raise Exception(
                "Uploaded file is empty"
            )

        # Normalize path for DB

        db_file_path = file_path.replace(
            "\\",
            "/"
        )

        # ======================================
        # SAVE DOCUMENT RECORD
        # ======================================

        insert_query = """
            INSERT INTO
            candidate_uploaded_documents (

                candidate_id,
                bgv_id,
                access_link_id,
                document_type,
                original_filename,
                stored_filename,
                file_path,
                mime_type,
                file_size,
                upload_status

            )

            VALUES (

                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """

        cursor.execute(
            insert_query,
            (
                candidate_id,
                bgv_id,
                access_link_id,
                document_type,
                original_filename,
                unique_filename,
                db_file_path,
                file.mimetype,
                file_size,
                "UPLOADED"
            )
        )

        connection.commit()

        document_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return jsonify({

            "success": True,

            "document_id": document_id,

            "candidate_id": candidate_id,

            "file_size": file_size,

            "file_path": db_file_path,

            "message": "Document uploaded successfully"

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500