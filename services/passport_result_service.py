# from repositories.passport_repository import PassportRepository


# class PassportResultService:
#     @staticmethod
#     def get_result(candidate_id):

#         verification_result = PassportRepository.get_passport_result(candidate_id)

#         if not verification_result:
#             return {
#                 "success": False,
#                 "verification_status": "NOT_VERIFIED",
#                 "display_message": "Passport has not been verified",
#             }

#         verification_status = verification_result.get("verification_status")

#         ####################################################
#         # VERIFIED
#         ####################################################

#         if verification_status == "VERIFIED":
#             return {
#                 "success": True,
#                 "verification_status": "VERIFIED",
#                 "display_message": "Passport verification completed successfully",
#             }

#         ####################################################
#         # FAILED
#         ####################################################

#         if verification_status == "FAILED":
#             return {
#                 "success": False,
#                 "verification_status": "FAILED",
#                 "display_message": "Passport verification failed",
#             }

#         ####################################################
#         # DEFAULT
#         ####################################################

#         return {
#             "success": False,
#             "verification_status": verification_status,
#             "display_message": "Passport verification incomplete",
#         }
from repositories.passport_repository import PassportRepository


class PassportResultService:
    @staticmethod
    def get_result(candidate_id):

        # =====================================================
        # GET PASSPORT VERIFICATION RESULT
        # =====================================================

        verification_result = PassportRepository.get_passport_result(candidate_id)

        if not verification_result:
            return {
                "success": False,
                "verification_status": "NOT_VERIFIED",
                "display_message": "Passport has not been verified",
                "data": None,
            }

        # =====================================================
        # GET OCR RESULT
        # =====================================================

        passport_ocr_result = PassportRepository.get_passport_ocr_result_by_id(
            verification_result.get("passport_ocr_result_id")
        )

        verification_status = verification_result.get("verification_status")

        # =====================================================
        # RETURN COMPLETE PASSPORT RESULT
        # =====================================================

        return {
            "success": verification_status == "VERIFIED",
            "verification_status": verification_status,
            "display_message": (
                "Passport verification completed successfully"
                if verification_status == "VERIFIED"
                else "Passport verification failed"
            ),
            "data": {
                # =================================================
                # VERIFICATION RESULT
                # =================================================
                "verification": {
                    "verification_status": verification_status,
                    "passport_match_status": verification_result.get(
                        "passport_match_status"
                    ),
                    "name_match_status": verification_result.get("name_match_status"),
                    "dob_match_status": verification_result.get("dob_match_status"),
                    "provider_name": verification_result.get("provider_name"),
                    "api_reference_id": verification_result.get("api_reference_id"),
                },
                # =================================================
                # PASSPORT OCR INFORMATION
                # =================================================
                "passport_information": {
                    "id": passport_ocr_result.get("id")
                    if passport_ocr_result
                    else None,
                    "candidate_id": passport_ocr_result.get("candidate_id")
                    if passport_ocr_result
                    else verification_result.get("candidate_id"),
                    "bgv_id": passport_ocr_result.get("bgv_id")
                    if passport_ocr_result
                    else verification_result.get("bgv_id"),
                    "document_id": passport_ocr_result.get("document_id")
                    if passport_ocr_result
                    else None,
                    "passport_number": passport_ocr_result.get("passport_number")
                    if passport_ocr_result
                    else verification_result.get("passport_number"),
                    "file_number": passport_ocr_result.get("file_number")
                    if passport_ocr_result
                    else None,
                    "given_name": passport_ocr_result.get("given_name")
                    if passport_ocr_result
                    else None,
                    "surname": passport_ocr_result.get("surname")
                    if passport_ocr_result
                    else None,
                    "full_name": passport_ocr_result.get("full_name")
                    if passport_ocr_result
                    else verification_result.get("full_name"),
                    "gender": passport_ocr_result.get("gender")
                    if passport_ocr_result
                    else None,
                    "date_of_birth": passport_ocr_result.get("date_of_birth")
                    if passport_ocr_result
                    else verification_result.get("date_of_birth"),
                    "issue_date": passport_ocr_result.get("issue_date")
                    if passport_ocr_result
                    else verification_result.get("issue_date"),
                    "expiry_date": passport_ocr_result.get("expiry_date")
                    if passport_ocr_result
                    else verification_result.get("expiry_date"),
                    "nationality": passport_ocr_result.get("nationality")
                    if passport_ocr_result
                    else verification_result.get("nationality"),
                    "country": passport_ocr_result.get("country")
                    if passport_ocr_result
                    else verification_result.get("country"),
                    "guardian_name": passport_ocr_result.get("guardian_name")
                    if passport_ocr_result
                    else None,
                    "mother_name": passport_ocr_result.get("mother_name")
                    if passport_ocr_result
                    else None,
                    "place_of_birth": passport_ocr_result.get("place_of_birth")
                    if passport_ocr_result
                    else None,
                    "place_of_issue": passport_ocr_result.get("place_of_issue")
                    if passport_ocr_result
                    else None,
                    "provider_name": passport_ocr_result.get("provider_name")
                    if passport_ocr_result
                    else verification_result.get("provider_name"),
                    "api_reference_id": passport_ocr_result.get("api_reference_id")
                    if passport_ocr_result
                    else verification_result.get("api_reference_id"),
                },
            },
        }
