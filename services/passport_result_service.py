from repositories.passport_repository import (
    PassportRepository
)


class PassportResultService:

    @staticmethod
    def get_result(

        candidate_id

    ):

        verification_result = (

            PassportRepository
            .get_passport_result(

                candidate_id

            )

        )

        if not verification_result:

            return {

                "success": False,

                "verification_status": "NOT_VERIFIED",

                "display_message":

                "Passport has not been verified"

            }

        verification_status = (

            verification_result.get(

                "verification_status"

            )

        )

        ####################################################
        # VERIFIED
        ####################################################

        if verification_status == "VERIFIED":

            return {

                "success": True,

                "verification_status": "VERIFIED",

                "display_message":

                "Passport verification completed successfully"

            }

        ####################################################
        # FAILED
        ####################################################

        if verification_status == "FAILED":

            return {

                "success": False,

                "verification_status": "FAILED",

                "display_message":

                "Passport verification failed"

            }

        ####################################################
        # DEFAULT
        ####################################################

        return {

            "success": False,

            "verification_status":

            verification_status,

            "display_message":

            "Passport verification incomplete"

        }