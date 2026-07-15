from services.ongrid.ccrv_generate_service import (
    CCRVGenerateService
)


class CCRVVerificationService:

    ###############################################################
    # VERIFY CCRV
    ###############################################################

    @staticmethod
    def verify_ccrv(
        candidate_id,
        bgv_id
    ):

        ###########################################################
        # VALIDATIONS
        ###########################################################

        if not candidate_id:
            raise Exception(
                "Candidate ID is required."
            )

        if not bgv_id:
            raise Exception(
                "BGV ID is required."
            )

        ###########################################################
        # GENERATE CCRV REQUEST
        ###########################################################

        return (
            CCRVGenerateService.generate_report(
                candidate_id=candidate_id,
                bgv_id=bgv_id
            )
        )