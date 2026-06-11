import json
from urllib import response

from services.ongrid.ongrid_client import (
    OnGridClient
)

from repositories.driving_license_repository import (
    DrivingLicenseRepository
)
from repositories.provider_usage_repository import (
    ProviderUsageRepository
)
class OnGridDrivingLicenseService:

    @staticmethod
    def verify_driving_license(
        dl_number,
        date_of_birth,
        candidate_id,
        bgv_id
    ):

        payload = {

            "driving_license_number": dl_number,

            "date_of_birth": date_of_birth,

            "consent": "Y"
        }
        print("=" * 80)
        print("GRIDLINES DL PAYLOAD")
        print(payload)
        print("=" * 80)
        response = OnGridClient.post(

            "/dl-api/fetch",

            payload
        )
        DrivingLicenseRepository.save_driving_license_result(

            candidate_id=candidate_id,

            bgv_id=bgv_id,

            verification_status=(
                "APPROVED"
                if response.get("data", {}).get("code") == "1000"
                else "FAILED"
            ),

            license_number=dl_number,

            full_name=None,

            date_of_birth=date_of_birth,

            issue_date=None,

            expiry_date=None,

            provider_name="ongrid",

            api_reference_id=response.get(
                "request_id"
            ),

            raw_response=json.dumps(response)
        )
        gridlines_success = (
            response.get(
                "data",
                {}
            ).get(
                "code"
            ) == "1000"
        )
        ProviderUsageRepository.increment_usage(

            provider_name="ONGRID",

            verification_type="DRIVING_LICENSE"
        )

        return {
            "success": gridlines_success,
            "provider": "ongrid",
            "request_id": response.get("request_id"),
            "status": response.get("status"),
            "response": response
        }