from repositories.employment_repository import EmploymentRepository


class EmploymentResultService:
    ###############################################################
    # GET EMPLOYMENT RESULT
    ###############################################################

    @staticmethod
    def get_result(candidate_id):

        ###########################################################
        # GET EMPLOYMENT RESULT
        ###########################################################

        result = EmploymentRepository.get_result(candidate_id)

        if not result:
            raise Exception(
                f"Employment Verification result not found for Candidate ID: {candidate_id}."
            )

        ###########################################################
        # GET EMPLOYMENT HISTORY
        ###########################################################

        history = EmploymentRepository.get_history(result["id"])

        ###########################################################
        # GET EMPLOYER DETAILS
        ###########################################################

        employer = EmploymentRepository.get_employer_details(result["id"])

        ###########################################################
        # RETURN
        ###########################################################

        return {
            "success": True,
            "employment_result": result,
            "employment_history": history,
            "employer_details": employer,
        }
