import json

from services.ongrid.ongrid_client import (
    OnGridClient
)

from repositories.pan_repository import (
    PanRepository
)

from repositories.provider_usage_repository import (
    ProviderUsageRepository
)


class OnGridPANService:

    @staticmethod
    def verify_pan(
        candidate_id,
        bgv_id,
        pan_ocr_result_id,
        pan_number,
        full_name,
        date_of_birth
    ):

        payload = {

            "pan_number": pan_number,

            "name": full_name,

            "date_of_birth": date_of_birth,

            "consent": "Y"
        }

        print("=" * 80)
        print("GRIDLINES PAN PAYLOAD")
        print(payload)
        print("=" * 80)

        response = OnGridClient.post(

            "/pan-api/verify",

            payload
        )

        name_match_status = (
            response.get(
                "data",
                {}
            ).get(
                "pan_data",
                {}
            ).get(
                "name_match_status"
            )
        )

        dob_match_status = (
            response.get(
                "data",
                {}
            ).get(
                "pan_data",
                {}
            ).get(
                "dob_match_status"
            )
        )

        verification_status = (
            "VERIFIED"
            if (
                name_match_status == "MATCH"
                and
                dob_match_status == "MATCH"
            )
            else "FAILED"
        )

        PanRepository.save_pan_verification_result(

            candidate_id=candidate_id,

            bgv_id=bgv_id,

            pan_ocr_result_id=pan_ocr_result_id,

            verification_status=verification_status,

            pan_number=pan_number,

            full_name=full_name,

            date_of_birth=date_of_birth,

            name_match_status=name_match_status,

            dob_match_status=dob_match_status,

            provider_name="GRIDLINES",

            api_reference_id=response.get(
                "request_id"
            ),

            raw_response=json.dumps(
                response
            )
        )

        ProviderUsageRepository.increment_usage(

            provider_name="GRIDLINES",

            verification_type="PAN"
        )

        return {

            "success": (
                verification_status
                == "VERIFIED"
            ),

            "provider": "GRIDLINES",

            "request_id": response.get(
                "request_id"
            ),

            "status": response.get(
                "status"
            ),

            "response": response
        }