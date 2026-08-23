import json

from repositories.aadhaar_repository import AadhaarRepository


class AadhaarResultService:
    @staticmethod
    def save_result(
        candidate_id,
        bgv_id,
        aadhaar_data,
    ):

        print("=" * 80)
        print("PROCESSING GRIDLINES AADHAAR RESULT")
        print("CANDIDATE ID:", candidate_id)
        print("BGV ID:", bgv_id)
        print("=" * 80)

        # ==================================================
        # NORMALIZE GRIDLINES RESPONSE
        # ==================================================

        # Actual SDK response shown in your console is:
        #
        # {
        #     resident_name: "...",
        #     dob: "...",
        #     gender: "...",
        #     address: "...",
        #     resident_image: "...",
        #     ...
        # }

        if isinstance(aadhaar_data, dict):
            # Direct SDK object
            data = aadhaar_data.get("data")

            if isinstance(data, dict):
                source = data
            else:
                source = aadhaar_data

        else:
            raise Exception("Invalid Aadhaar data format")

        # ==================================================
        # EXTRACT VALUES
        # ==================================================

        resident_name = source.get("resident_name") or ""
        date_of_birth = source.get("dob") or ""
        gender = source.get("gender") or ""
        address = source.get("address") or ""
        resident_image = source.get("resident_image") or ""

        # ==================================================
        # VALIDATION
        # ==================================================

        if not resident_name:
            raise Exception("resident_name not received from Gridlines")

        if not date_of_birth:
            raise Exception("dob not received from Gridlines")

        if not gender:
            raise Exception("gender not received from Gridlines")

        # ==================================================
        # SAVE RESULT
        # ==================================================

        verification_result_id = AadhaarRepository.save_aadhaar_verification_result(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            verification_status="VERIFIED",
            resident_name=resident_name,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            resident_image=resident_image,
            provider_name="GRIDLINES",
            api_reference_id=(
                aadhaar_data.get("request_id")
                if isinstance(aadhaar_data, dict)
                else None
            ),
            raw_response=json.dumps(
                aadhaar_data,
                default=str,
            ),
        )

        print("=" * 80)
        print("AADHAAR RESULT SAVED")
        print("RESULT ID:", verification_result_id)
        print("=" * 80)

        return {
            "success": True,
            "verification_status": "VERIFIED",
            "message": "Aadhaar verification result saved successfully",
            "verification_result_id": verification_result_id,
        }

    @staticmethod
    def get_result(candidate_id):

        verification_result = AadhaarRepository.get_aadhaar_verification_result(
            candidate_id
        )

        if verification_result:
            verification_status = verification_result.get("verification_status")

            if verification_status == "VERIFIED":
                return {
                    "success": True,
                    "verification_status": "VERIFIED",
                    "display_message": ("Aadhaar verification completed successfully"),
                    "data": verification_result,
                }

            return {
                "success": False,
                "verification_status": verification_status,
                "display_message": ("Aadhaar verification failed"),
                "data": verification_result,
            }

        return {
            "success": False,
            "verification_status": "PENDING",
            "display_message": ("Aadhaar verification result is not available yet"),
        }

    # @staticmethod
    # def get_result(candidate_id):

    #     verification_result = AadhaarRepository.get_aadhaar_verification_result(
    #         candidate_id
    #     )

    #     session = AadhaarRepository.get_aadhaar_session(candidate_id)

    #     # =====================================
    #     # CONSENT SESSION NOT FOUND
    #     # =====================================

    #     if not session:
    #         raise Exception("Aadhaar consent session not found")

    #     session_status = session.get("session_status")

    #     # =====================================
    #     # CONSENT PENDING
    #     # =====================================

    #     if session_status == "PENDING":
    #         return {
    #             "success": False,
    #             "verification_status": "PENDING",
    #             "display_message": "Candidate has not completed Aadhaar consent",
    #         }

    #     # =====================================
    #     # CONSENT REJECTED
    #     # =====================================

    #     if session_status == "REJECTED":
    #         return {
    #             "success": False,
    #             "verification_status": "REJECTED",
    #             "display_message": "Candidate denied Aadhaar consent",
    #         }

    #     # =====================================
    #     # VERIFICATION NOT DONE
    #     # =====================================

    #     if not verification_result:
    #         return {
    #             "success": False,
    #             "verification_status": "NOT_VERIFIED",
    #             "display_message": "Admin has not verified Aadhaar yet",
    #         }

    #     verification_status = verification_result.get("verification_status")

    #     # =====================================
    #     # VERIFIED
    #     # =====================================

    #     if verification_status == "VERIFIED":
    #         return {
    #             "success": True,
    #             "verification_status": "VERIFIED",
    #             "display_message": "Aadhaar verification completed successfully",
    #         }

    #     # =====================================
    #     # FAILED
    #     # =====================================

    #     return {
    #         "success": False,
    #         "verification_status": verification_status,
    #         "display_message": "Aadhaar verification failed",
    #     }
