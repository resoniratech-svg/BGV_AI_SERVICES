# import os
# import json

# from repositories.document_repository import DocumentRepository
# from repositories.passport_repository import PassportRepository
# from services.ongrid.ongrid_client import OnGridClient


# class PassportOCRService:
#     @staticmethod
#     def extract_passport_data(
#         candidate_id,
#         bgv_id,
#         front_document_id,
#         back_document_id,
#     ):
#         ####################################################
#         # 1. GET PASSPORT FRONT DOCUMENT
#         ####################################################

#         front_document = DocumentRepository.get_document_by_id(front_document_id)

#         if not front_document:
#             raise Exception("Passport front document not found")

#         front_file_path = os.path.abspath(front_document["file_path"])

#         if not os.path.exists(front_file_path):
#             raise Exception(f"Passport front file not found: {front_file_path}")

#         ####################################################
#         # 2. GET PASSPORT BACK DOCUMENT
#         ####################################################

#         back_document = DocumentRepository.get_document_by_id(back_document_id)

#         if not back_document:
#             raise Exception("Passport back document not found")

#         back_file_path = os.path.abspath(back_document["file_path"])

#         if not os.path.exists(back_file_path):
#             raise Exception(f"Passport back file not found: {back_file_path}")

#         ####################################################
#         # 3. VALIDATE DOCUMENT TYPES
#         ####################################################

#         if front_document.get("document_type") != "Passport":
#             raise Exception("Front document is not a Passport document")

#         if back_document.get("document_type") != "Passport":
#             raise Exception("Back document is not a Passport document")

#         ####################################################
#         # 4. GRIDLINES PASSPORT OCR
#         #
#         # Gridlines requires:
#         #
#         # multipart/form-data
#         #
#         # file_front
#         # file_back
#         # consent
#         #
#         ####################################################

#         try:
#             with (
#                 open(front_file_path, "rb") as front_file,
#                 open(back_file_path, "rb") as back_file,
#             ):
#                 files = {
#                     "file_front": (
#                         front_document["original_filename"],
#                         front_file,
#                         front_document.get(
#                             "mime_type",
#                             "application/octet-stream",
#                         ),
#                     ),
#                     "file_back": (
#                         back_document["original_filename"],
#                         back_file,
#                         back_document.get(
#                             "mime_type",
#                             "application/octet-stream",
#                         ),
#                     ),
#                 }

#                 data = {
#                     "consent": "Y",
#                 }

#                 response = OnGridClient.post_multipart(
#                     "/passport-api/ocr",
#                     files=files,
#                     data=data,
#                 )

#         except Exception as e:
#             raise Exception(
#                 f"Unable to connect to Gridlines Passport OCR API. {str(e)}"
#             )

#         ####################################################
#         # 5. VALIDATE GRIDLINES RESPONSE
#         ####################################################

#         if not response:
#             raise Exception("Empty Passport OCR response")

#         response_status = response.get("status")

#         if response_status != 200:
#             error_message = response.get("message")

#             if not error_message:
#                 error_message = response.get(
#                     "raw_response",
#                     "Passport OCR failed",
#                 )

#             raise Exception(f"Gridlines Passport OCR failed: {error_message}")

#         ####################################################
#         # 6. VALIDATE OCR SUCCESS CODE
#         #
#         # Gridlines documentation:
#         #
#         # 1007 = Data extracted
#         #
#         ####################################################

#         response_data = response.get("data", {})

#         response_code = response_data.get("code")

#         if response_code != "1007":
#             raise Exception(
#                 response_data.get(
#                     "message",
#                     "Passport OCR failed",
#                 )
#             )

#         ####################################################
#         # 7. EXTRACT OCR DATA
#         ####################################################

#         ocr = response_data.get("ocr_data", {})

#         if not ocr:
#             raise Exception("Passport OCR returned empty OCR data")

#         ####################################################
#         # 8. BASIC OCR VALIDATION
#         ####################################################

#         if not ocr.get("document_id"):
#             raise Exception("Passport number was not extracted")

#         ####################################################
#         # 9. SAVE OCR RESULT
#         ####################################################

