import json

from datetime import datetime

from services.ongrid.ongrid_client import OnGridClient

from repositories.salary_slip_repository import SalarySlipRepository

from repositories.pan_repository import PanRepository

from repositories.consent_repository import ConsentRepository

from repositories.employment_repository import EmploymentRepository

from repositories.provider_usage_repository import ProviderUsageRepository


class EmploymentService:
    ####################################################
    # DATE PARSER
    ####################################################

    @staticmethod
    def parse_date(date_value):

        if not date_value:
            return None

        try:
            return datetime.strptime(date_value, "%Y-%m-%d").date()

        except Exception:
            return None

    ####################################################
    # VERIFY EMPLOYMENT
    ####################################################

    @staticmethod
    def verify_employment(candidate_id, bgv_id, mobile_number):

        ####################################################
        # SALARY SLIP OCR
        ####################################################

        salary_slip = SalarySlipRepository.get_salary_slip_ocr_result(candidate_id)

        if not salary_slip:
            raise Exception("Salary Slip OCR result not found.")

        ####################################################
        # UAN
        ####################################################

        uan_number = salary_slip.get("uan_number")

        ####################################################
        # MANUAL VERIFICATION
        ####################################################

        if not uan_number:
            return {
                "success": False,
                "status": "MANUAL_VERIFICATION_REQUIRED",
                "message": "UAN number not found in Salary Slip OCR. Candidate must proceed with Manual Employment Verification.",
                "candidate_id": candidate_id,
                "bgv_id": bgv_id,
            }

        ####################################################
        # PAN OCR
        ####################################################

        pan = PanRepository.get_pan_ocr_result(candidate_id)

        if not pan:
            raise Exception("PAN OCR result not found.")

        ####################################################
        # PAN DETAILS
        ####################################################

        pan_number = pan.get("pan_number")

        full_name = pan.get("full_name")

        ####################################################
        # VALIDATION
        ####################################################

        if not pan_number:
            raise Exception("PAN number not available.")

        if not full_name:
            raise Exception("Candidate name not available.")

        if not mobile_number:
            raise Exception("Candidate mobile number not available.")

        ####################################################
        # CONSENT
        ####################################################

        consent = ConsentRepository.get_candidate_consent(
            candidate_id=candidate_id, bgv_id=bgv_id, verification_type="EMPLOYMENT"
        )

        if not consent:
            raise Exception("Employment consent not found.")

        ####################################################
        # CONSENT STATUS
        ####################################################

        if consent.get("consent_status") != "GIVEN":
            raise Exception("Candidate has not given Employment consent.")

        ####################################################
        # GRIDLINES PAYLOAD
        ####################################################

        payload = {
            "mobile_number": mobile_number,
            "pan": pan_number,
            "uan_number": uan_number,
            "name": full_name,
            "consent": "Y",
            "include_profile_details": True,
            "include_employer_details": True,
            "partial_response": False,
        }

        print("=" * 80)
        print("EMPLOYMENT REQUEST PAYLOAD")
        print(json.dumps(payload, indent=4))
        print("=" * 80)

        ####################################################
        # GRIDLINES API
        ####################################################

        response = OnGridClient.post("/epfo-api/employment-history/fetch/v2", payload)

        print("=" * 80)
        print("EMPLOYMENT RESPONSE")
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

        if response.get("status") != 200:
            status = response.get("status")

            request_id = response.get("request_id")

            raw_response = response.get("raw_response")

            raise Exception(
                f"""
        Gridlines Employment API Error

        Status      : {status}

        Request ID  : {request_id}

        Response    :

        {raw_response}
                """.strip()
            )

        ####################################################
        # RESPONSE DATA
        ####################################################

        data = response.get("data", {})

        ####################################################
        # GRIDLINES CODE
        ####################################################

        if data.get("code") != "1013":
            raise Exception(data.get("message", "Employment Verification failed."))

        ####################################################
        # TRANSACTION VALIDATION
        ####################################################

        transaction_id = response.get("transaction_id")

        request_id = response.get("request_id")

        if not transaction_id:
            raise Exception("Gridlines did not return transaction_id.")

        if not request_id:
            raise Exception("Gridlines did not return request_id.")

        print("=" * 80)
        print("GRIDLINES TRANSACTION")
        print("Transaction ID :", transaction_id)
        print("Request ID     :", request_id)
        print("=" * 80)

        ####################################################
        # SAVE REQUEST
        ####################################################

        employment_request_id = EmploymentRepository.save_request(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            consent_id=consent["id"],
            provider_name="GRIDLINES",
            transaction_id=transaction_id,
            request_id=request_id,
            verification_status="COMPLETED",
            api_reference_id=request_id,
            raw_response=json.dumps(response, default=str),
            requested_at=datetime.now(),
            completed_at=datetime.now(),
        )

        if not employment_request_id:
            raise Exception("Unable to save Employment request.")

        ####################################################
        # DUPLICATE RESULT
        ####################################################

        if EmploymentRepository.result_exists(employment_request_id):
            EmploymentRepository.delete_existing_result(employment_request_id)

        ####################################################
        # UAN PROFILE
        ####################################################

        uan_profiles = data.get("uan_profiles", [])

        profile = {}

        if len(uan_profiles) > 0:
            profile = uan_profiles[0].get("uan_profile_data", {})
        ####################################################
        # SAVE EMPLOYMENT RESULT
        ####################################################

        employment_result_id = EmploymentRepository.save_result(
            employment_request_id=employment_request_id,
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            uan=profile.get("uan"),
            name=profile.get("name"),
            pan_number=profile.get("pan_number"),
            dob=EmploymentService.parse_date(profile.get("dob")),
            gender=profile.get("gender"),
            mobile_number=profile.get("mobile_number"),
            email=profile.get("email"),
            masked_aadhaar_number=profile.get("masked_aadhaar_number"),
            guardian_name=profile.get("guardian_name"),
            guardian_relation=profile.get("guardian_relation"),
            bank_account_number=profile.get("bank_account_number"),
            ifsc=profile.get("ifsc"),
            provider_name="GRIDLINES",
            request_id=request_id,
            transaction_id=transaction_id,
            api_reference_id=request_id,
            raw_response=json.dumps(response, default=str),
            verified_at=datetime.now(),
        )

        if not employment_result_id:
            raise Exception("Unable to save Employment result.")

        ####################################################
        # SAVE EMPLOYMENT HISTORY
        ####################################################

        histories = data.get("employment_history", [])

        for history in histories:
            history_uan = history.get("uan")

            employment_data = history.get("employment_data", [])

            for company in employment_data:
                EmploymentRepository.save_history(
                    employment_result_id=employment_result_id,
                    uan=history_uan,
                    employee_name=company.get("name"),
                    establishment_name=company.get("establishment_name"),
                    member_id=company.get("member_id"),
                    joining_date=EmploymentService.parse_date(
                        company.get("date_of_joining")
                    ),
                    exit_date=EmploymentService.parse_date(company.get("date_of_exit")),
                    guardian_name=company.get("guardian_name"),
                    name_match_score=company.get("name_match_score"),
                    raw_history=json.dumps(company, default=str),
                )

        ####################################################
        # SAVE EMPLOYER DETAILS
        ####################################################

        employer_data = data.get("employer_data", {})

        establishment = employer_data.get("establishment_data", {})

        address = establishment.get("address_data", {})

        EmploymentRepository.save_employer_details(
            employment_result_id=employment_result_id,
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            establishment_id=establishment.get("establishment_id"),
            establishment_name=establishment.get("establishment_name"),
            business_activity=establishment.get("business_activity"),
            pan_status=establishment.get("pan_status"),
            ownership_type=establishment.get("ownership_type"),
            employer_status=establishment.get("status"),
            date_of_setup=EmploymentService.parse_date(
                establishment.get("date_of_setup")
            ),
            date_of_coverage=EmploymentService.parse_date(
                establishment.get("date_of_coverage")
            ),
            last_updated=EmploymentService.parse_date(
                establishment.get("last_updated")
            ),
            address_line1=address.get("line_1"),
            address_line2=address.get("line_2"),
            city=address.get("city"),
            district=address.get("district"),
            state=address.get("state"),
            pf_payment_details=json.dumps(
                establishment.get("pf_payment_details", []), default=str
            ),
            provider_name="GRIDLINES",
            request_id=request_id,
            transaction_id=transaction_id,
            api_reference_id=request_id,
            raw_response=json.dumps(establishment, default=str),
            verified_at=datetime.now(),
        )

        ####################################################
        # PROVIDER USAGE
        ####################################################

        ProviderUsageRepository.increment_usage(
            provider_name="GRIDLINES", verification_type="EMPLOYMENT"
        )

        ####################################################
        # SUCCESS LOG
        ####################################################

        print("=" * 80)
        print("EMPLOYMENT VERIFICATION COMPLETED")
        print("Candidate ID   :", candidate_id)
        print("Transaction ID :", transaction_id)
        print("Result ID      :", employment_result_id)
        print("=" * 80)

        ####################################################
        # RETURN
        ####################################################

        return {
            "success": True,
            "message": "Employment verification completed successfully.",
            "employment_request_id": employment_request_id,
            "employment_result_id": employment_result_id,
            "transaction_id": transaction_id,
            "request_id": request_id,
            "verification_status": "COMPLETED",
        }
