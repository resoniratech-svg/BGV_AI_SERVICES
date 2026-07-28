import os
import base64

from repositories.document_repository import (
    DocumentRepository
)

from services.ongrid.ongrid_client import (
    OnGridClient
)


class PanOCRService:

    @staticmethod
    def extract_pan_data(

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
                "PAN document not found"
            )

        file_path = os.path.abspath(
            document["file_path"]
        )

        if not os.path.exists(
            file_path
        ):

            raise Exception(
                f"Document file not found: {file_path}"
            )

        # ======================================
        # CONVERT TO BASE64
        # ======================================

        with open(
            file_path,
            "rb"
        ) as file:

            base64_data = (
                base64.b64encode(
                    file.read()
                )
                .decode("utf-8")
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

        try:

            response = OnGridClient.post(

                "/pan-api/ocr",

                payload

            )

        except Exception as e:

            raise Exception(

                f"Unable to connect to Gridlines PAN OCR API. {str(e)}"

    )

       

        # ======================================
        # RESPONSE VALIDATION
        # ======================================

        if not response:

            raise Exception(
                "Empty OCR response received"
            )

        if response.get("status") != 200:

            raise Exception(

                response.get(
                    "message",
                    "PAN OCR request failed."
                )

            )

        # ======================================
        # BUSINESS RESPONSE VALIDATION
        # ======================================

        data = response.get("data", {})

        code = data.get("code")

        if code != "1009":

            raise Exception(

                data.get(

                    "message",

                    "PAN OCR failed."

                )

            )

        # ======================================
        # OCR DATA VALIDATION
        # ======================================

        if not data.get("ocr_data"):

            raise Exception(

                "PAN OCR data not found."

            )
        # ======================================
        # EXTRACT DATA
        # ======================================

        document_data = (

    response.get(

        "data",

        {}

    ).get(

        "ocr_data",

        {}

    ).get(

        "document",

        {}

    )

)

        pan_number = (

            document_data.get(
                "document_id"
            )
        )

        full_name = (

            document_data.get(
                "name"
            )
        )

        father_name = (

            document_data.get(
                "father_name"
            )
        )

        date_of_birth = (

            document_data.get(
                "date_of_birth"
            )
        )

        # ======================================
        # RETURN DATA
        # ======================================

        return {

            "pan_number":
            pan_number,

            "full_name":
            full_name,

            "father_name":
            father_name,

            "date_of_birth":
            date_of_birth,

            "request_id":
            response.get(
                "request_id"
            ),

            "raw_response":
            response

        }