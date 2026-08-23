from repositories.ccrv_repository import CCRVRepository

from services.ongrid.ccrv_fetch_service import CCRVFetchService


class CCRVCallbackService:
    @staticmethod
    def process_callback(payload):

        ###########################################################
        # VALIDATE CALLBACK PAYLOAD
        ###########################################################

        if not payload:
            raise Exception("Gridlines callback payload is empty.")

        ###########################################################
        # EXTRACT VALUES
        ###########################################################

        transaction_id = payload.get("transaction_id")

        request_id = payload.get("request_id")

        verification_status = payload.get("status")

        ###########################################################
        # LOG CALLBACK
        ###########################################################

        print("=" * 80)
        print("CCRV CALLBACK RECEIVED")
        print("Transaction ID :", transaction_id)
        print("Request ID     :", request_id)
        print("Status         :", verification_status)
        print("=" * 80)

        ###########################################################
        # VALIDATION
        ###########################################################

        if not transaction_id:
            raise Exception("Gridlines callback does not contain a transaction_id.")

        ###########################################################
        # FIND ORIGINAL REQUEST
        ###########################################################

        request = CCRVRepository.get_request_by_transaction_id(transaction_id)

        if not request:
            raise Exception(
                f"No CCRV request found for Transaction ID '{transaction_id}'."
            )

        ###########################################################
        # IDEMPOTENT CHECK
        # Ignore duplicate callbacks
        ###########################################################

        if CCRVRepository.result_exists(request["id"]):
            print("=" * 80)
            print("DUPLICATE CALLBACK RECEIVED")
            print("Transaction :", transaction_id)
            print("Report already processed.")
            print("=" * 80)

            return {
                "success": True,
                "transaction_id": transaction_id,
                "message": "Duplicate callback ignored. CCRV report has already been processed.",
            }

        ###########################################################
        # FAILED CALLBACK
        ###########################################################

        if verification_status == "FAILED":
            CCRVRepository.update_request_failed(
                transaction_id=transaction_id, raw_response=str(payload)
            )

            return {
                "success": False,
                "transaction_id": transaction_id,
                "status": "FAILED",
                "message": "Gridlines completed the CCRV verification with FAILED status.",
            }

        ###########################################################
        # STILL PROCESSING
        ###########################################################

        if verification_status in ("REQUESTED", "IN_PROGRESS"):
            CCRVRepository.update_request_status(
                transaction_id=transaction_id,
                ccrv_status=verification_status,
                raw_response=str(payload),
            )

            return {
                "success": True,
                "transaction_id": transaction_id,
                "status": verification_status,
                "message": f"Gridlines reports the CCRV request is currently '{verification_status}'.",
            }

        ###########################################################
        # COMPLETED
        ###########################################################

        if verification_status != "COMPLETED":
            raise Exception(f"Unknown callback status : {verification_status}")

        ###########################################################
        # FETCH FINAL REPORT
        ###########################################################

        print("=" * 80)
        print("CALLING FETCH REPORT")
        print("Transaction :", transaction_id)
        print("=" * 80)

        result = CCRVFetchService.fetch_report(transaction_id)

        ###########################################################
        # RESPONSE
        ###########################################################

        return {
            "success": True,
            "message": "CCRV callback processed successfully.",
            "data": result,
        }
