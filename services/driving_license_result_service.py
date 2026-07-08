from repositories.driving_license_repository import (
    DrivingLicenseRepository
)


class DrivingLicenseResultService:

    @staticmethod
    def get_result(
            candidate_id
    ):

        ########################################
        # VALIDATION
        ########################################

        if not candidate_id:

            raise Exception(
                "Candidate ID is required"
            )

        ########################################
        # GET RESULT
        ########################################

        result = (

            DrivingLicenseRepository

            .get_driving_license_result(

                candidate_id

            )

        )

        ########################################
        # NOT FOUND
        ########################################

        if not result:

            raise Exception(

                "Driving License verification result not found"

            )

        ########################################
        # RETURN
        ########################################

        return result