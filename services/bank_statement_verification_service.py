from services.ongrid.bank_statement_service import (
    BankStatementService
)

from services.ongrid.bank_statement_callback_service import (
    BankStatementCallbackService
)


class BankStatementVerificationService:

    ###############################################################
    # UPLOAD BANK STATEMENT
    ###############################################################

    @staticmethod
    def upload_bank_statement(

            candidate_id,
            bgv_id,
            bank_name=None,
            bank_statement_password=None

    ):

        ###########################################################
        # CALL GRIDLINES BANK STATEMENT SERVICE
        ###########################################################

        result = (

            BankStatementService
            .upload_bank_statement(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                bank_name=bank_name,

                bank_statement_password=bank_statement_password

            )

        )

        ###########################################################
        # RETURN
        ###########################################################

        return result

    ###############################################################
    # PROCESS CALLBACK
    ###############################################################

    @staticmethod
    def process_callback(

            callback_payload

    ):

        ###########################################################
        # CALL CALLBACK SERVICE
        ###########################################################

        result = (

            BankStatementCallbackService
            .process_callback(

                callback_payload

            )

        )

        ###########################################################
        # RETURN
        ###########################################################

        return result