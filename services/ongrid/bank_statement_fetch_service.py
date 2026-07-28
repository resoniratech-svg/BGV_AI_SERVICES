import json
from repositories.bank_statement_repository import BankStatementRepository
from services.ongrid.ongrid_client import OnGridClient
from services.ongrid.bank_statement_download_service import BankStatementDownloadService


class BankStatementFetchService:

    ####################################################
    # FETCH REPORT
    ####################################################
    @staticmethod
    def fetch_report(candidate_id, bgv_id, transaction_id, request_id):

        ####################################################
        # FETCH LOG
        ####################################################
        print("=" * 80)
        print("BANK STATEMENT FETCH REPORT")
        print("Candidate ID  :", candidate_id)
        print("BGV ID        :", bgv_id)
        print("Request ID    :", request_id)
        print("Transaction ID:", transaction_id)
        print("=" * 80)

        ####################################################
        # VALIDATE TRANSACTION ID
        ####################################################
        if not transaction_id:
            raise Exception("Transaction ID is required.")

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
                f"Bank Statement request not found for transaction_id : {transaction_id}"
            )

        ####################################################
        # REQUEST LOG
        ####################################################
        print("=" * 80)
        print("REQUEST FOUND")
        print("Database ID        :", request["id"])
        print("Candidate ID       :", request["candidate_id"])
        print("BGV ID             :", request["bgv_id"])
        print("Current Status     :", request["request_status"])
        print("=" * 80)

        ####################################################
        # ALREADY COMPLETED
        ####################################################
        if request.get("request_status") == "COMPLETED":
            print("=" * 80)
            print("REPORT ALREADY FETCHED")
            print("Transaction ID :", transaction_id)
            print("=" * 80)

            return {
                "success": True,
                "message": "Bank Statement report already processed."
            }

        ####################################################
        # REQUEST HEADERS
        ####################################################
        headers = {
            "X-Transaction-ID": transaction_id
        }

        ####################################################
        # REQUEST LOG
        ####################################################
        print("=" * 80)
        print("FETCH REPORT REQUEST")
        print(json.dumps(headers, indent=4))
        print("=" * 80)

        ####################################################
        # FETCH REPORT API
        ####################################################
        response = OnGridClient.get(
            "/bank-api/bank-statement-analyzer/fetch-report",
            headers=headers
        )

        ####################################################
        # RESPONSE LOG
        ####################################################
        print("=" * 80)
        print("FETCH REPORT RESPONSE")
        print(json.dumps(response, indent=4, default=str))
        print("=" * 80)

        ####################################################
        # EMPTY RESPONSE
        ####################################################
        if not response:
            raise Exception("Empty response received from Gridlines.")

        ####################################################
        # API FAILURE
        ####################################################
        if response.get("success") is False:
            raise Exception(
                f"Gridlines Fetch Report API Error\n\nStatus :\n\n{response.get('status')}\n\nResponse :\n\n{response.get('message')}"
            )

        ####################################################
        # HTTP STATUS
        ####################################################
        if response.get("status") != 200:
            raise Exception(
                f"Gridlines Fetch Report Failed\n\nHTTP Status :\n\n{response.get('status')}\n\nResponse :\n\n{json.dumps(response, indent=4, default=str)}"
            )

        ####################################################
        # RESPONSE DATA
        ####################################################
        data = response.get("data", {})

        ####################################################
        # PROVIDER CODE & MESSAGE
        ####################################################
        provider_status_code = data.get("code")
        provider_message = data.get("message")

        ####################################################
        # RESPONSE LOG
        ####################################################
        print("=" * 80)
        print("PROVIDER STATUS")
        print("Code    :", provider_status_code)
        print("Message :", provider_message)
        print("=" * 80)

        ####################################################
        # REPORT STILL PROCESSING
        ####################################################
        if provider_status_code == "1021":
            
            # UPDATE REQUEST STATUS
            BankStatementRepository.update_request_status(
                transaction_id=transaction_id,
                request_status="PROCESSING",
                provider_status_code=provider_status_code,
                response_payload=json.dumps(response, default=str)
            )

            # PROCESSING LOG
            print("=" * 80)
            print("BANK STATEMENT REPORT STILL PROCESSING")
            print("Transaction ID      :", transaction_id)
            print("Provider Code       :", provider_status_code)
            print("Provider Message    :", provider_message)
            print("Request Status      : PROCESSING")
            print("=" * 80)

            # RETURN
            return {
                "success": True,
                "request_status": "PROCESSING",
                "provider_status_code": provider_status_code,
                "message": provider_message
            }

        ####################################################
        # REPORT READY
        ####################################################
        if provider_status_code != "1022":
            raise Exception(
                f"Unexpected response received from Gridlines.\n\nProvider Code :\n\n{provider_status_code}\n\nProvider Message :\n\n{provider_message}"
            )

        # REPORT READY LOG
        print("=" * 80)
        print("BANK STATEMENT REPORT READY")
        print("Transaction ID      :", transaction_id)
        print("Provider Code       :", provider_status_code)
        print("Provider Message    :", provider_message)
        print("=" * 80)

        ####################################################
        # REPORT LINKS
        ####################################################
        json_link = data.get("json_link")
        excel_link = data.get("excel_link")

        ####################################################
        # REPORT VALIDATION
        ####################################################
        if not json_link and not excel_link:
            raise Exception("Gridlines returned report completed but no report links were found.")

        # REPORT LINKS LOG
        print("=" * 80)
        print("REPORT LINKS")
        print("JSON  :", json_link)
        print("EXCEL :", excel_link)
        print("=" * 80)

        ####################################################
        # DOWNLOAD REPORT
        ####################################################
        download_response = BankStatementDownloadService.download_report(
            candidate_id=request["candidate_id"],
            bgv_id=request["bgv_id"],
            transaction_id=transaction_id,
            request_id=request["id"],
            fetch_response=response
        )

        # DOWNLOAD LOG
        print("=" * 80)
        print("DOWNLOAD SERVICE RESPONSE")
        print(json.dumps(download_response, indent=4, default=str))
        print("=" * 80)

        ####################################################
        # RETURN
        ####################################################
        return download_response