from repositories.pan_repository import PanRepository

from repositories.consent_repository import ConsentRepository

from services.ongrid.credit_bureau_service import CreditBureauService


class CreditBureauVerificationService:
    @staticmethod
    def verify_credit_bureau(candidate_id, bgv_id, first_name, last_name, phone):

        ####################################################
        # PAN OCR
        ####################################################

        pan = PanRepository.get_pan_ocr_result(candidate_id)

        if not pan:
            raise Exception("PAN OCR result not found.")

        ####################################################
        # CONSENT
        ####################################################

        consent = ConsentRepository.get_candidate_consent(
            candidate_id=candidate_id, bgv_id=bgv_id, verification_type="CREDIT_BUREAU"
        )

        if not consent:
            raise Exception("Candidate consent not found.")

        if consent.get("consent_status") != "GIVEN":
            raise Exception("Candidate has not given Credit Bureau consent.")

        ####################################################
        # REQUIRED VALUES
        ####################################################

        pan_number = pan.get("pan_number")

        consent_text = consent.get("consent_text")

        ####################################################
        # VALIDATIONS
        ####################################################

        if not first_name:
            raise Exception("Candidate first name is required.")

        if not phone:
            raise Exception("Candidate phone number is required.")

        if not pan_number:
            raise Exception("PAN number not found.")

        if not consent_text:
            raise Exception("Consent text not found.")

        ####################################################
        # GRIDLINES PAYLOAD
        ####################################################

        payload = {
            "phone": phone,
            "first_name": first_name,
            "last_name": last_name,
            "pan": pan_number,
            "consent": "Y",
            "consent_text": consent_text,
        }

        ####################################################
        # GRIDLINES VERIFICATION
        ####################################################

        return CreditBureauService.verify_credit_bureau(
            candidate_id=candidate_id, bgv_id=bgv_id, payload=payload
        )
