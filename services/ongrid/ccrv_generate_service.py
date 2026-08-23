import json

from datetime import datetime
from datetime import timedelta

from config import Config

from services.ongrid.ongrid_client import OnGridClient

from repositories.ccrv_repository import CCRVRepository

from repositories.pan_repository import PanRepository

from repositories.aadhaar_repository import AadhaarRepository

from repositories.consent_repository import ConsentRepository

from repositories.provider_usage_repository import ProviderUsageRepository


class CCRVGenerateService:
    @staticmethod
    def generate_report(candidate_id, bgv_id):

        ####################################################
        # PAN OCR DATA
        ####################################################

        pan = PanRepository.get_pan_ocr_result(candidate_id)

        if not pan:
            raise Exception(
                "PAN OCR result not found. Please complete PAN OCR before CCRV verification."
            )

        ####################################################
        # AADHAAR VERIFIED DATA
        ####################################################

        aadhaar = AadhaarRepository.get_aadhaar_verification_result(candidate_id)

        if not aadhaar:
            raise Exception(
                "Verified Aadhaar data not found. CCRV requires verified Aadhaar data."
            )

        address = aadhaar.get("address")

        if not address:
            raise Exception(
                "Verified Aadhaar address is missing. CCRV requires a verified address."
            )
        ####################################################
        # CONSENT
        ####################################################

        consent = ConsentRepository.get_candidate_consent(
            candidate_id=candidate_id, bgv_id=bgv_id, verification_type="CCRV"
        )

        if not consent:
            raise Exception("Candidate CCRV consent not found.")

        ####################################################
        # CONSENT STATUS
        ####################################################

        if consent.get("consent_status") != "GIVEN":
            raise Exception(
                f"Candidate consent status is '{consent.get('consent_status')}'. Expected status is 'GIVEN'."
            )

        ####################################################
        # REQUIRED VALUES
        ####################################################

        full_name = pan.get("full_name")

        father_name = pan.get("father_name")

        date_of_birth = pan.get("date_of_birth")

        if date_of_birth:
            date_of_birth = str(date_of_birth)

        if not full_name:
            raise Exception("Full name not available.")

        if not father_name:
            raise Exception("Father name not available.")

        if not date_of_birth:
            raise Exception("Date of birth not available.")

        if not address:
            raise Exception("Address not available.")

        ####################################################
        # GRIDLINES PAYLOAD
        ####################################################

        payload = {
            "name": full_name,
            "father_name": father_name,
            "date_of_birth": date_of_birth,
            "address": address,
            "consent": "Y",
            "callback_url": Config.CCRV_CALLBACK_URL,
        }

        print("=" * 80)
        print("CCRV GENERATE PAYLOAD")
        print(json.dumps(payload, indent=4, default=str))
        print("=" * 80)

        ####################################################
        # CALL GRIDLINES
        ####################################################

        response = OnGridClient.post("/ccrv-api/generate-report", payload)

        print("=" * 80)
        print("CCRV GENERATE RESPONSE")
        print(json.dumps(response, indent=4))
        print("=" * 80)

        ####################################################
        # EMPTY RESPONSE
        ####################################################

        if not response:
            raise Exception("Empty CCRV response.")

        ####################################################
        # API FAILURE
        ####################################################

        if response.get("success") is False:
            status = response.get("status")

            ####################################################
            # 400
            ####################################################

            if status == 400:
                raise Exception(
                    "Gridlines rejected the CCRV Generate request. Please verify the payload."
                )

            ####################################################
            # 401
            ####################################################

            if status == 401:
                raise Exception(
                    "Gridlines authentication failed. Please verify the API Key."
                )

            ####################################################
            # 403
            ####################################################

            if status == 403:
                raise Exception(
                    "Gridlines access forbidden. Your account does not have permission to use the CCRV Generate API."
                )

            ####################################################
            # 404
            ####################################################

            if status == 404:
                raise Exception("Gridlines CCRV Generate API endpoint not found.")

            ####################################################
            # 409
            ####################################################

            if status == 409:
                raise Exception("Gridlines reported a duplicate CCRV request.")

            ####################################################
            # 429
            ####################################################

            if status == 429:
                raise Exception(
                    "Gridlines API rate limit exceeded. Please try again later."
                )

            ####################################################
            # SERVER ERROR
            ####################################################

            if status >= 500:
                raise Exception(
                    "Gridlines server is temporarily unavailable. Please try again later."
                )

            ####################################################
            # UNKNOWN
            ####################################################

            raise Exception(
                response.get("raw_response", "Unknown error received from Gridlines.")
            )
        ####################################################
        # RESPONSE DATA
        ####################################################

        data = response.get("data", {})

        ####################################################
        # VALIDATION
        ####################################################

        transaction_id = data.get("transaction_id") or response.get("transaction_id")

        request_id = data.get("request_id") or response.get("request_id")

        if not transaction_id:
            raise Exception("Transaction ID not received from Gridlines.")

        ####################################################
        # SAVE REQUEST
        ####################################################

        requested_at = datetime.now()

        expected_completion = requested_at + timedelta(hours=8)

        CCRVRepository.save_request(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            consent_id=consent["id"],
            provider_name="GRIDLINES",
            transaction_id=transaction_id,
            request_id=request_id,
            ccrv_status="REQUESTED",
            api_reference_id=request_id,
            raw_response=json.dumps(response, default=str),
            requested_at=requested_at,
            expected_completion_at=expected_completion,
        )

        ####################################################
        # PROVIDER USAGE
        ####################################################

        ProviderUsageRepository.increment_usage(
            provider_name="GRIDLINES", verification_type="CCRV"
        )

        ####################################################
        # RETURN
        ####################################################

        return {
            "success": True,
            "message": "CCRV report generation initiated successfully.",
            "verification_status": "REQUESTED",
            "transaction_id": transaction_id,
            "request_id": request_id,
            "expected_completion_at": expected_completion.strftime("%Y-%m-%d %H:%M:%S"),
        }
