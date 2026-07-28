import json
from services.ocr.pan_ocr_service import PanOCRService
from services.ongrid.pan_service import OnGridPANService
from repositories.pan_repository import PanRepository


class OnGridPANVerificationService:

    @staticmethod
    def verify_pan(candidate_id, bgv_id, document_id):
        # =====================================
        # EXTRACT & VALIDATE PAN OCR DATA
        # =====================================
        try:
            pan_data = PanOCRService.extract_pan_data(
                candidate_id=candidate_id,
                bgv_id=bgv_id,
                document_id=document_id
            )
        except Exception as e:
            raise Exception(f"PAN OCR Service Error: {str(e)}")

        if not pan_data:
            raise Exception("PAN OCR failed. No data returned.")

        # Fail-fast validations
        pan_number = pan_data.get("pan_number")
        full_name = pan_data.get("full_name")
        dob = pan_data.get("date_of_birth")

        if not pan_number:
            raise Exception("PAN number not extracted from OCR.")
        if not full_name:
            raise Exception("PAN holder name not extracted from OCR.")
        if not dob:
            raise Exception("Date of birth not extracted from OCR.")

        # =====================================
        # SAVE OCR RESULT
        # =====================================
        try:
            # Safely stringify raw response; handles missing or None values cleanly
            raw_resp = pan_data.get("raw_response")
            serialized_raw_response = json.dumps(raw_resp) if raw_resp is not None else json.dumps({})

            pan_ocr_result_id = PanRepository.save_pan_ocr_result(
                candidate_id=candidate_id,
                bgv_id=bgv_id,
                document_id=document_id,
                pan_number=pan_number,
                full_name=full_name,
                father_name=pan_data.get("father_name"),
                date_of_birth=dob,
                provider_name="GRIDLINES",
                api_reference_id=pan_data.get("request_id"),
                raw_response=serialized_raw_response
            )
        except Exception as e:
            raise Exception(f"Unable to save PAN OCR result. {str(e)}")

        # =====================================
        # CALL PAN VERIFICATION API
        # =====================================
        try:
            verification_result = OnGridPANService.verify_pan(
                candidate_id=candidate_id,
                bgv_id=bgv_id,
                pan_ocr_result_id=pan_ocr_result_id,
                pan_number=pan_number,
                full_name=full_name,
                date_of_birth=dob
            )

            if not verification_result:
                raise Exception("PAN verification returned an empty response.")

            return verification_result

        except Exception as e:
            raise Exception(f"PAN Verification Service Error: {str(e)}")