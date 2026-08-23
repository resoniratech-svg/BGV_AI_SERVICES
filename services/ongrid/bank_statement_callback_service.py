import json

from repositories.bank_statement_repository import BankStatementRepository

from services.ongrid.bank_statement_fetch_service import BankStatementFetchService


class BankStatementCallbackService:
    ####################################################
    # PROCESS CALLBACK
    ####################################################

    @staticmethod
    def process_callback(callback_payload):

        transaction_id = None
        provider_status_code = None

        try:
            ####################################################
            # CALLBACK LOG
            ####################################################

            print("=" * 80)
            print("BANK STATEMENT CALLBACK RECEIVED")
            print(json.dumps(callback_payload, indent=4, default=str))
            print("=" * 80)

            ####################################################
            # VALIDATE CALLBACK
            ####################################################

            if not callback_payload:
                raise Exception("Empty callback payload received.")

            ####################################################
            # TRANSACTION ID
            ####################################################

            transaction_id = callback_payload.get(
                "transaction_id"
            ) or callback_payload.get("data", {}).get("transaction_id")

            if not transaction_id:
                raise Exception("transaction_id not found in callback payload.")

            ####################################################
            # REQUEST DETAILS
            ####################################################

            request = BankStatementRepository.get_request_by_transaction_id(
                transaction_id
            )

            ####################################################
            # REQUEST EXISTS
            ####################################################

            if not request:
                raise Exception(
                    f"No Bank Statement request found for transaction_id : {transaction_id}"
                )

            ####################################################
            # REQUEST LOG
            ####################################################

            print("=" * 80)
            print("BANK STATEMENT REQUEST FOUND")
            print("Request ID      :", request["id"])
            print("Candidate ID    :", request["candidate_id"])
            print("BGV ID          :", request["bgv_id"])
            print("Transaction ID  :", transaction_id)
            print("Current Status  :", request["request_status"])
            print("=" * 80)

            ####################################################
            # IDEMPOTENCY CHECK
            ####################################################

            if request.get("request_status") == "COMPLETED":
                print("=" * 80)
                print("CALLBACK ALREADY PROCESSED")
                print("Transaction ID :", transaction_id)
                print("=" * 80)

                return {"success": True, "message": "Callback already processed."}

            ####################################################
            # CALLBACK DATA
            ####################################################

            callback_data = callback_payload.get("data", {})

            ####################################################
            # PROVIDER STATUS CODE
            ####################################################

            provider_status_code = callback_data.get("code")

            ####################################################
            # PROVIDER MESSAGE
            ####################################################

            provider_message = callback_data.get("message")

            ####################################################
            # REQUEST STATUS
            ####################################################

            if provider_status_code == "200":
                request_status = "PROCESSING"

            else:
                request_status = "FAILED"

            ####################################################
            # UPDATE REQUEST
            ####################################################

            BankStatementRepository.update_request_status(
                transaction_id=transaction_id,
                request_status=request_status,
                provider_status_code=provider_status_code,
                response_payload=json.dumps(callback_payload, default=str),
            )

            ####################################################
            # UPDATE LOG
            ####################################################

            print("=" * 80)
            print("BANK STATEMENT REQUEST UPDATED")
            print("Transaction ID      :", transaction_id)
            print("Provider Code       :", provider_status_code)
            print("Provider Message    :", provider_message)
            print("Request Status      :", request_status)
            print("=" * 80)

            ####################################################
            # CALLBACK NOTIFICATION RECEIVED
            ####################################################

            print("=" * 80)
            print("CALLBACK NOTIFICATION RECEIVED")
            print("CALLING FETCH REPORT API")
            print("Transaction ID :", transaction_id)
            print("=" * 80)

            ####################################################
            # CALLBACK FAILED
            ####################################################

            if request_status == "FAILED":
                return {
                    "success": False,
                    "message": provider_message or "Provider processing failed.",
                }

            ####################################################
            # FETCH REPORT
            ####################################################

            return BankStatementFetchService.fetch_report(
                candidate_id=request["candidate_id"],
                bgv_id=request["bgv_id"],
                transaction_id=transaction_id,
                request_id=request["id"],
            )

        ####################################################
        # EXCEPTION
        ####################################################

        except Exception as exception:
            ####################################################
            # ERROR LOG
            ####################################################

            print("=" * 80)
            print("BANK STATEMENT CALLBACK ERROR")
            print(str(exception))
            print("=" * 80)

            ####################################################
            # UPDATE REQUEST STATUS
            ####################################################

            try:
                if transaction_id:
                    BankStatementRepository.update_request_status(
                        transaction_id=transaction_id,
                        request_status="FAILED",
                        provider_status_code=provider_status_code,
                        response_payload=json.dumps(callback_payload, default=str),
                    )

            except Exception as update_exception:
                print("=" * 80)
                print("FAILED TO UPDATE REQUEST STATUS")
                print(str(update_exception))
                print("=" * 80)

            ####################################################
            # RAISE
            ####################################################

            raise
