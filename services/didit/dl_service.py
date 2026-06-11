import json
import requests

from config import Config

from repositories.document_repository import (
    DocumentRepository
)

from repositories.driving_license_repository import (
    DrivingLicenseRepository
)

from repositories.provider_usage_repository import (
    ProviderUsageRepository
)


class DiditDrivingLicenseService:

    @staticmethod
    def verify_driving_license(
        candidate_id,
        bgv_id,
        front_document_id,
        back_document_id
    ):

        front_document = (
            DocumentRepository
            .get_uploaded_document(
                front_document_id
            )
        )

        if not front_document:

            raise Exception(
                "Driving license front image not found"
            )

        back_document = (
            DocumentRepository
            .get_uploaded_document(
                back_document_id
            )
        )

        if not back_document:

            raise Exception(
                "Driving license back image not found"
            )

        front_file_path = front_document.get(
            "file_path"
        )

        back_file_path = back_document.get(
            "file_path"
        )

        headers = {
            "x-api-key": Config.DIDIT_API_KEY
        }

        with open(front_file_path, "rb") as front_file, \
             open(back_file_path, "rb") as back_file:

            files = {

                "front_image": front_file,

                "back_image": back_file
            }

            response = requests.post(

                f"{Config.DIDIT_BASE_URL}/v3/id-verification/",

                headers=headers,

                files=files,

                timeout=60
            )

        response.raise_for_status()

        response_data = response.json()

        id_verification = (
            response_data.get(
                "id_verification",
                {}
            )
        )

        DrivingLicenseRepository.save_driving_license_result(

            candidate_id=candidate_id,

            bgv_id=bgv_id,

            verification_status=id_verification.get(
                "status"
            ),

            license_number=id_verification.get(
                "document_number"
            ),

            full_name=id_verification.get(
                "full_name"
            ),

            date_of_birth=id_verification.get(
                "date_of_birth"
            ),

            issue_date=id_verification.get(
                "date_of_issue"
            ),

            expiry_date=id_verification.get(
                "expiration_date"
            ),

            provider_name="Didit",

            api_reference_id=response_data.get(
                "request_id"
            ),

            raw_response=json.dumps(
                response_data
            )
        )

        ProviderUsageRepository.increment_usage(

            provider_name="DIDIT",

            verification_type="DRIVING_LICENSE"
        )

        return {

            "success": True,

            "provider": "didit",

            "reference_id": response_data.get(
                "request_id"
            ),

            "verification_status": id_verification.get(
                "status"
            )
        }