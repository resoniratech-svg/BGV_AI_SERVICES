import os
import re
import json

from utils.ocr_utils import (
    OCRUtils
)

from utils.image_preprocessing import (
    ImagePreprocessing
)

from repositories.salary_slip_repository import (
    SalarySlipRepository
)

from services.verification_service import (
    VerificationService
)


class SalarySlipService:

    @staticmethod
    def verify_salary_slip(

        file_path,
        candidate_id
    ):

        try:

            # ==========================================
            # CREATE VERIFICATION SESSION
            # ==========================================

            verification_id = (
                VerificationService
                .initiate_resume_verification(

                    candidate_id
                )
            )

            # ==========================================
            # SAVE DOCUMENT ENTRY
            # ==========================================

            stored_filename = os.path.basename(
                file_path
            )

            SalarySlipRepository.save_salary_slip_document(

                candidate_id=candidate_id,

                verification_id=verification_id,

                original_file_name=stored_filename,

                stored_file_name=stored_filename,

                file_path=file_path,

                file_size=os.path.getsize(
                    file_path
                ),

                mime_type="application/octet-stream",

                upload_status="UPLOADED"
            )

            # ==========================================
            # IMAGE PREPROCESSING
            # ==========================================

            file_extension = os.path.splitext(
                file_path
            )[1].lower()

            if file_extension in [

                ".png",
                ".jpg",
                ".jpeg"
            ]:

                file_path = (
                    ImagePreprocessing
                    .preprocess_image(

                        file_path
                    )
                )

            # ==========================================
            # OCR EXTRACTION
            # ==========================================

            raw_text = (
                OCRUtils.extract_text(

                    file_path
                )
            )
            print("\n===== SALARY OCR OUTPUT =====\n")

            print(raw_text)

            print("\n=============================\n")

            # ==========================================
            # EMPTY OCR CHECK
            # ==========================================

            if not raw_text.strip():

                VerificationService.mark_verification_failed(

                    verification_id
                )

                return {

                    "success": False,

                    "message": (
                        "No text extracted from salary slip"
                    )
                }

            # ==========================================
            # PAN EXTRACTION
            # ==========================================

            pan_match = re.search(

                r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",

                raw_text,
                re.IGNORECASE
            )

            pan_number = (

                pan_match.group(0).upper()

                if pan_match

                else None
            )

            # ==========================================
            # UAN EXTRACTION
            # ==========================================

            uan_match = re.search(

                r"\b\d{12}\b",

                raw_text
            )

            uan_number = (

                uan_match.group(0)

                if uan_match

                else None
            )

            # ==========================================
            # NET SALARY EXTRACTION
            # ==========================================

            salary_match = re.search(

                r"(?:Net Salary|Take Home|Net Pay)[^\d]*(\d[\d,]*)",

                raw_text,

                re.IGNORECASE
            )

            salary_amount = (

                salary_match.group(1).replace(",", "")

                if salary_match

                else None
            )

            net_salary = salary_amount

            # ==========================================
            # EMPLOYEE NAME EXTRACTION
            # ==========================================

            employee_name = None

            employee_patterns = [

                r"Employee Name[\s:\-]+([A-Za-z ]+)",
                r"Name[\s:\-]+([A-Za-z ]+)",
                r"Employee[\s:\-]+([A-Za-z ]+)"
            ]

            for pattern in employee_patterns:

                match = re.search(

                    pattern,
                    raw_text,
                    re.IGNORECASE
                )

                if match:

                    employee_name = (
                        match.group(1).strip()
                    )

                    break

            # ==========================================
            # DESIGNATION EXTRACTION
            # ==========================================

            designation = None

            designation_patterns = [

                r"Designation[\s:\-]+([A-Za-z ]+)",
                r"Role[\s:\-]+([A-Za-z ]+)",
                r"Position[\s:\-]+([A-Za-z ]+)",
                r"Department[\s:\-]+([A-Za-z ]+)"
            ]

            for pattern in designation_patterns:

                match = re.search(

                    pattern,
                    raw_text,
                    re.IGNORECASE
                )

                if match:

                    designation = (
                        match.group(1).strip()
                    )

                    break

            # ==========================================
            # BANK ACCOUNT EXTRACTION
            # ==========================================

            bank_account_last4 = None

            bank_patterns = [

                r"Account Number[^\d]*(\d{4,})",
                r"A/C Number[^\d]*(\d{4,})",
                r"Bank Account[^\d]*(\d{4,})"
            ]

            for pattern in bank_patterns:

                match = re.search(

                    pattern,
                    raw_text,
                    re.IGNORECASE
                )

                if match:

                    bank_account_last4 = (
                        match.group(1)[-4:]
                    )

                    break

            # ==========================================
            # FRAUD CHECKS
            # ==========================================

            fraud_flags = []

            fraud_score = 0.00

            if not pan_number:

                fraud_flags.append(
                    "PAN_NOT_FOUND"
                )

                fraud_score += 0.25

            if not salary_amount:

                fraud_flags.append(
                    "SALARY_NOT_FOUND"
                )

                fraud_score += 0.25

            if not employee_name:

                fraud_flags.append(
                    "EMPLOYEE_NAME_NOT_FOUND"
                )

                fraud_score += 0.10

            # ==========================================
            # STATIC VALUES
            # ==========================================

            document_type = "SALARY_SLIP"

            extraction_status = "SUCCESS"

            # ==========================================
            # SAVE RESULT
            # ==========================================

            salary_slip_id = (
                SalarySlipRepository
                .save_salary_slip_result(

                    candidate_id=candidate_id,

                    verification_id=verification_id,

                    employee_name=employee_name,

                    designation=designation,

                    salary_amount=salary_amount,

                    net_salary=net_salary,

                    pan_number=pan_number,

                    uan_number=uan_number,

                    bank_account_last4=bank_account_last4,

                    document_type=document_type,

                    fraud_score=fraud_score,

                    fraud_flags=json.dumps(
                        fraud_flags
                    ),

                    extraction_status=extraction_status,

                    provider_name="Tesseract OCR",

                    raw_text=raw_text
                )
            )

            # ==========================================
            # SAVE OCR PAGE
            # ==========================================

            SalarySlipRepository.save_ocr_page(

                salary_slip_id=salary_slip_id,

                page_number=1,

                extracted_text=raw_text
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

                remarks=remarks
            )

            # ==========================================
            # UPDATE VERIFICATION RESULT
            # ==========================================

            VerificationService.update_verification_result(

                verification_id=verification_id,

                status="COMPLETED",

                module_score=fraud_score,

                remarks=remarks,

                document_path=file_path
            )

            # ==========================================
            # COMPLETE VERIFICATION
            # ==========================================

            VerificationService.mark_verification_completed(

                verification_id
            )

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

                "fraud_score": fraud_score
            }

            SalarySlipRepository.save_api_log(

                module_name="SALARY_SLIP_VERIFICATION",

                provider_name="Tesseract OCR",

                endpoint="/api/v1/salary-slip/verify",

                request_payload=json.dumps({

                    "candidate_id": candidate_id,

                    "file_path": file_path
                }),

                response_payload=json.dumps(
                    response_payload
                ),

                status_code=200
            )

            # ==========================================
            # SUCCESS RESPONSE
            # ==========================================

            return {

                "success": True,

                "salary_slip_id": (
                    salary_slip_id
                ),

                "verification_id": (
                    verification_id
                ),

                "candidate_id": (
                    candidate_id
                ),

                "salary_data": {

                    "employee_name": (
                        employee_name
                    ),

                    "designation": (
                        designation
                    ),

                    "salary_amount": (
                        salary_amount
                    ),

                    "pan_number": (
                        pan_number
                    ),

                    "uan_number": (
                        uan_number
                    ),

                    "bank_account_last4": (
                        bank_account_last4
                    )
                },

                "fraud_score": (
                    fraud_score
                ),

                "fraud_flags": (
                    fraud_flags
                )
            }

        except Exception as e:

            return {

                "success": False,

                "message": (
                    "Salary slip verification failed"
                ),

                "error": str(e)
            }