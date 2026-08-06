import json
import os
import requests
from datetime import datetime
from repositories.bank_statement_repository import BankStatementRepository


class BankStatementDownloadService:

    ####################################################
    # DOWNLOAD REPORT
    ####################################################
    @staticmethod
    def download_report(
        candidate_id,
        bgv_id,
        transaction_id,
        request_id,
        callback_payload=None,
        fetch_response=None
    ):
        ####################################################
        # DOWNLOAD LOG
        ####################################################
        print("=" * 80)
        print("BANK STATEMENT DOWNLOAD REPORT")
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
        print("REQUEST DETAILS")
        print("Database ID        :", request["id"])
        print("Candidate ID       :", request["candidate_id"])
        print("BGV ID             :", request["bgv_id"])
        print("Current Status     :", request["request_status"])
        print("=" * 80)

        ####################################################
        # RESULT EXISTS
        ####################################################
        existing_result = BankStatementRepository.get_result(
            request["candidate_id"],
            request["bgv_id"]
        )

        ####################################################
        # ALREADY DOWNLOADED
        ####################################################
        if existing_result:
            print("=" * 80)
            print("REPORT ALREADY EXISTS")
            print("Transaction ID :", transaction_id)
            print("=" * 80)

            return {
                "success": True,
                "message": "Bank Statement report already downloaded.",
                "request_status": "COMPLETED"
            }

        ####################################################
        # RESPONSE SOURCE
        ####################################################
        response = callback_payload if callback_payload else fetch_response

        ####################################################
        # VALIDATE RESPONSE
        ####################################################
        if not response:
            raise Exception("Report response is required.")

        ####################################################
        # DOWNLOAD START LOG
        ####################################################
        print("=" * 80)
        print("STARTING REPORT DOWNLOAD")
        print("=" * 80)

        ####################################################
        # RESPONSE DATA
        ####################################################
        response_data = response.get("data", {})

        ####################################################
        # REPORT LINKS
        ####################################################
        json_link = response_data.get("json_link")
        excel_link = response_data.get("excel_link")

        ####################################################
        # VALIDATE REPORT LINKS
        ####################################################
        if not json_link and not excel_link:
            raise Exception("No report links received from Gridlines.")

        ####################################################
        # REPORT LINKS LOG
        ####################################################
        print("=" * 80)
        print("REPORT LINKS")
        print("JSON LINK  :", json_link)
        print("EXCEL LINK :", excel_link)
        print("=" * 80)

        ####################################################
        # REPORT DIRECTORY & CREATION
        ####################################################
        report_directory = os.path.join(
            "uploads",
            f"candidate_{candidate_id}",
            "bank_statement"
        )
        os.makedirs(report_directory, exist_ok=True)

        ####################################################
        # FILE PATHS
        ####################################################
        json_file_path = os.path.join(
            report_directory,
            f"bank_statement_{transaction_id}.json"
        )
        excel_file_path = os.path.join(
            report_directory,
            f"bank_statement_{transaction_id}.xlsx"
        )

        ####################################################
        # FILE PATH LOG
        ####################################################
        print("=" * 80)
        print("DOWNLOAD LOCATION")
        print("Directory :", report_directory)
        print("JSON File :", json_file_path)
        print("Excel File:", excel_file_path)
        print("=" * 80)

        ####################################################
        # DOWNLOAD JSON REPORT
        ####################################################
        json_report = None
        if json_link:
            print("=" * 80)
            print("DOWNLOADING JSON REPORT")
            print(json_link)
            print("=" * 80)

            try:

                json_response = requests.get(

                    json_link,

                    stream=True,

                    timeout=60

                )

            except requests.exceptions.Timeout:

                raise Exception(

                    "JSON report download timed out."

                )

            except requests.exceptions.ConnectionError:

                raise Exception(

                    "Unable to connect to JSON report server."

                )

            except requests.exceptions.RequestException as error:

                raise Exception(

                    f"JSON report download failed : {error}"

                )
            if json_response.status_code != 200:
                raise Exception(
                    f"Unable to download JSON report. HTTP Status : {json_response.status_code}"
                )

            content_type = json_response.headers.get("Content-Type", "")
            if "application/json" not in content_type.lower():
                raise Exception(
                f"""
            Expected a JSON report from Gridlines.

            URL          : {json_link}
            HTTP Status  : {json_response.status_code}
            Content-Type : {content_type}

            The provider returned a non-JSON response.
            This usually means the report URL is invalid, expired, or not yet available.
            """.strip()
)

            try:
                json_report = json_response.json()
            except Exception:
                raise Exception("Downloaded JSON report is not a valid JSON document.")

            # SAVE JSON FILE
            with open(json_file_path, "wb") as file:
                for chunk in json_response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)

            json_file_size = os.path.getsize(json_file_path)
            print("=" * 80)
            print("JSON REPORT SAVED")
            print("File :", json_file_path)
            print("Size :", json_file_size, "bytes")
            print("=" * 80)

        ####################################################
        # DOWNLOAD EXCEL REPORT
        ####################################################
        if excel_link:
            print("=" * 80)
            print("DOWNLOADING EXCEL REPORT")
            print(excel_link)
            print("=" * 80)

            excel_response = requests.get(excel_link, stream=True, timeout=60)

            if excel_response.status_code != 200:
                raise Exception(
                    f"Unable to download Excel report. HTTP Status : {excel_response.status_code}"
                )

            content_type = excel_response.headers.get("Content-Type", "")
            if "text/html" in content_type.lower():
                raise Exception("Excel download returned HTML instead of an Excel file.")

            # SAVE EXCEL FILE
            with open(excel_file_path, "wb") as file:
                for chunk in excel_response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)

            excel_file_size = os.path.getsize(excel_file_path)
            print("=" * 80)
            print("EXCEL REPORT SAVED")
            print("File :", excel_file_path)
            print("Size :", excel_file_size, "bytes")
            print("=" * 80)

        ####################################################
        # SAVE RESULT
        ####################################################
        report_generated_at = datetime.now()

        result_id = BankStatementRepository.save_result(
            request_id=request["id"],
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            provider=request["provider"],
            transaction_id=transaction_id,
            provider_request_id=request["provider_request_id"],
            provider_status_code=request.get("provider_status_code"),
            provider_json_url=json_link,
            provider_excel_url=excel_link,
            json_file_path=json_file_path if json_link else None,
            excel_file_path=excel_file_path if excel_link else None,
            report_generated_at=report_generated_at
        )

        if not result_id:
            raise Exception("Unable to save Bank Statement result.")

        ####################################################
        # UPDATE REQUEST STATUS
        ####################################################
        BankStatementRepository.update_request_status(
            transaction_id=transaction_id,
            request_status="COMPLETED",
            provider_status_code=request.get("provider_status_code"),
            response_payload=json.dumps(response, default=str)
        )

        ####################################################
        # SUCCESS LOG
        ####################################################
        print("=" * 80)
        print("BANK STATEMENT DOWNLOAD COMPLETED")
        print("Result ID         :", result_id)
        print("Transaction ID    :", transaction_id)
        print("JSON File         :", json_file_path)
        print("Excel File        :", excel_file_path)
        print("Status            : COMPLETED")
        print("=" * 80)

        ####################################################
        # RETURN
        ####################################################
        return {
            "success": True,
            "message": "Bank Statement report downloaded successfully.",
            "request_status": "COMPLETED",
            "result_id": result_id,
            "transaction_id": transaction_id,
            "json_file_path": json_file_path,
            "excel_file_path": excel_file_path
        }