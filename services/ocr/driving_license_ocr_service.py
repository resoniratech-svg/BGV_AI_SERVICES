import json
import base64
import os

from repositories.driving_license_repository import (
    DrivingLicenseRepository
)

from repositories.provider_usage_repository import (
    ProviderUsageRepository
)

from services.ongrid.ongrid_client import (
    OnGridClient
)


class DrivingLicenseOCRService:

    @staticmethod
    def process_ocr(

            candidate_id,
            bgv_id,
            front_image_path,
            back_image_path

    ):

        ###################################################
        # VALIDATE FILES
        ###################################################

        if not os.path.exists(front_image_path):

            raise Exception(
                "Driving license front image not found"
            )

        if not os.path.exists(back_image_path):

            raise Exception(
                "Driving license back image not found"
            )

        ###################################################
        # CONVERT TO BASE64
        ###################################################

        with open(front_image_path, "rb") as file:

            front_base64 = (

                base64.b64encode(

                    file.read()

                ).decode("utf-8")

            )

        with open(back_image_path, "rb") as file:

            back_base64 = (

                base64.b64encode(

                    file.read()

                ).decode("utf-8")

            )

        ###################################################
        # GRIDLINES OCR
        ###################################################

        payload = {

            "front_image": front_base64,

            "back_image": back_base64,

            "consent": "Y"

        }

        try:

            response = OnGridClient.post(

                "/dl-api/ocr",

                payload

            )

        except Exception as e:

            raise Exception(

                f"Unable to connect to Gridlines Driving License OCR API. {str(e)}"

            )

        

        ###################################################
        # VALIDATION
        ###################################################

        if not response:

            raise Exception(

                "No response received from Gridlines Driving License OCR service."

            )

        if response.get("status") != 200:

            error_message = (

                response.get("data", {})

                .get("message")

                or response.get("message")

                or "Driving License OCR request failed."

            )

            raise Exception(error_message)

        data = response.get("data", {})

        if data.get("code") != "1002":

            raise Exception(

                data.get(

                    "message",

                    "Unable to extract Driving License details from the uploaded document."

                )

            )

        ocr_data = data.get("ocr_data")

        if not ocr_data:

            raise Exception(

                "Driving License OCR data not found in provider response."

            )

        if not ocr_data.get("document_id"):

            raise Exception(

                "Driving License number could not be extracted from the uploaded document."

            )

        if not ocr_data.get("name"):

            raise Exception(

                "Candidate name could not be extracted from the uploaded document."

            )

        if not ocr_data.get("date_of_birth"):

            raise Exception(

                "Date of birth could not be extracted from the uploaded document."

            )

        if not ocr_data.get("address"):

            raise Exception(

                "Address could not be extracted from the uploaded document."

            )

        ###################################################
        # OCR DATA
        ###################################################

        ocr = (

        data

        .get("ocr_data", {})

        )

        ###################################################
        # SAVE OCR RESULT
        ###################################################

        ocr_result_id = (

            DrivingLicenseRepository

            .save_driving_license_ocr_result(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                document_id=ocr.get(
                    "document_id"
                ),

                license_number=ocr.get(
                    "document_id"
                ),

                full_name=ocr.get(
                    "name"
                ),

                dependent_name=ocr.get(
                    "dependent_name"
                ),

                date_of_birth=ocr.get(
                    "date_of_birth"
                ),

                issue_date=ocr.get(
                    "issued_date"
                ),

                expiry_date=ocr.get(
                    "valid_till"
                ),

                place_of_issue=ocr.get(
                    "place_of_issue"
                ),

                address=ocr.get(
                    "address"
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

        ###################################################
        # PROVIDER USAGE
        ###################################################

        ProviderUsageRepository.increment_usage(

            provider_name="GRIDLINES",

            verification_type="DRIVING_LICENSE_OCR"

        )

        ###################################################
        # RETURN
        ###################################################

        return {

            "ocr_result_id":

            ocr_result_id,

            "license_number":

            ocr.get(

                "document_id"

            ),

            "full_name":

            ocr.get(

                "name"

            ),

            "dependent_name":

            ocr.get(

                "dependent_name"

            ),

            "date_of_birth":

            ocr.get(

                "date_of_birth"

            ),

            "issue_date":

            ocr.get(

                "issued_date"

            ),

            "expiry_date":

            ocr.get(

                "valid_till"

            ),

            "place_of_issue":

            ocr.get(

                "place_of_issue"

            ),

            "address":

            ocr.get(

                "address"

            ),

            "provider_name":

            "GRIDLINES",

            "api_reference_id":

            response.get(

                "request_id"

            ),

            "raw_response":

            response

        }
    