# import json
# import os

# import requests

# from repositories.driving_license_repository import (
#     DrivingLicenseRepository,
# )

# from repositories.provider_usage_repository import (
#     ProviderUsageRepository,
# )

# from services.ongrid.ongrid_client import OnGridClient


# class DrivingLicenseOCRService:
#     ###################################################
#     # DRIVING LICENSE OCR
#     ###################################################

#     @staticmethod
#     def process_ocr(
#         candidate_id,
#         bgv_id,
#         front_image_path,
#         back_image_path,
#     ):

#         ###################################################
#         # VALIDATE FRONT FILE
#         ###################################################

#         if not front_image_path:
#             raise Exception("Driving license front image path is required")

#         if not os.path.exists(front_image_path):
#             raise Exception("Driving license front image not found")

#         ###################################################
#         # VALIDATE BACK FILE
#         ###################################################

#         if not back_image_path:
#             raise Exception("Driving license back image path is required")

#         if not os.path.exists(back_image_path):
#             raise Exception("Driving license back image not found")

#         ###################################################
#         # GRIDLINES OCR URL
#         ###################################################

#         url = "https://api.gridlines.io/dl-api/ocr"

#         ###################################################
#         # GET GRIDLINES CONFIGURATION
#         #
#         # We intentionally do NOT use Config.GRIDLINES_BASE_URL
#         # because that property does not exist in your project.
#         #
#         # The existing project already uses OnGridClient for
#         # Gridlines API communication.
#         ###################################################

#         ###################################################
#         # PREPARE MULTIPART REQUEST
#         ###################################################

#         payload = {
#             "consent": "Y",
#         }

#         front_filename = os.path.basename(front_image_path)
#         back_filename = os.path.basename(back_image_path)

#         ###################################################
#         # DETERMINE CONTENT TYPES
#         ###################################################

#         front_content_type = (
#             "application/pdf"
#             if front_filename.lower().endswith(".pdf")
#             else "image/jpeg"
#         )

#         back_content_type = (
#             "application/pdf"
#             if back_filename.lower().endswith(".pdf")
#             else "image/jpeg"
#         )

#         ###################################################
#         # GRIDLINES OCR REQUEST
#         ###################################################

#         try:
#             ###################################################
#             # IMPORTANT:
#             #
#             # Gridlines DL OCR requires multipart/form-data:
#             #
#             # file_front
#             # file_back
#             # consent
#             #
#             # We therefore send the actual files.
#             ###################################################

#             # -------------------------------------------------
#             # Obtain API configuration from the existing
#             # OnGridClient module.
#             # -------------------------------------------------

#             api_key = getattr(
#                 OnGridClient,
#                 "API_KEY",
#                 None,
#             )

#             if not api_key:
#                 raise Exception("Gridlines API key is not configured in OnGridClient.")

#             headers = {
#                 "Accept": "application/json",
#                 "X-API-Key": api_key,
#                 "X-Auth-Type": "API-Key",
#             }

#             with (
#                 open(
#                     front_image_path,
#                     "rb",
#                 ) as front_file,
#                 open(
#                     back_image_path,
#                     "rb",
#                 ) as back_file,
#             ):
#                 files = {
#                     "file_front": (
#                         front_filename,
#                         front_file,
#                         front_content_type,
#                     ),
#                     "file_back": (
#                         back_filename,
#                         back_file,
#                         back_content_type,
#                     ),
#                 }

#                 ###################################################
#                 # DEBUG REQUEST
#                 ###################################################

#                 print("=" * 80)
#                 print("GRIDLINES DRIVING LICENSE OCR REQUEST")
#                 print("=" * 80)

#                 print("URL:")
#                 print(url)

#                 print("FRONT FILE:")
#                 print(front_filename)

#                 print("BACK FILE:")
#                 print(back_filename)

#                 print("CONSENT:")
#                 print(payload["consent"])

#                 print("=" * 80)

#                 ###################################################
#                 # API REQUEST
#                 ###################################################

#                 provider_response = requests.post(
#                     url,
#                     headers=headers,
#                     data=payload,
#                     files=files,
#                     timeout=180,
#                 )

#         ###################################################
#         # TIMEOUT
#         ###################################################

#         except requests.exceptions.Timeout:
#             raise Exception("Gridlines Driving License OCR request timed out.")

#         ###################################################
#         # CONNECTION ERROR
#         ###################################################

#         except requests.exceptions.ConnectionError:
#             raise Exception(
#                 "Unable to connect to Gridlines Driving License OCR service."
#             )

#         ###################################################
#         # REQUEST ERROR
#         ###################################################

