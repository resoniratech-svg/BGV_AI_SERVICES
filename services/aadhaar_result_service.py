from repositories.aadhaar_repository import (
    AadhaarRepository
)


class AadhaarResultService:


    @staticmethod
    def get_result(

        candidate_id

    ):


        verification_result = (

            AadhaarRepository
            .get_aadhaar_verification_result(

                candidate_id

            )

        )


        session = (

            AadhaarRepository
            .get_aadhaar_session(

                candidate_id

            )

        )


        # =====================================
        # CONSENT SESSION NOT FOUND
        # =====================================

        if not session:

            raise Exception(

                "Aadhaar consent session not found"

            )


        session_status = (

            session.get(

                "session_status"

            )

        )


        # =====================================
        # CONSENT PENDING
        # =====================================

        if session_status == "PENDING":

            return {

                "success": False,

                "verification_status": "PENDING",

                "display_message":

                "Candidate has not completed Aadhaar consent"

            }


        # =====================================
        # CONSENT REJECTED
        # =====================================

        if session_status == "REJECTED":

            return {

                "success": False,

                "verification_status": "REJECTED",

                "display_message":

                "Candidate denied Aadhaar consent"

            }


        # =====================================
        # VERIFICATION NOT DONE
        # =====================================

        if not verification_result:

            return {

                "success": False,

                "verification_status": "NOT_VERIFIED",

                "display_message":

                "Admin has not verified Aadhaar yet"

            }


        verification_status = (

            verification_result.get(

                "verification_status"

            )

        )


        # =====================================
        # VERIFIED
        # =====================================

        if verification_status == "VERIFIED":

            return {

                "success": True,

                "verification_status": "VERIFIED",

                "display_message":

                "Aadhaar verification completed successfully"

            }


        # =====================================
        # FAILED
        # =====================================

        return {

            "success": False,

            "verification_status": verification_status,

            "display_message":

            "Aadhaar verification failed"

        }