from repositories.credit_bureau_repository import (
    CreditBureauRepository
)


class CreditBureauResultService:

    @staticmethod
    def get_result(

            candidate_id

    ):

        ####################################################
        # MAIN RESULT
        ####################################################

        credit_bureau_result = (

            CreditBureauRepository
            .get_credit_bureau_result(

                candidate_id

            )

        )

        if not credit_bureau_result:

            raise Exception(

                "Credit Bureau result not found"

            )

        ####################################################
        # RESULT ID
        ####################################################

        credit_bureau_result_id = (

            credit_bureau_result["id"]

        )

        ####################################################
        # PERSONAL INFORMATION
        ####################################################

        personal_information = (

            CreditBureauRepository
            .get_personal_information(

                credit_bureau_result_id

            )

        )

        ####################################################
        # CONTACT INFORMATION
        ####################################################

        contact_information = (

            CreditBureauRepository
            .get_contact_information(

                credit_bureau_result_id

            )

        )

        ####################################################
        # CREDIT ACCOUNTS
        ####################################################

        credit_accounts = (

            CreditBureauRepository
            .get_credit_accounts(

                credit_bureau_result_id

            )

        )

        ####################################################
        # SUMMARY
        ####################################################

        summary = (

            CreditBureauRepository
            .get_summary(

                credit_bureau_result_id

            )

        )

        ####################################################
        # SCORE FACTORS
        ####################################################

        score_factors = (

            CreditBureauRepository
            .get_score_factors(

                credit_bureau_result_id

            )

        )

        ####################################################
        # RETURN
        ####################################################

        return {

            "credit_bureau_result":

                credit_bureau_result,

            "personal_information":

                personal_information,

            "contact_information":

                contact_information,

            "summary":

                summary,

            "credit_accounts":

                credit_accounts,

            "score_factors":

                score_factors

        }