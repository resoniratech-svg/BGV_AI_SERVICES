from repositories.pan_repository import PanRepository


class PANResultService:
    @staticmethod
    def get_result(candidate_id):

        verification_result = PanRepository.get_pan_verification_result(candidate_id)

        ocr_result = PanRepository.get_pan_ocr_result(candidate_id)

        if not verification_result:
            return {
                "success": False,
                "verification_status": "NOT_VERIFIED",
                "display_message": "Admin has not verified PAN yet",
            }

        verification_status = verification_result.get("verification_status")

        pan_match_status = verification_result.get("pan_match_status")

        name_match_status = verification_result.get("name_match_status")

        dob_match_status = verification_result.get("dob_match_status")

        if verification_status == "VERIFIED":
            return {
                "success": True,
                "verification_status": "VERIFIED",
                "display_message": "PAN verification completed successfully",
                "ocr_result": ocr_result,
                "verification_result": verification_result,
            }

        if (
            pan_match_status == "NOT_MATCH"
            and name_match_status == "MATCH"
            and dob_match_status == "MATCH"
        ):
            return {
                "success": False,
                "verification_status": "FAILED",
                "display_message": "PAN verification failed",
                "ocr_result": ocr_result,
                "verification_result": verification_result,
            }

        if (
            pan_match_status == "MATCH"
            and name_match_status == "NOT_MATCH"
            and dob_match_status == "MATCH"
        ):
            return {
                "success": False,
                "verification_status": "FAILED",
                "display_message": "PAN holder name does not match",
            }

        if (
            pan_match_status == "MATCH"
            and name_match_status == "MATCH"
            and dob_match_status == "NOT_MATCH"
        ):
            return {
                "success": False,
                "verification_status": "FAILED",
                "display_message": "PAN holder DOB does not match",
            }

        return {
            "success": False,
            "verification_status": "FAILED",
            "display_message": "PAN verification failed",
        }
