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


        name_match_status = (

            verification_result.get(

                "name_match_status"

            )

        )


        dob_match_status = (

            verification_result.get(

                "dob_match_status"

            )

        )


        gender_match_status = (

            verification_result.get(

                "gender_match_status"

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
        # FIND ALL MISMATCHES
        # =====================================

        mismatches = []


        if name_match_status == "NOT_MATCH":

            mismatches.append(

                "name"

            )


        if dob_match_status == "NOT_MATCH":

            mismatches.append(

                "date of birth"

            )


        if gender_match_status == "NOT_MATCH":

            mismatches.append(

                "gender"

            )


        # =====================================
        # BUILD MESSAGE
        # =====================================

        if len(mismatches) == 1:

            message = (

                f"Aadhaar holder {mismatches[0]} does not match"

            )


        elif len(mismatches) == 2:

            message = (

                f"Aadhaar holder "

                f"{mismatches[0]} and "

                f"{mismatches[1]} "

                f"do not match"

            )


        elif len(mismatches) == 3:

            message = (

                "Aadhaar holder "

                "name, date of birth and gender "

                "do not match"

            )


        else:

            message = (

                "Aadhaar verification failed"

            )


        return {

            "success": False,

            "verification_status": "FAILED",

            "display_message": message

        }