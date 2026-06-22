import os
import re
import json

from utils.ocr_utils import OCRUtils
from utils.image_preprocessing import ImagePreprocessing
from repositories.salary_slip_repository import SalarySlipRepository
from repositories.verification_repository import VerificationRepository
from services.verification_service import VerificationService


class SalarySlipService:
    @staticmethod
    def verify_salary_slip(file_path, candidate_id):

        try:
            # ==========================================
            # CREATE VERIFICATION SESSION
            # ==========================================

            verification_id = VerificationRepository.create_verification_request(
                candidate_id, "SALARY_SLIP", "Tesseract OCR"
            )

            # ==========================================
            # SAVE DOCUMENT ENTRY
            # ==========================================

            stored_filename = os.path.basename(file_path)

            SalarySlipRepository.save_salary_slip_document(
                candidate_id=candidate_id,
                verification_id=verification_id,
                original_file_name=stored_filename,
                stored_file_name=stored_filename,
                file_path=file_path,
                file_size=os.path.getsize(file_path),
                mime_type="application/octet-stream",
                upload_status="UPLOADED",
            )

            # ==========================================
            # IMAGE PREPROCESSING
            # ==========================================

            file_extension = os.path.splitext(file_path)[1].lower()

            if file_extension in [".png", ".jpg", ".jpeg"]:
                file_path = ImagePreprocessing.preprocess_image(file_path)

            # ==========================================
            # OCR EXTRACTION
            # ==========================================

            raw_text = OCRUtils.extract_text(file_path)
            print("\n===== SALARY OCR OUTPUT =====\n")
            print(raw_text)
            print("\n=============================\n")

            # ==========================================
            # EMPTY OCR CHECK
            # ==========================================

            if not raw_text.strip():
                VerificationRepository.update_verification_status(
                    verification_id, "FAILED"
                )

                return {
                    "success": False,
                    "message": "No text extracted from salary slip",
                }

            # ==========================================
            # PAN EXTRACTION
            # ==========================================

            pan_match = re.search(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", raw_text, re.IGNORECASE)

            pan_number = pan_match.group(0).upper() if pan_match else None

            # ==========================================
            # UAN EXTRACTION
            # ==========================================

            uan_number = None

            uan_patterns = [
                r"UAN\s*Number\s*[:\-]?\s*(\d{12})",
                r"UAN\s*[:\-]?\s*(\d{12})",
                r"\b(\d{12})\b",
            ]

            for pattern in uan_patterns:
                match = re.search(pattern, raw_text, re.IGNORECASE)

                if match:
                    uan_number = match.group(1)
                    break

            # ==========================================
            # NET SALARY EXTRACTION
            # ==========================================

            salary_amount = None

            salary_patterns = [
                r"Net Salary\s*[:\-]?\s*([\d,]+)",
                r"Net Pay\s*[:\-]?\s*([\d,]+)",
                r"Take Home\s*[:\-]?\s*([\d,]+)",
                r"Salary\s*[:\-]?\s*([\d,]+)",
            ]

            for pattern in salary_patterns:
                match = re.search(pattern, raw_text, re.IGNORECASE)

                if match:
                    salary_amount = match.group(1).replace(",", "").strip()
                    break

            net_salary = salary_amount

            # ==========================================
            # GROSS SALARY EXTRACTION
            # ==========================================

            gross_salary = None

            gross_salary_patterns = [
                r"Gross Salary\s*[:\-]?\s*([\d,]+)",
                r"Gross Pay\s*[:\-]?\s*([\d,]+)",
                r"Gross Earnings\s*[:\-]?\s*([\d,]+)",
            ]

            for pattern in gross_salary_patterns:
                match = re.search(pattern, raw_text, re.IGNORECASE)

                if match:
                    gross_salary = match.group(1).replace(",", "").strip()
                    break

            # ==========================================
            # EMPLOYEE NAME EXTRACTION
            # ==========================================

            employee_name = None

            employee_patterns = [
                r"Employee Name\s*[:\-]?\s*([A-Za-z ]+)",
                r"Name\s*[:\-]?\s*([A-Za-z ]+)",
                r"Employee\s*[:\-]?\s*([A-Za-z ]+)",
            ]

            for pattern in employee_patterns:
                match = re.search(pattern, raw_text, re.IGNORECASE)

                if match:
                    employee_name = match.group(1).strip().split("\n")[0]
                    break

            # ==========================================
            # EMPLOYEE ID EXTRACTION
            # ==========================================

            employee_id = None

            employee_id_patterns = [
                r"Employee\s*ID\s*[:\-]?\s*([A-Z0-9]+)",
                r"Emp\s*ID\s*[:\-]?\s*([A-Z0-9]+)",
            ]

            for pattern in employee_id_patterns:
                match = re.search(pattern, raw_text, re.IGNORECASE)

                if match:
                    employee_id = match.group(1).strip()
                    print("EMPLOYEE ID =", employee_id)
                    break

            # ==========================================
            # DESIGNATION EXTRACTION
            # ==========================================

            designation = None

            designation_patterns = [
                r"Designation\s*[:\-]?\s*(.+)",
                r"Role\s*[:\-]?\s*(.+)",
                r"Position\s*[:\-]?\s*(.+)",
            ]

            for pattern in designation_patterns:
                match = re.search(pattern, raw_text, re.IGNORECASE)

                if match:
                    designation = match.group(1).strip().split("\n")[0]
                    break

            # ==========================================
            # BANK ACCOUNT EXTRACTION
            # ==========================================

            bank_account_last4 = None

            bank_patterns = [
                r"Bank Account\s*([A-ZXx\d]+)",
                r"Account Number\s*([A-ZXx\d]+)",
                r"A/C Number\s*([A-ZXx\d]+)",
            ]

            for pattern in bank_patterns:
                match = re.search(pattern, raw_text, re.IGNORECASE)

                if match:
                    account_text = match.group(1)
                    digits = re.findall(r"\d", account_text)

                    if len(digits) >= 4:
                        bank_account_last4 = "".join(digits[-4:])
                    break

            # ==========================================
            # FRAUD CHECKS
            # ==========================================

            fraud_flags = []
            fraud_score = 0.00

            if not pan_number:
                fraud_flags.append("PAN_NOT_FOUND")
                fraud_score += 0.25

            if not salary_amount:
                fraud_flags.append("SALARY_NOT_FOUND")
                fraud_score += 0.25

            if not employee_name:
                fraud_flags.append("EMPLOYEE_NAME_NOT_FOUND")
                fraud_score += 0.10

            # ==========================================
            # STATIC VALUES
            # ==========================================

            document_type = "SALARY_SLIP"
            extraction_status = "SUCCESS"

            # ==========================================
            # SAVE RESULT
            # ==========================================

            salary_slip_id = SalarySlipRepository.save_salary_slip_result(
                candidate_id=candidate_id,
                verification_id=verification_id,
                employee_name=employee_name,
                employee_id=employee_id,
                gross_salary=gross_salary,
                designation=designation,
                salary_amount=salary_amount,
                net_salary=net_salary,
                pan_number=pan_number,
                uan_number=uan_number,
                bank_account_last4=bank_account_last4,
                document_type=document_type,
                fraud_score=fraud_score,
                fraud_flags=json.dumps(fraud_flags),
                extraction_status=extraction_status,
                provider_name="Tesseract OCR",
                raw_text=raw_text,
            )

            # ==========================================
            # FRAUD STATUS
            # ==========================================

            fraud_status = "PASSED"
            remarks = "No fraud detected"

            if fraud_score > 0.70:
                fraud_status = "FAILED"
                remarks = "High fraud risk detected"
            elif fraud_score > 0.40:
                fraud_status = "REVIEW"
                remarks = "Medium fraud risk detected"

            # ==========================================
            # SAVE FRAUD CHECK
            # ==========================================

            SalarySlipRepository.save_fraud_check(
                salary_slip_id=salary_slip_id,
                fraud_type="SALARY_SLIP_ANALYSIS",
                fraud_score=fraud_score,
                fraud_status=fraud_status,
                remarks=remarks,
            )

            # ==========================================
            # COMPLETE VERIFICATION SESSION
            # ==========================================

            VerificationRepository.mark_verification_completed(verification_id)

            # ==========================================
            # API LOGGING
            # ==========================================

            response_payload = {
                "employee_name": employee_name,
                "designation": designation,
                "salary_amount": salary_amount,
                "pan_number": pan_number,
                "uan_number": uan_number,
                "bank_account_last4": bank_account_last4,
                "fraud_score": fraud_score,
            }

            SalarySlipRepository.save_api_log(
                module_name="SALARY_SLIP_VERIFICATION",
                provider_name="Tesseract OCR",
                endpoint="/api/v1/salary-slip/verify",
                request_payload=json.dumps(
                    {"candidate_id": candidate_id, "file_path": file_path}
                ),
                response_payload=json.dumps(response_payload),
                status_code=200,
            )

            # ==========================================
            # SUCCESS RESPONSE
            # ==========================================

            return {
                "success": True,
                "salary_slip_id": salary_slip_id,
                "verification_id": verification_id,
                "candidate_id": candidate_id,
                "salary_data": {
                    "employee_name": employee_name,
                    "employee_id": employee_id,
                    "designation": designation,
                    "salary_amount": salary_amount,
                    "gross_salary": gross_salary,
                    "pan_number": pan_number,
                    "uan_number": uan_number,
                    "bank_account_last4": bank_account_last4,
                },
                "fraud_score": fraud_score,
                "fraud_flags": fraud_flags,
            }

        except Exception as e:
            return {
                "success": False,
                "message": "Salary slip verification failed",
                "error": str(e),
            }
