from repositories.face_match_repository import FaceMatchRepository


class FaceMatchResultService:
    @staticmethod
    def get_result(candidate_id):

        result = FaceMatchRepository.get_result(candidate_id)

        if not result:
            return {
                "success": False,
                "verification_status": "NOT_VERIFIED",
                "display_message": "Face Match has not been performed",
            }

        verification_status = result.get("verification_status")

        confidence_score = result.get("confidence_score")

        if verification_status == "MATCH":
            return {
                "success": True,
                "verification_status": "MATCH",
                "confidence_score": confidence_score,
                "display_message": "Face Match completed successfully",
            }

        return {
            "success": False,
            "verification_status": "NOT_MATCH",
            "confidence_score": confidence_score,
            "display_message": "Face does not match Aadhaar image",
        }
