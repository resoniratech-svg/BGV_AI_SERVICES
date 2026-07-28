import json
import os
from config import Config
from datetime import datetime

from services.ongrid.ongrid_client import OnGridClient
from repositories.bank_statement_repository import BankStatementRepository


class BankStatementService:

    ####################################################
    # UPLOAD BANK STATEMENT
    ####################################################
    @staticmethod
    def upload_bank_statement(
        candidate_id,
        bgv_id,
        bank_name=None,
        bank_statement_password=None
    ):
        ####################################################
        # UPLOADED BANK STATEMENT
        ####################################################
        document = BankStatementRepository.get_uploaded_bank_statement(
            candidate_id,
            bgv_id
        )

        if not document:
            raise Exception("Uploaded Bank Statement not found.")

        ####################################################
        # DOCUMENT PATH
        ####################################################
        document_path = document.get("file_path")

        if not document_path:
            raise Exception("Bank Statement file path not found.")

        ####################################################
        # FILE EXISTS
        ####################################################
        if not os.path.exists(document_path):
            raise Exception(f"Bank Statement file does not exist: {document_path}")

        ####################################################
        # FILE SIZE
        ####################################################
        file_size = os.path.getsize(document_path)

        ####################################################
        # MAX FILE SIZE (20 MB)
        ####################################################
        if file_size > (20 * 1024 * 1024):
            raise Exception("Bank Statement exceeds maximum allowed size of 20 MB.")

        ####################################################
        # PDF VALIDATION
        ####################################################
        extension = os.path.splitext(document_path)[1].lower()

        if extension != ".pdf":
            raise Exception("Only PDF Bank Statements are supported.")

        ####################################################
        # CONSENT
        ####################################################
        consent = BankStatementRepository.get_bank_statement_consent(
            candidate_id,
            bgv_id
        )

        if not consent:
            raise Exception("Bank Statement consent not found.")

        ####################################################
        # CONSENT STATUS
        ####################################################
        if consent.get("consent_status") != "GIVEN":
            raise Exception("Candidate has not provided Bank Statement consent.")

        ####################################################
        # LOG
        ####################################################
        print("=" * 80)
        print("BANK STATEMENT UPLOAD")
        print("Candidate ID :", candidate_id)
        print("BGV ID       :", bgv_id)
        print("Document ID  :", document["id"])
        print("File         :", document_path)
        print("Bank Name    :", bank_name)
        print(f"Password     : {bank_statement_password}")
        print("=" * 80)

        ####################################################
        # MULTIPART FILE & UPLOAD
        ####################################################
        with open(document_path, "rb") as statement_file:
            files = {
                "file": (
                    document.get("original_filename"),
                    statement_file,
                    "application/pdf"
                )
            }

            data = {
                "consent": "Y"
            }

            if bank_name:
                data["bank_name"] = bank_name

            if bank_statement_password:
                data["password"] = bank_statement_password

            print("=" * 80)
            print("BANK STATEMENT REQUEST DATA")
            print(json.dumps(data, indent=4))
            print("=" * 80)

            response = OnGridClient.post_multipart(
                "/bank-api/bank-statement-analyzer/upload",
                files,
                data
            )

        ####################################################
        # RESPONSE LOG
        ####################################################
        print("=" * 80)
        print("BANK STATEMENT RESPONSE")
        print(json.dumps(response, indent=4, default=str))
        print("=" * 80)

        ####################################################
        # EMPTY RESPONSE
        ####################################################
        if not response:
            raise Exception("Empty response received from Gridlines.")

        ####################################################
        # API STATUS
        ####################################################
        if response.get("success") is False:
            status = response.get("status")
            message = response.get("message")
            raise Exception(
                f"Gridlines Bank Statement Upload API Error\n\nStatus :\n\n{status}\n\nResponse :\n\n{message}"
            )

        ####################################################
        # HTTP STATUS
        ####################################################
        if response.get("status") != 200:
            raise Exception(
                f"Gridlines Bank Statement Upload Failed\n\nHTTP Status :\n\n{response.get('status')}\n\nResponse :\n\n{json.dumps(response, indent=4, default=str)}"
            )

        ####################################################
        # RESPONSE DATA
        ####################################################
        data_payload = response.get("data", {})

        ####################################################
        # GRIDLINES RESPONSE CODE
        ####################################################
        if data_payload.get("code") != "1019":
            raise Exception(data_payload.get("message", "Bank Statement Upload failed."))

        ####################################################
        # TRANSACTION & REQUEST ID
        ####################################################
        transaction_id = response.get("transaction_id")
        if not transaction_id:
            raise Exception("Gridlines did not return transaction_id.")

        request_id = response.get("request_id")
        if not request_id:
            raise Exception("Gridlines did not return request_id.")

        ####################################################
        # SUCCESS LOG
        ####################################################
        print("=" * 80)
        print("BANK STATEMENT UPLOAD SUCCESS")
        print("Transaction ID :", transaction_id)
        print("Request ID     :", request_id)
        print("Provider Code  :", data_payload.get("code"))
        print("Message        :", data_payload.get("message"))
        print("=" * 80)

        ####################################################
        # SAVE REQUEST
        ####################################################
        payload = {
            "bank_name": bank_name,
            "password": bank_statement_password,
            "consent": "Y",
            "callback_url": Config.BANK_STATEMENT_CALLBACK_URL
        }

        request_status = "PROCESSING"
        provider_status_code = data_payload.get("code")

        bank_statement_request_id = BankStatementRepository.save_request(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            document_id=document["id"],
            provider="GRIDLINES",
            transaction_id=transaction_id,
            provider_request_id=request_id,
            request_status=request_status,
            provider_status_code=provider_status_code,
            request_payload=json.dumps(payload, default=str),
            response_payload=json.dumps(response, default=str)
        )

        if not bank_statement_request_id:
            raise Exception("Unable to save Bank Statement request.")

        ####################################################
        # SUCCESS LOG
        ####################################################
        print("=" * 80)
        print("BANK STATEMENT REQUEST SAVED")
        print("Request ID            :", bank_statement_request_id)
        print("Candidate ID          :", candidate_id)
        print("BGV ID                :", bgv_id)
        print("Transaction ID        :", transaction_id)
        print("Provider Request ID   :", request_id)
        print("Status                :", request_status)
        print("=" * 80)

        ####################################################
        # RETURN
        ####################################################
        return {
            "success": True,
            "message": "Bank Statement uploaded successfully. Report generation is in progress.",
            "bank_statement_request_id": bank_statement_request_id,
            "transaction_id": transaction_id,
            "request_id": request_id,
            "provider_status_code": provider_status_code,
            "request_status": request_status
        }