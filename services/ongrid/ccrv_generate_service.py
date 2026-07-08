import json

from datetime import datetime
from datetime import timedelta

from services.ongrid.ongrid_client import (
    OnGridClient
)

from repositories.ccrv_repository import (
    CCRVRepository
)

from repositories.pan_repository import (
    PanRepository
)

from repositories.aadhaar_repository import (
    AadhaarRepository
)

from repositories.consent_repository import (
    ConsentRepository
)

from repositories.provider_usage_repository import (
    ProviderUsageRepository
)


class CCRVGenerateService:

    @staticmethod
    def generate_report(

            candidate_id,
            bgv_id

    ):

        ####################################################
        # PAN OCR DATA
        ####################################################

        pan = (

            PanRepository
            .get_pan_ocr_result(
                candidate_id
            )

        )

        if not pan:

            raise Exception(
                "PAN OCR data not found"
            )

        ####################################################
        # AADHAAR VERIFIED DATA
        ####################################################

        aadhaar = (

            AadhaarRepository
            .get_aadhaar_verification_result(
                candidate_id
            )

        )

        if not aadhaar:

            raise Exception(
                "Aadhaar verification not found"
            )

        ####################################################
        # CONSENT
        ####################################################

        consent = (

            ConsentRepository
            .get_candidate_consent(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                verification_type="CCRV"

            )

        )

        if not consent:

            raise Exception(
                "Candidate CCRV consent not found"
            )

        if consent["consent_status"] != "GRANTED":

            raise Exception(
                "Candidate has not provided CCRV consent"
            )

        ####################################################
        # REQUIRED VALUES
        ####################################################

        full_name = pan.get("full_name")

        father_name = pan.get("father_name")

        date_of_birth = pan.get("date_of_birth")

        address = aadhaar.get("address")

        if not full_name:
            raise Exception("Full name not available")

        if not father_name:
            raise Exception("Father name not available")

        if not date_of_birth:
            raise Exception("Date of birth not available")

        if not address:
            raise Exception("Address not available")

        ####################################################
        # GRIDLINES PAYLOAD
        ####################################################

        payload = {

            "name": full_name,

            "father_name": father_name,

            "date_of_birth": date_of_birth,

            "address": address,

            "consent": "Y"

        }

        print("=" * 80)
        print("CCRV GENERATE PAYLOAD")
        print(json.dumps(payload, indent=4))
        print("=" * 80)

        ####################################################
        # API CALL
        ####################################################

        response = (

            OnGridClient.post(

                "/ccrv-api/generate-report",

                payload

            )

        )

        print("=" * 80)
        print("CCRV GENERATE RESPONSE")
        print(json.dumps(response, indent=4))
        print("=" * 80)

        ####################################################
        # VALIDATION
        ####################################################

        if not response:

            raise Exception(
                "Empty CCRV response"
            )

        if response.get("status") != 200:

            raise Exception(

                response.get(
                    "message",
                    "CCRV request failed"
                )

            )

        data = response.get("data", {})

        if data.get("code") != "1000":

            raise Exception(

                data.get(
                    "message",
                    "Unable to generate CCRV report"
                )

            )

        ####################################################
        # SAVE REQUEST
        ####################################################

        requested_at = datetime.now()

        expected_completion = (

            requested_at +

            timedelta(hours=8)

        )

        CCRVRepository.save_request(

            candidate_id=candidate_id,

            bgv_id=bgv_id,

            consent_id=consent["id"],

            provider_name="GRIDLINES",

            transaction_id=response.get(
                "transaction_id"
            ),

            request_id=response.get(
                "request_id"
            ),

            ccrv_status="REQUESTED",

            api_reference_id=response.get(
                "request_id"
            ),

            raw_response=json.dumps(response),

            requested_at=requested_at,

            expected_completion_at=expected_completion

        )

        ####################################################
        # PROVIDER USAGE
        ####################################################

        ProviderUsageRepository.increment_usage(

            provider_name="GRIDLINES",

            verification_type="CCRV"

        )

        ####################################################
        # RETURN
        ####################################################

        return {

            "success": True,

            "verification_status": "REQUESTED",

            "transaction_id": response.get(
                "transaction_id"
            ),

            "request_id": response.get(
                "request_id"
            ),

            "expected_completion_at":

                expected_completion.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

        }