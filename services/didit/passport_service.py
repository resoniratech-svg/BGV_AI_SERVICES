import json
import requests

from config import Config

from repositories.document_repository import (
    DocumentRepository
)

from repositories.passport_repository import (
    PassportRepository
)
from repositories.provider_usage_repository import ProviderUsageRepository


class DiditPassportService:

    @staticmethod
    def verify_passport(
        candidate_id,
        bgv_id,
        document_id
    ):

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

        file_path = document.get(
            "file_path"
        )

        headers = {
            "x-api-key": Config.DIDIT_API_KEY
        }

        with open(file_path, "rb") as passport_file:

            files = {
                "front_image": passport_file
            }
            print("DIDIT_BASE_URL =", Config.DIDIT_BASE_URL)
            print("DIDIT_API_KEY =", Config.DIDIT_API_KEY[:10] + "...")

            response = requests.post(
                f"{Config.DIDIT_BASE_URL}/v3/id-verification/",
                headers=headers,
                files=files,
                timeout=60
            )

        if response.status_code != 200:
            raise Exception(
                f"Didit Error: {response.text}"
            )

        response_data = response.json()

        id_verification = (
            response_data.get(
                "id_verification",
                {}
            )
        )

        passport_result_id = (
            PassportRepository
            .save_passport_result(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                verification_status=id_verification.get(
                    "status"
                ),

                passport_number=id_verification.get(
                    "document_number"
                ),

                full_name=id_verification.get(
                    "full_name"
                ),

                nationality=id_verification.get(
                    "nationality"
                ),

                country=id_verification.get(
                    "issuing_state"
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
        )
        ProviderUsageRepository.increment_usage(

            provider_name="didit",

            verification_type="passport_dl"
        )
        return {

            "success": True,

            "passport_result_id": (
                passport_result_id
            ),

            "provider": "Didit",

            "request_id": (
                response_data.get(
                    "request_id"
                )
            )
        }