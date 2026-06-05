import os
import uuid

from flask import Blueprint
from flask import request
from flask import jsonify
from werkzeug.utils import secure_filename

from db import get_connection


document_bp = Blueprint(

    "document_bp",
    __name__
)


UPLOAD_FOLDER = "uploads"


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

                "message": (
                    "secure_token is required"
                )
            }), 400

        if not bgv_id:

            return jsonify({

                "success": False,

                "message": (
                    "bgv_id is required"
                )
            }), 400

        if not document_type:

            return jsonify({

                "success": False,

                "message": (
                    "document_type is required"
                )
            }), 400

        if not file:

            return jsonify({

                "success": False,

                "message": (
                    "file is required"
                )
            }), 400

        os.makedirs(

            UPLOAD_FOLDER,

            exist_ok=True
        )

        original_filename = secure_filename(

            file.filename
        )

        unique_filename = (

            f"{uuid.uuid4()}_"
            f"{original_filename}"
        )

        file_path = os.path.join(

            UPLOAD_FOLDER,

            unique_filename
        )

        file.save(
            file_path
        )

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        # ======================================
        # GET CANDIDATE FROM TOKEN
        # ======================================

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

            return jsonify({

                "success": False,

                "message": (
                    "Invalid secure token"
                )
            }), 400

        candidate_id = access_data.get(
            "candidate_id"
        )

        access_link_id = access_data.get(
            "id"
        )

        # ======================================
        # SAVE DOCUMENT
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
                file_path,
                file.mimetype,
                0,
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

            "message": (
                "Document uploaded successfully"
            )
        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)
        }), 500