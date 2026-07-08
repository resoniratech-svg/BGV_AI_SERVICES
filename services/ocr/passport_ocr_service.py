import os
import json
import base64

from repositories.document_repository import (
    DocumentRepository
)

from repositories.passport_repository import (
    PassportRepository
)

from services.ongrid.ongrid_client import (
    OnGridClient
)


class PassportOCRService:

    @staticmethod
    def extract_passport_data(
        candidate_id,
        bgv_id,
        document_id
    ):

        ####################################################
        # Uploaded Passport
        ####################################################

        document = (
            DocumentRepository
            .get_uploaded_document(
                document_id
            )
        )

        if not document:
            raise Exception(
                "Passport document not found"
            )

        file_path = os.path.abspath(
            document["file_path"]
        )

        if not os.path.exists(file_path):
            raise Exception(
                f"Passport file not found : {file_path}"
            )

        ####################################################
        # Base64
        ####################################################

        with open(file_path, "rb") as file:

            base64_data = (
                base64
                .b64encode(
                    file.read()
                )
                .decode("utf-8")
            )

        ####################################################
        # OCR API
        ####################################################

        payload = {

            "base64_data": base64_data,

            "consent": "Y"

        }

        response = (
            OnGridClient.post(
                "/passport-api/ocr",
                payload
            )
        )

        print("=" * 80)
        print("PASSPORT OCR RESPONSE")
        print(json.dumps(response, indent=4))
        print("=" * 80)

        ####################################################
        # Validation
        ####################################################

        if not response:
            raise Exception(
                "Empty Passport OCR response"
            )

        if response.get("status") != 200:
            raise Exception(

                    response.get(

                        "raw_response",

                        response.get(

                            "message",

                            "Passport OCR failed"

                        )

                    )

                )

        if (
            response
            .get("data", {})
            .get("code")
        ) != "1007":

            raise Exception(

                response
                .get("data", {})
                .get(
                    "message",
                    "Passport OCR failed"
                )

            )

        ####################################################
        # OCR DATA
        ####################################################

        ocr = (
            response["data"]["ocr_data"]
        )

        ####################################################
        # SAVE OCR RESULT
        ####################################################

        passport_ocr_result_id = (
            PassportRepository
            .save_passport_ocr_result(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                document_id=document_id,

                passport_number=ocr.get(
                    "document_id"
                ),

                file_number=ocr.get(
                    "file_number"
                ),

                given_name=ocr.get(
                    "first_name"
                ),

                surname=ocr.get(
                    "last_name"
                ),

                full_name=ocr.get(
                    "full_name"
                ),

                gender=ocr.get(
                    "gender"
                ),

                date_of_birth=ocr.get(
                    "date_of_birth"
                ),

                issue_date=ocr.get(
                    "issue_date"
                ),

                expiry_date=ocr.get(
                    "valid_till"
                ),

                nationality=ocr.get(
                    "nationality"
                ),

                country=ocr.get(
                    "country"
                ),

                guardian_name=ocr.get(
                    "guardian_name"
                ),

                mother_name=ocr.get(
                    "mother_name"
                ),

                place_of_birth=ocr.get(
                    "place_of_birth"
                ),

                place_of_issue=ocr.get(
                    "place_of_issue"
                ),

                provider_name="GRIDLINES",

                api_reference_id=response.get(
                    "request_id"
                ),

                raw_response=json.dumps(
                    response
                )

            )
        )

        ####################################################
        # RETURN
        ####################################################

        return {

            "passport_ocr_result_id":
            passport_ocr_result_id,

            "passport_number":
            ocr.get("document_id"),

            "file_number":
            ocr.get("file_number"),

            "given_name":
            ocr.get("first_name"),

            "surname":
            ocr.get("last_name"),

            "full_name":
            ocr.get("full_name"),

            "gender":
            ocr.get("gender"),

            "date_of_birth":
            ocr.get("date_of_birth"),

            "issue_date":
            ocr.get("issue_date"),

            "expiry_date":
            ocr.get("valid_till"),

            "country":
            ocr.get("country"),

            "nationality":
            ocr.get("nationality"),

            "guardian_name":
            ocr.get("guardian_name"),

            "mother_name":
            ocr.get("mother_name"),

            "place_of_birth":
            ocr.get("place_of_birth"),

            "place_of_issue":
            ocr.get("place_of_issue"),

            "request_id":
            response.get("request_id"),

            "raw_response":
            response

        }