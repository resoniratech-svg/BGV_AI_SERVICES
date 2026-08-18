import json


from repositories.aadhaar_repository import AadhaarRepository


class AadhaarVerificationService:
    @staticmethod
    def verify_aadhaar(candidate_id, bgv_id, document_id=None):

        # ==========================================
        # GET SESSION
        # ==========================================

        session = AadhaarRepository.get_aadhaar_session(candidate_id)

        if not session:
            raise Exception("Aadhaar consent session not found")

        if session["session_status"] != "SUCCESS":
            raise Exception("Candidate has not completed Aadhaar consent")

        try:
            response = json.loads(session["raw_response"])

        except Exception:
            raise Exception("Invalid Aadhaar session response")

        # ==========================================
        # EXTRACT UIDAI DATA
        # ==========================================

        ovse_data = response.get("data", {}).get("ovse_data", {})

        address = ovse_data.get("address") or ""

        resident_image = ovse_data.get("resident_image") or ""
        if not resident_image:
            raise Exception("Resident image not received from UIDAI")

        resident_name = ovse_data.get("resident_name") or ""
        if not resident_name:
            raise Exception("Resident name not received from UIDAI")

        uidai_dob = ovse_data.get("dob") or ""

        if not uidai_dob:
            raise Exception("Date of birth not received from UIDAI")

        uidai_gender = ovse_data.get("gender") or ""
        if not uidai_gender:
            raise Exception("Gender not received from UIDAI")

        # ==========================================
        # FINAL STATUS
        # ==========================================

        verification_status = "VERIFIED"
        # ==========================================
        # SAVE RESULT
        # ==========================================

        AadhaarRepository.save_aadhaar_verification_result(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            verification_status=verification_status,
            resident_name=resident_name,
            date_of_birth=uidai_dob,
            gender=uidai_gender,
            address=address,
            resident_image=resident_image,
            provider_name="GRIDLINES",
            api_reference_id=response.get("request_id"),
            raw_response=json.dumps(response),
        )

        return {
            "success": True,
            "verification_status": "VERIFIED",
            "resident_name": resident_name,
            "date_of_birth": uidai_dob,
            "gender": uidai_gender,
            "address": address,
            "provider": "GRIDLINES",
        }