#         except requests.exceptions.RequestException as e:
#             raise Exception(f"Gridlines Driving License OCR request failed. {str(e)}")

#         ###################################################
#         # OTHER ERROR
#         ###################################################

#         except Exception as e:
#             raise Exception(f"Unable to process Driving License OCR request. {str(e)}")

#         ###################################################
#         # PRINT PROVIDER RESPONSE
#         ###################################################

#         print("=" * 80)
#         print("GRIDLINES DRIVING LICENSE OCR RESPONSE")
#         print("=" * 80)

#         print(
#             "HTTP STATUS:",
#             provider_response.status_code,
#         )

#         print(
#             "RESPONSE:",
#             provider_response.text,
#         )

#         print("=" * 80)

#         ###################################################
#         # PARSE JSON RESPONSE
#         ###################################################

#         try:
#             response = provider_response.json()

#         except ValueError:
#             raise Exception(
#                 "Gridlines Driving License OCR returned an invalid JSON response."
#             )

#         ###################################################
#         # EMPTY RESPONSE
#         ###################################################

#         if not response:
#             raise Exception(
#                 "No response received from Gridlines Driving License OCR service."
#             )

#         ###################################################
#         # HTTP STATUS VALIDATION
#         ###################################################

#         if provider_response.status_code != 200:
#             data = response.get(
#                 "data",
#                 {},
#             )

#             error_message = (
#                 data.get("message")
#                 or response.get("message")
#                 or "Driving License OCR request failed."
#             )

#             raise Exception(f"Gridlines Driving License OCR failed: {error_message}")

#         ###################################################
#         # GRIDLINES STATUS VALIDATION
#         ###################################################

#         if response.get("status") != 200:
#             data = response.get(
#                 "data",
#                 {},
#             )

#             error_message = (
#                 data.get("message")
#                 or response.get("message")
#                 or "Driving License OCR request failed."
#             )

#             raise Exception(error_message)

#         ###################################################
#         # RESPONSE DATA
#         ###################################################

#         data = response.get(
#             "data",
#             {},
#         )

#         ###################################################
#         # SUCCESS CODE
#         ###################################################

#         if data.get("code") != "1002":
#             raise Exception(
#                 data.get(
#                     "message",
#                     "Unable to extract Driving License "
#                     "details from the uploaded document.",
#                 )
#             )

#         ###################################################
#         # OCR DATA
#         ###################################################

#         ocr_data = data.get("ocr_data")

#         if not ocr_data:
#             raise Exception("Driving License OCR data not found in provider response.")

#         ###################################################
#         # REQUIRED DOCUMENT NUMBER
#         ###################################################

#         if not ocr_data.get("document_id"):
#             raise Exception(
#                 "Driving License number could not be "
#                 "extracted from the uploaded document."
#             )

#         ###################################################
#         # REQUIRED NAME
#         ###################################################

#         if not ocr_data.get("name"):
#             raise Exception(
#                 "Candidate name could not be extracted from the uploaded document."
#             )

#         ###################################################
#         # REQUIRED DATE OF BIRTH
#         ###################################################

#         if not ocr_data.get("date_of_birth"):
#             raise Exception(
#                 "Date of birth could not be extracted from the uploaded document."
#             )

#         ###################################################
#         # REQUIRED ADDRESS
#         ###################################################

#         if not ocr_data.get("address"):
#             raise Exception(
#                 "Address could not be extracted from the uploaded document."
#             )

#         ###################################################
#         # EXTRACT OCR VALUES
#         ###################################################

#         license_number = ocr_data.get("document_id")

#         full_name = ocr_data.get("name")

#         dependent_name = ocr_data.get("dependent_name")

#         date_of_birth = ocr_data.get("date_of_birth")

#         issue_date = ocr_data.get("issued_date")

#         expiry_date = ocr_data.get("valid_till")

#         place_of_issue = ocr_data.get("place_of_issue")

#         address = ocr_data.get("address")

#         ###################################################
#         # SAVE OCR RESULT
#         ###################################################

#         ocr_result_id = DrivingLicenseRepository.save_driving_license_ocr_result(
#             candidate_id=candidate_id,
#             bgv_id=bgv_id,
#             document_id=license_number,
#             license_number=license_number,
#             full_name=full_name,
#             dependent_name=dependent_name,
#             date_of_birth=date_of_birth,
#             issue_date=issue_date,
#             expiry_date=expiry_date,
#             place_of_issue=place_of_issue,
#             address=address,
#             provider_name="GRIDLINES",
#             api_reference_id=response.get("request_id"),
#             raw_response=json.dumps(response),
#         )

#         ###################################################
#         # PROVIDER USAGE
#         ###################################################

