import json
import re

from services.ongrid.ongrid_client import OnGridClient
from repositories.pan_repository import PanRepository
from repositories.provider_usage_repository import ProviderUsageRepository


def normalize_name(value):
    """
    Utility function removed from the class scope because it doesn't
    rely on class state or instance properties.
    """
    if not value:
        return ""
    
    value = value.upper()
    value = re.sub(r"\s+", " ", value)
    return value.strip()


class OnGridPANService:

    @staticmethod
    def verify_pan(candidate_id, bgv_id, pan_ocr_result_id, pan_number, full_name, date_of_birth):
        # =====================================
        # PREPARE REQUEST PAYLOAD
        # =====================================
        payload = {
            "pan_number": pan_number,
            "consent": "Y"
        }

        # =====================================
        # CALL GRIDLINES PAN API
        # =====================================
        try:
            response = OnGridClient.post("/pan-api/fetch-detailed", payload)
        except Exception as e:
            raise Exception(f"Unable to connect to Gridlines PAN API. {str(e)}")

        # =====================================
        # VALIDATE RESPONSE
        # =====================================
        if not response:
            raise Exception("Empty response received from Gridlines.")

        if response.get("status") != 200:
            raise Exception(response.get("message", "Gridlines PAN API request failed."))

        # =====================================
        # VALIDATE BUSINESS RESPONSE
        # =====================================
        data_block = response.get("data", {})
        code = data_block.get("code")

        if code != "1000":
            return {

            "success": False,

            "provider": "GRIDLINES",

            "provider_code": code,

            "message": response.get(

                "data",

                {}

            ).get(

                "message",

                "PAN verification unsuccessful."

            )

}
        # =====================================
        # EXTRACT PAN DATA
        # =====================================
        pan_data = data_block.get("pan_data", {})
        if not pan_data:
            raise Exception("PAN verification data not found.")

        provider_pan_number = pan_data.get("document_id") or ""
        provider_full_name = pan_data.get("name") or ""
        provider_dob = pan_data.get("date_of_birth") or ""

        # =====================================
        # NORMALIZE & COMPARE STRINGS
        # =====================================
        normalized_provider_name = normalize_name(provider_full_name)
        normalized_ocr_name = normalize_name(full_name)

        pan_match_status = "MATCH" if pan_number.upper() == provider_pan_number.upper() else "NOT_MATCH"
        name_match_status = "MATCH" if normalized_ocr_name == normalized_provider_name else "NOT_MATCH"
        dob_match_status = "MATCH" if str(date_of_birth).strip() == str(provider_dob).strip() else "NOT_MATCH"

        verification_status = (
            "VERIFIED" 
            if pan_match_status == "MATCH" and name_match_status == "MATCH" and dob_match_status == "MATCH"
            else "FAILED"
        )

        # =====================================
        # SAVE VERIFICATION RESULT
        # =====================================
        try:
            verification_result_id = PanRepository.save_pan_verification_result(
                candidate_id=candidate_id,
                bgv_id=bgv_id,
                pan_ocr_result_id=pan_ocr_result_id,
                verification_status=verification_status,
                pan_number=provider_pan_number,
                full_name=normalized_provider_name,
                date_of_birth=provider_dob,
                pan_match_status=pan_match_status,
                name_match_status=name_match_status,
                dob_match_status=dob_match_status,
                provider_name="GRIDLINES",
                api_reference_id=response.get("request_id"),
                raw_response=json.dumps(response)
            )
        except Exception as e:
            raise Exception(f"Unable to save PAN verification result. {str(e)}")

        # =====================================
        # UPDATE PROVIDER USAGE (NON-BLOCKING)
        # =====================================
        try:
            ProviderUsageRepository.increment_usage(
                provider_name="GRIDLINES",
                verification_type="PAN"
            )
        except Exception as e:
            # Operational safeguards: Internal telemetry failures should never crash operations
            print(f"WARNING: Unable to update provider usage. {str(e)}")

        # =====================================
        # RETURN RESPONSE
        # =====================================
        return {
            "success": verification_status == "VERIFIED",
            "verification_result_id": verification_result_id,
            "verification_status": verification_status,
            "pan_match_status": pan_match_status,
            "name_match_status": name_match_status,
            "dob_match_status": dob_match_status,
            "provider": "GRIDLINES",
            "request_id": response.get("request_id"),
            "response": response
        }