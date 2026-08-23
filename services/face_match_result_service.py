# from repositories.face_match_repository import FaceMatchRepository


# class FaceMatchResultService:
#     @staticmethod
#     def get_result(candidate_id):

#         result = FaceMatchRepository.get_result(candidate_id)

#         if not result:
#             return {
#                 "success": False,
#                 "verification_status": "NOT_VERIFIED",
#                 "display_message": "Face Match has not been performed",
#             }

#         verification_status = result.get("verification_status")

#         confidence_score = result.get("confidence_score")

#         if verification_status == "MATCH":
#             return {
#                 "success": True,
#                 "verification_status": "MATCH",
#                 "confidence_score": confidence_score,
#                 "display_message": "Face Match completed successfully",
#             }

#         return {
#             "success": False,
#             "verification_status": "NOT_MATCH",
#             "confidence_score": confidence_score,
#             "display_message": "Face does not match Aadhaar image",
#         }
from repositories.face_match_repository import FaceMatchRepository
from repositories.aadhaar_repository import AadhaarRepository


class FaceMatchResultService:
    @staticmethod
    def get_result(candidate_id):

        # =====================================================
        # GET FACE MATCH RESULT
        # =====================================================

        result = FaceMatchRepository.get_result(candidate_id)

        if not result:
            return {
                "success": False,
                "verification_status": "NOT_VERIFIED",
                "confidence_score": None,
                "resident_image": None,
                "document_id": None,
                "display_message": "Face Match has not been performed",
            }

        verification_status = result.get("verification_status")
        confidence_score = result.get("confidence_score")
        document_id = result.get("document_id")

        # =====================================================
        # GET ACTUAL AADHAAR RESIDENT IMAGE
        #
        # This comes from:
        # aadhaar_verification_results.resident_image
        #
        # It is NOT the uploaded Aadhaar card document.
        # =====================================================

        aadhaar = AadhaarRepository.get_aadhaar_verification_result(candidate_id)

        resident_image = None

        if aadhaar:
            resident_image = aadhaar.get("resident_image")

        # =====================================================
        # MATCH
        # =====================================================

        if verification_status == "MATCH":
            return {
                "success": True,
                "verification_status": "MATCH",
                "confidence_score": confidence_score,
                "resident_image": resident_image,
                "document_id": document_id,
                "display_message": "Face Match completed successfully",
            }

        # =====================================================
        # NOT MATCH
        # =====================================================

        return {
            "success": False,
            "verification_status": "NOT_MATCH",
            "confidence_score": confidence_score,
            "resident_image": resident_image,
            "document_id": document_id,
            "display_message": "Face does not match Aadhaar image",
        }
