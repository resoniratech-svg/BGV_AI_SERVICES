import os
import base64

from repositories.document_repository import (
    DocumentRepository
)

from services.ongrid.ongrid_client import (
    OnGridClient
)


class AadhaarOCRService:

    @staticmethod
    def extract_aadhaar_data(

        candidate_id,
        bgv_id,
        document_id

    ):

        # ======================================
        # GET DOCUMENT
        # ======================================

        document = (

            DocumentRepository
            .get_uploaded_document(
                document_id
            )

        )

        if not document:

            raise Exception(
                "Aadhaar document not found"
            )

        file_path = os.path.abspath(

            document[
                "file_path"
            ]

        )

        if not os.path.exists(
            file_path
        ):

            raise Exception(

                f"Document file not found: {file_path}"

            )

        # ======================================
        # CONVERT FILE TO BASE64
        # ======================================

        with open(
            file_path,
            "rb"
        ) as file:

            base64_data = (

                base64.b64encode(
                    file.read()
                )

                .decode(
                    "utf-8"
                )

            )

        # ======================================
        # OCR REQUEST
        # ======================================

        payload = {

            "base64_data":
            base64_data,

            "consent":
            "Y"
        }

        response = (

            OnGridClient
            .post(

                "/ocr",

                payload

            )

        )

        # ======================================
        # RESPONSE VALIDATION
        # ======================================

        if not response:

            raise Exception(
                "Empty Aadhaar OCR response"
            )

        if response.get(
            "status"
        ) != 200:

            raise Exception(

                response.get(
                    "message",
                    "Aadhaar OCR failed"
                )

            )

        if not response.get(
            "data",
            {}
        ).get(
            "ocr_data"
        ):

            raise Exception(

                response.get(
                    "data",
                    {}
                ).get(
                    "message",
                    "Aadhaar OCR failed"
                )

            )

        # ======================================
        # EXTRACT DATA
        # ======================================

        document_data = (

            response

            ["data"]

            ["ocr_data"]

            ["document"]

        )

        return {

            "aadhaar_number":

            document_data.get(
                "document_id"
            ),

            "virtual_id":

            document_data.get(
                "virtual_id"
            ),

            "full_name":

            document_data.get(
                "name"
            ),

            "date_of_birth":

            document_data.get(
                "date_of_birth"
            ),

            "gender":

            document_data.get(
                "gender"
            ),

            "request_id":

            response.get(
                "request_id"
            ),

            "raw_response":

            response
        }