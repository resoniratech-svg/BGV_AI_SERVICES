import json
import base64

from repositories.document_repository import DocumentRepository

from repositories.salary_slip_repository import SalarySlipRepository

from services.ongrid.salary_slip_service import SalarySlipService


class SalarySlipOCRService:
    @staticmethod
    def verify_salary_slip(candidate_id, bgv_id, document_id):

        ####################################################
        # VALIDATIONS
        ####################################################

        if not candidate_id:
            raise Exception("Candidate ID is required.")

        if not bgv_id:
            raise Exception("BGV ID is required.")

        if not document_id:
            raise Exception("Document ID is required.")

        ####################################################
        # GET DOCUMENT
        ####################################################

        document = DocumentRepository.get_uploaded_document(document_id)

        if not document:
            raise Exception("Salary Slip document not found.")

        ####################################################
        # DOCUMENT PATH
        ####################################################

        file_path = document.get("file_path")

        if not file_path:
            raise Exception("Salary Slip file path not found.")

        ####################################################
        # READ DOCUMENT
        ####################################################

        try:
            with open(file_path, "rb") as file:
                base64_data = base64.b64encode(file.read()).decode("utf-8")

        except Exception as error:
            raise Exception(f"Unable to read Salary Slip document. {str(error)}")

        ####################################################
        # GRIDLINES OCR
        ####################################################

        response = SalarySlipService.salary_slip_ocr(base64_data)

        ####################################################
        # VALIDATION
        ####################################################

        ####################################################
        # EMPTY RESPONSE
        ####################################################

        if not response:
            raise Exception("Salary Slip OCR provider returned an empty response.")

        ####################################################
        # PROVIDER FAILURE
        ####################################################

        if response.get("success") is False:
            error_message = (
                response.get("message")
                or response.get("raw_response")
                or "Unknown provider error."
            )

            raise Exception(f"Gridlines Salary Slip OCR failed. {error_message}")

        ####################################################
        # RESPONSE DATA
        ####################################################

        data = response.get("data")

        if data is None:
            raise Exception(
                f"Gridlines did not return data.\nResponse: {json.dumps(response, indent=4)}"
            )

        ####################################################
        # OCR DATA
        ####################################################

        ocr_data = data.get("data")

        if ocr_data is None:
            raise Exception(
                f"OCR fields are missing.\nResponse: {json.dumps(response, indent=4)}"
            )

        ####################################################
        # EXTRACT FIELDS
        ####################################################

        employee_name = ocr_data.get("name")

        employee_id = ocr_data.get("employee_id")

        pan_number = ocr_data.get("pan_number")

        uan_number = ocr_data.get("uan_number")

        bank_account_number = ocr_data.get("bank_account_number")

        pf_number = ocr_data.get("pf_number")

        grade = ocr_data.get("grade")

        designation = ocr_data.get("designation")

        company_business_name = ocr_data.get("company_business_name")

        office_state = ocr_data.get("office_state")

        office_address = ocr_data.get("office_address")

        joining_date = ocr_data.get("joining_date")

        payslip_date = ocr_data.get("payslip_date")

        pf_amount = ocr_data.get("pf_amount")

        net_pay = ocr_data.get("net_pay")

        provider_name = "GRIDLINES"

        api_reference_id = response.get("request_id")

        raw_response = json.dumps(response)

        ####################################################
        # SAVE OCR RESULT
        ####################################################

        salary_slip_result_id = SalarySlipRepository.save_salary_slip_ocr_result(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            document_id=document_id,
            employee_name=employee_name,
            employee_id=employee_id,
            pan_number=pan_number,
            uan_number=uan_number,
            bank_account_number=bank_account_number,
            pf_number=pf_number,
            grade=grade,
            designation=designation,
            company_business_name=company_business_name,
            office_state=office_state,
            office_address=office_address,
            joining_date=joining_date,
            payslip_date=payslip_date,
            pf_amount=pf_amount,
            net_pay=net_pay,
            provider_name=provider_name,
            api_reference_id=api_reference_id,
            raw_response=raw_response,
        )

        ####################################################
        # SUCCESS RESPONSE
        ####################################################

        return {
            "success": True,
            "message": "Salary Slip OCR completed successfully.",
            "salary_slip_ocr_result_id": salary_slip_result_id,
            "request_id": response.get("request_id"),
            "transaction_id": response.get("transaction_id"),
            "candidate_id": candidate_id,
            "bgv_id": bgv_id,
            "employee_name": employee_name,
            "employee_id": employee_id,
            "pan_number": pan_number,
            "uan_number": uan_number,
            "bank_account_number": bank_account_number,
            "pf_number": pf_number,
            "designation": designation,
            "grade": grade,
            "company_business_name": company_business_name,
            "office_state": office_state,
            "office_address": office_address,
            "joining_date": joining_date,
            "payslip_date": payslip_date,
            "pf_amount": pf_amount,
            "net_pay": net_pay,
        }