#         ProviderUsageRepository.increment_usage(
#             provider_name="GRIDLINES",
#             verification_type="DRIVING_LICENSE_OCR",
#         )

#         ###################################################
#         # RETURN OCR RESULT
#         ###################################################

#         return {
#             "ocr_result_id": ocr_result_id,
#             "license_number": license_number,
#             "full_name": full_name,
#             "dependent_name": dependent_name,
#             "date_of_birth": date_of_birth,
#             "issue_date": issue_date,
#             "expiry_date": expiry_date,
#             "place_of_issue": place_of_issue,
#             "address": address,
#             "provider_name": "GRIDLINES",
#             "api_reference_id": response.get("request_id"),
#             "raw_response": response,
#         }


import json
import os

from repositories.driving_license_repository import (
    DrivingLicenseRepository,
)

from repositories.provider_usage_repository import (
    ProviderUsageRepository,
)

from services.ongrid.ongrid_client import OnGridClient


class DrivingLicenseOCRService:
    # =====================================================
    # DRIVING LICENSE OCR
    # =====================================================

    @staticmethod
    def process_ocr(
        candidate_id,
        bgv_id,
        front_image_path,
        back_image_path,
    ):

        # =================================================
        # VALIDATE FRONT FILE
        # =================================================

        if not front_image_path:
            raise Exception("Driving license front image path is required")

        if not os.path.exists(front_image_path):
            raise Exception("Driving license front image not found")

        # =================================================
        # VALIDATE BACK FILE
        # =================================================

        if not back_image_path:
            raise Exception("Driving license back image path is required")

        if not os.path.exists(back_image_path):
            raise Exception("Driving license back image not found")

        print("=" * 80)
        print("STARTING DRIVING LICENSE OCR")
        print("=" * 80)

        print("CANDIDATE ID:", candidate_id)
        print("BGV ID:", bgv_id)

        print(
            "FRONT IMAGE:",
            front_image_path,
        )

        print(
            "BACK IMAGE:",
            back_image_path,
        )

        # =================================================
        # FILE NAMES
        # =================================================

        front_filename = os.path.basename(front_image_path)

        back_filename = os.path.basename(back_image_path)

        # =================================================
        # CONTENT TYPES
        # =================================================

        front_content_type = (
            "application/pdf"
            if front_filename.lower().endswith(".pdf")
            else "image/jpeg"
        )

        back_content_type = (
            "application/pdf"
            if back_filename.lower().endswith(".pdf")
            else "image/jpeg"
        )

        # =================================================
        # GRIDLINES OCR PAYLOAD
        # =================================================

        data = {
            "consent": "Y",
        }

        # =================================================
        # PREPARE MULTIPART FILES
        # =================================================

        try:
            with (
                open(
                    front_image_path,
                    "rb",
                ) as front_file,
                open(
                    back_image_path,
                    "rb",
                ) as back_file,
            ):
                files = {
                    "file_front": (
                        front_filename,
                        front_file,
                        front_content_type,
                    ),
                    "file_back": (
                        back_filename,
                        back_file,
                        back_content_type,
                    ),
                }

                # =================================================
                # DEBUG
                # =================================================

                print("=" * 80)
                print("GRIDLINES DRIVING LICENSE OCR REQUEST")
                print("=" * 80)

                print(
                    "ENDPOINT:",
                    "/dl-api/ocr",
                )

                print(
                    "FRONT FILE:",
                    front_filename,
                )

                print(
                    "BACK FILE:",
                    back_filename,
                )

                print(
                    "CONSENT:",
                    data["consent"],
                )

                print("=" * 80)

                # =================================================
                # GRIDLINES API CALL
                # =================================================

                response = OnGridClient.post_multipart(
                    "/dl-api/ocr",
                    files=files,
                    data=data,
                )

        except Exception as e:
            raise Exception(f"Unable to process Driving License OCR request. {str(e)}")

        # =================================================
        # PRINT RESPONSE
        # =================================================

        print("=" * 80)
        print("GRIDLINES DRIVING LICENSE OCR RESPONSE")
        print("=" * 80)

        print(
            json.dumps(
                response,
                indent=4,
                default=str,
            )
        )

        print("=" * 80)

        # =================================================
        # VALIDATE RESPONSE
        # =================================================

        if not response:
            raise Exception(
                "No response received from Gridlines Driving License OCR service."
            )

        # =================================================
        # HANDLE CLIENT ERROR RESPONSE
        # =================================================

        if response.get("success") is False:
            error_message = (
                response.get("message")
                or response.get("raw_response")
                or "Driving License OCR request failed."
            )

            raise Exception(f"Gridlines Driving License OCR failed: {error_message}")

        # =================================================
        # HTTP STATUS
        # =================================================

        if response.get("status") != 200:
            data_response = response.get(
                "data",
                {},
            )

            error_message = (
                data_response.get("message")
                or response.get("message")
                or "Driving License OCR request failed."
            )

            raise Exception(f"Gridlines Driving License OCR failed: {error_message}")

        # =================================================
        # RESPONSE DATA
        # =================================================

        data_response = response.get(
            "data",
            {},
        )

        # =================================================
        # GRIDLINES OCR SUCCESS CODE
        # =================================================

        if data_response.get("code") != "1002":
            raise Exception(
                data_response.get(
                    "message",
                    "Unable to extract Driving License "
                    "details from the uploaded document.",
                )
            )

        # =================================================
        # OCR DATA
        # =================================================

        ocr_data = data_response.get("ocr_data")

        if not ocr_data:
            raise Exception("Driving License OCR data not found in provider response.")

        # =================================================
        # REQUIRED LICENSE NUMBER
        # =================================================

        if not ocr_data.get("document_id"):
            raise Exception(
                "Driving License number could not be "
                "extracted from the uploaded document."
            )

        # =================================================
        # REQUIRED NAME
        # =================================================

        if not ocr_data.get("name"):
            raise Exception(
                "Candidate name could not be extracted from the uploaded document."
            )

        # =================================================
        # REQUIRED DOB
        # =================================================

        if not ocr_data.get("date_of_birth"):
            raise Exception(
                "Date of birth could not be extracted from the uploaded document."
            )

        # =================================================
        # REQUIRED ADDRESS
        # =================================================

        if not ocr_data.get("address"):
            raise Exception(
                "Address could not be extracted from the uploaded document."
            )

        # =================================================
        # EXTRACT OCR VALUES
        # =================================================

        license_number = ocr_data.get("document_id")

        full_name = ocr_data.get("name")

        dependent_name = ocr_data.get("dependent_name")

        date_of_birth = ocr_data.get("date_of_birth")

        issue_date = ocr_data.get("issued_date")

        expiry_date = ocr_data.get("valid_till")

        place_of_issue = ocr_data.get("place_of_issue")

        address = ocr_data.get("address")

        # =================================================
        # DEBUG OCR VALUES
        # =================================================

        print("=" * 80)
        print("EXTRACTED DRIVING LICENSE OCR DATA")
        print("=" * 80)

        print(
            "LICENSE NUMBER:",
            license_number,
        )

        print(
            "FULL NAME:",
            full_name,
        )

        print(
            "DEPENDENT NAME:",
            dependent_name,
        )

        print(
            "DATE OF BIRTH:",
            date_of_birth,
        )

        print(
            "ISSUE DATE:",
            issue_date,
        )

        print(
            "EXPIRY DATE:",
            expiry_date,
        )

        print(
            "PLACE OF ISSUE:",
            place_of_issue,
        )

        print(
            "ADDRESS:",
            address,
        )

        print("=" * 80)

        # =================================================
        # SAVE OCR RESULT
        # =================================================

        ocr_result_id = DrivingLicenseRepository.save_driving_license_ocr_result(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            document_id=license_number,
            license_number=license_number,
            full_name=full_name,
            dependent_name=dependent_name,
            date_of_birth=date_of_birth,
            issue_date=issue_date,
            expiry_date=expiry_date,
            place_of_issue=place_of_issue,
            address=address,
            provider_name="GRIDLINES",
            api_reference_id=response.get("request_id"),
            raw_response=json.dumps(
                response,
                default=str,
            ),
        )

        # =================================================
        # VERIFY OCR RESULT ID
        # =================================================

        if not ocr_result_id:
            raise Exception(
                "Driving License OCR result could not be saved to database."
            )

        print("=" * 80)
        print(
            "DRIVING LICENSE OCR RESULT SAVED:",
            ocr_result_id,
        )
        print("=" * 80)

        # =================================================
        # PROVIDER USAGE
        # =================================================

        ProviderUsageRepository.increment_usage(
            provider_name="GRIDLINES",
            verification_type="DRIVING_LICENSE_OCR",
        )

        # =================================================
        # FINAL RETURN
        # =================================================

        return {
            "success": True,
            "ocr_result_id": ocr_result_id,
            "license_number": license_number,
            "full_name": full_name,
            "dependent_name": dependent_name,
            "date_of_birth": date_of_birth,
            "issue_date": issue_date,
            "expiry_date": expiry_date,
            "place_of_issue": place_of_issue,
            "address": address,
            "provider_name": "GRIDLINES",
            "api_reference_id": response.get("request_id"),
            "raw_response": response,
        }