#         passport_ocr_result_id = PassportRepository.save_passport_ocr_result(
#             candidate_id=candidate_id,
#             bgv_id=bgv_id,
#             # Existing database structure stores
#             # the primary/front passport document ID.
#             document_id=front_document_id,
#             passport_number=ocr.get("document_id"),
#             file_number=ocr.get("file_number"),
#             given_name=ocr.get("first_name"),
#             surname=ocr.get("last_name"),
#             full_name=ocr.get("full_name"),
#             gender=ocr.get("gender"),
#             date_of_birth=ocr.get("date_of_birth"),
#             issue_date=ocr.get("issue_date"),
#             expiry_date=ocr.get("valid_till"),
#             nationality=ocr.get("nationality"),
#             country=ocr.get("country"),
#             guardian_name=ocr.get("guardian_name"),
#             mother_name=ocr.get("mother_name"),
#             place_of_birth=ocr.get("place_of_birth"),
#             place_of_issue=ocr.get("place_of_issue"),
#             provider_name="GRIDLINES",
#             api_reference_id=response.get("request_id"),
#             raw_response=json.dumps(response),
#         )

#         ####################################################
#         # 10. RETURN OCR RESULT
#         ####################################################

#         return {
#             "passport_ocr_result_id": passport_ocr_result_id,
#             "passport_number": ocr.get("document_id"),
#             "file_number": ocr.get("file_number"),
#             "given_name": ocr.get("first_name"),
#             "surname": ocr.get("last_name"),
#             "full_name": ocr.get("full_name"),
#             "gender": ocr.get("gender"),
#             "date_of_birth": ocr.get("date_of_birth"),
#             "issue_date": ocr.get("issue_date"),
#             "expiry_date": ocr.get("valid_till"),
#             "country": ocr.get("country"),
#             "nationality": ocr.get("nationality"),
#             "guardian_name": ocr.get("guardian_name"),
#             "mother_name": ocr.get("mother_name"),
#             "place_of_birth": ocr.get("place_of_birth"),
#             "place_of_issue": ocr.get("place_of_issue"),
#             "request_id": response.get("request_id"),
#             "transaction_id": response.get("transaction_id"),
#             "raw_response": response,
#         }
import os
import json
from datetime import datetime

from repositories.document_repository import DocumentRepository
from repositories.passport_repository import PassportRepository
from services.ongrid.ongrid_client import OnGridClient


