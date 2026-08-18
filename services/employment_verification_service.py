from services.ongrid.employment_service import EmploymentService


class EmploymentVerificationService:
    ###############################################################
    # VERIFY EMPLOYMENT
    ###############################################################

    @staticmethod
    def verify_employment(candidate_id, bgv_id, mobile_number):

        ###########################################################
        # CALL GRIDLINES EMPLOYMENT SERVICE
        ###########################################################

        result = EmploymentService.verify_employment(
            candidate_id=candidate_id, bgv_id=bgv_id, mobile_number=mobile_number
        )

        ###########################################################
        # RETURN
        ###########################################################

        return result
