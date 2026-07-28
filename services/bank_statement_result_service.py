from repositories.bank_statement_repository import (
    BankStatementRepository
)


class BankStatementResultService:

    ###############################################################
    # GET BANK STATEMENT RESULT
    ###############################################################

    @staticmethod
    def get_result(

            candidate_id,
            bgv_id

    ):

        ###########################################################
        # GET RESULT
        ###########################################################

        result = (

            BankStatementRepository
            .get_result(

                candidate_id,
                bgv_id

            )

        )

        ###########################################################
        # VALIDATION
        ###########################################################

        if not result:

            raise Exception(

                "Bank Statement result not found."

            )

        ###########################################################
        # RETURN
        ###########################################################

        return result