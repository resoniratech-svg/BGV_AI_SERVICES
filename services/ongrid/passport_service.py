import uuid
import json
from datetime import datetime
from services.ongrid.ongrid_client import (
    OnGridClient
)
from repositories.passport_repository import (
    PassportRepository
)
from repositories.provider_usage_repository import (
    ProviderUsageRepository
)
class OnGridPassportService:

    @staticmethod
    def verify_passport(
        candidate_id,
        bgv_id,
        passport_number,
        file_number,
        surname,
        given_name,
        date_of_birth
    ):

        payload = {

            "passport_number": passport_number,

            "file_number": file_number,

            "surname": surname,

            "given_name": given_name,

            "date_of_birth": date_of_birth,

            "consent": "Y"
        }
        print("=" * 80)
        print("GRIDLINES PASSPORT PAYLOAD")
        print(payload)
        print("=" * 80)
        print("=" * 80)
        print("PASSPORT NUMBER =", passport_number)
        print("FILE NUMBER =", file_number)
        print("SURNAME =", surname)
        print("GIVEN NAME =", given_name)
        print("DATE OF BIRTH =", date_of_birth)
        print("=" * 80)
        response = OnGridClient.post(
            "/passport-api/verify",
            payload
        )
        date_of_birth_db = datetime.strptime(
            date_of_birth,
            "%d/%m/%Y"
            ).strftime("%Y-%m-%d")
        PassportRepository.save_passport_result(

            candidate_id=candidate_id,

            bgv_id=bgv_id,

            verification_status=(
                "APPROVED"
                if response.get("status") == 200
                else "FAILED"
            ),

            passport_number=passport_number,

            full_name=(
                f"{given_name} {surname}"
            ),

            nationality=None,

            country=None,

            date_of_birth=date_of_birth_db,

            issue_date=None,

            expiry_date=None,

            provider_name="ongrid",

            api_reference_id=response.get(
                "request_id"
            ),

            raw_response=json.dumps(response)
        )
        return {

            "success": True,

            "provider": "ongrid",

            "request_id": response.get(
                "request_id"
            ),

            "status": response.get(
                "status"
            ),

            "response": response
        }
    ProviderUsageRepository.increment_usage(

    provider_name="ONGRID",

    verification_type="PASSPORT"
)