class PassportOCRService:
    @staticmethod
    def clean_date(value):
        """
        Convert Gridlines passport date values into MySQL-compatible
        YYYY-MM-DD format.

        Empty strings, None, and invalid dates become None.
        """

        # ---------------------------------------------
        # NULL / EMPTY VALUE
        # ---------------------------------------------

        if value is None:
            return None

        value = str(value).strip()

        if not value:
            return None

        # ---------------------------------------------
        # ALREADY MYSQL FORMAT
        # ---------------------------------------------

        formats = [
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%Y/%m/%d",
            "%d.%m.%Y",
            "%d %m %Y",
            "%d %b %Y",
            "%d %B %Y",
            "%b %d %Y",
            "%B %d %Y",
        ]

        for fmt in formats:
            try:
                parsed_date = datetime.strptime(value, fmt)

                return parsed_date.strftime("%Y-%m-%d")

            except ValueError:
                continue

        # ---------------------------------------------
        # DEBUG INVALID DATE
        # ---------------------------------------------

        print("=" * 80)
        print("PASSPORT DATE PARSE WARNING")
        print("ORIGINAL VALUE:", repr(value))
        print("Unable to convert value into YYYY-MM-DD")
        print("Returning NULL")
        print("=" * 80)

        return None

    @staticmethod
    def extract_passport_data(
        candidate_id,
        bgv_id,
        front_document_id,
        back_document_id,
    ):

        ####################################################
        # GET PASSPORT FRONT DOCUMENT
        ####################################################

        front_document = DocumentRepository.get_document_by_id(front_document_id)

        if not front_document:
            raise Exception(f"Passport front document not found: {front_document_id}")

        print("=" * 80)
        print("PASSPORT FRONT DOCUMENT")
        print(front_document)
        print("=" * 80)

        ####################################################
        # VALIDATE FRONT DOCUMENT TYPE
        ####################################################

        front_document_type = (
            (front_document.get("document_type") or "").strip().lower()
        )

        if front_document_type != "passport front":
            raise Exception(
                "Front document is not a Passport Front document. "
                f"Received: {front_document.get('document_type')}"
            )

        ####################################################
        # FRONT FILE
        ####################################################

        front_file_path = os.path.abspath(front_document["file_path"])

        if not os.path.exists(front_file_path):
            raise Exception(f"Passport front file not found: {front_file_path}")

        ####################################################
        # GET PASSPORT BACK DOCUMENT
        ####################################################

        back_document = DocumentRepository.get_document_by_id(back_document_id)

        if not back_document:
            raise Exception(f"Passport back document not found: {back_document_id}")

        print("=" * 80)
        print("PASSPORT BACK DOCUMENT")
        print(back_document)
        print("=" * 80)

        ####################################################
        # VALIDATE BACK DOCUMENT TYPE
        ####################################################

        back_document_type = (back_document.get("document_type") or "").strip().lower()

        if back_document_type != "passport back":
            raise Exception(
                "Back document is not a Passport Back document. "
                f"Received: {back_document.get('document_type')}"
            )

        ####################################################
        # BACK FILE
        ####################################################

        back_file_path = os.path.abspath(back_document["file_path"])

        if not os.path.exists(back_file_path):
            raise Exception(f"Passport back file not found: {back_file_path}")

        ####################################################
        # DEBUG FILE VALIDATION
        ####################################################

        print("=" * 80)
        print("PASSPORT FILE VALIDATION")
        print("=" * 80)

        print("FRONT DOCUMENT ID:", front_document_id)
        print(
            "FRONT DOCUMENT TYPE:",
            front_document_type,
        )
        print(
            "FRONT ORIGINAL FILE:",
            front_document.get("original_filename"),
        )
        print(
            "FRONT FILE:",
            front_file_path,
        )
        print(
            "FRONT EXISTS:",
            os.path.exists(front_file_path),
        )

        print()

        print("BACK DOCUMENT ID:", back_document_id)
        print(
            "BACK DOCUMENT TYPE:",
            back_document_type,
        )
        print(
            "BACK ORIGINAL FILE:",
            back_document.get("original_filename"),
        )
        print(
            "BACK FILE:",
            back_file_path,
        )
        print(
            "BACK EXISTS:",
            os.path.exists(back_file_path),
        )

        print("=" * 80)

        ####################################################
        # GRIDLINES PASSPORT OCR
        ####################################################

        try:
            with (
                open(front_file_path, "rb") as front_file,
                open(back_file_path, "rb") as back_file,
            ):
                files = {
                    "file_front": (
                        front_document["original_filename"],
                        front_file,
                        front_document.get(
                            "mime_type",
                            "application/octet-stream",
                        ),
                    ),
                    "file_back": (
                        back_document["original_filename"],
                        back_file,
                        back_document.get(
                            "mime_type",
                            "application/octet-stream",
                        ),
                    ),
                }

                data = {
                    "consent": "Y",
                }

                print("=" * 80)
                print("CALLING GRIDLINES PASSPORT OCR")
                print("=" * 80)

                response = OnGridClient.post_multipart(
                    "/passport-api/ocr",
                    files=files,
                    data=data,
                )

                print("=" * 80)
                print("GRIDLINES RESPONSE")
                print(response)
                print("=" * 80)

        except Exception as e:
            raise Exception(
                "Unable to connect to Gridlines Passport OCR API. " + str(e)
            )

        ####################################################
        # RESPONSE VALIDATION
        ####################################################

        if not response:
            raise Exception("Empty Passport OCR response")

        ####################################################
        # HTTP RESPONSE STATUS
        ####################################################

        if response.get("status") != 200:
            error_message = response.get("raw_response")

            if not error_message:
                error_message = response.get(
                    "message",
                    "Passport OCR failed",
                )

            raise Exception(error_message)

        ####################################################
        # GRIDLINES BUSINESS RESPONSE
        ####################################################

        response_data = response.get(
            "data",
            {},
        )

        if not isinstance(response_data, dict):
            raise Exception("Invalid Passport OCR response data")

        ####################################################
        # GRIDLINES BUSINESS CODE
        ####################################################

        if response_data.get("code") != "1007":
            raise Exception(
                response_data.get(
                    "message",
                    "Passport OCR failed",
                )
            )

        ####################################################
        # OCR DATA
        ####################################################

        ocr = response_data.get(
            "ocr_data",
            {},
        )

        if not isinstance(ocr, dict):
            raise Exception("Invalid Passport OCR data")

        ####################################################
        # DEBUG OCR RESPONSE
        ####################################################

        print("=" * 80)
        print("PASSPORT OCR DATA")
        print("=" * 80)

        print(
            json.dumps(
                ocr,
                indent=4,
                default=str,
            )
        )

        print("=" * 80)

        ####################################################
        # CLEAN DATE FIELDS
        ####################################################

        date_of_birth = PassportOCRService.clean_date(ocr.get("date_of_birth"))

        issue_date = PassportOCRService.clean_date(ocr.get("issue_date"))

        expiry_date = PassportOCRService.clean_date(ocr.get("valid_till"))

        ####################################################
        # DEBUG CLEANED DATES
        ####################################################

        print("=" * 80)
        print("PASSPORT CLEANED DATE VALUES")
        print("=" * 80)

        print(
            "ORIGINAL DATE OF BIRTH:",
            repr(ocr.get("date_of_birth")),
        )

        print(
            "CLEANED DATE OF BIRTH:",
            repr(date_of_birth),
        )

        print(
            "ORIGINAL ISSUE DATE:",
            repr(ocr.get("issue_date")),
        )

        print(
            "CLEANED ISSUE DATE:",
            repr(issue_date),
        )

        print(
            "ORIGINAL EXPIRY DATE:",
            repr(ocr.get("valid_till")),
        )

        print(
            "CLEANED EXPIRY DATE:",
            repr(expiry_date),
        )

        print("=" * 80)

        ####################################################
        # SAVE OCR RESULT
        ####################################################

        passport_ocr_result_id = PassportRepository.save_passport_ocr_result(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            document_id=front_document_id,
            passport_number=ocr.get("document_id"),
            file_number=ocr.get("file_number"),
            given_name=ocr.get("first_name"),
            surname=ocr.get("last_name"),
            full_name=ocr.get("full_name"),
            gender=ocr.get("gender"),
            date_of_birth=date_of_birth,
            issue_date=issue_date,
            expiry_date=expiry_date,
            nationality=ocr.get("nationality"),
            country=ocr.get("country"),
            guardian_name=ocr.get("guardian_name"),
            mother_name=ocr.get("mother_name"),
            place_of_birth=ocr.get("place_of_birth"),
            place_of_issue=ocr.get("place_of_issue"),
            provider_name="GRIDLINES",
            api_reference_id=response.get("request_id"),
            raw_response=json.dumps(response),
        )

        ####################################################
        # DEBUG DATABASE RESULT
        ####################################################

        print("=" * 80)
        print("PASSPORT OCR DATABASE SAVE")
        print("=" * 80)

        print(
            "PASSPORT OCR RESULT ID:",
            passport_ocr_result_id,
        )

        print("=" * 80)

        ####################################################
        # RETURN OCR RESULT
        ####################################################

        return {
            "passport_ocr_result_id": passport_ocr_result_id,
            "passport_number": ocr.get("document_id"),
            "file_number": ocr.get("file_number"),
            "given_name": ocr.get("first_name"),
            "surname": ocr.get("last_name"),
            "full_name": ocr.get("full_name"),
            "gender": ocr.get("gender"),
            "date_of_birth": date_of_birth,
            "issue_date": issue_date,
            "expiry_date": expiry_date,
            "country": ocr.get("country"),
            "nationality": ocr.get("nationality"),
            "guardian_name": ocr.get("guardian_name"),
            "mother_name": ocr.get("mother_name"),
            "place_of_birth": ocr.get("place_of_birth"),
            "place_of_issue": ocr.get("place_of_issue"),
            "request_id": response.get("request_id"),
            "raw_response": response,
        }
