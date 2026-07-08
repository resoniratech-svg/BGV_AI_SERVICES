from datetime import datetime, timedelta

from repositories.pan_repository import (
    PANRepository
)

from repositories.aadhaar_repository import (
    AadhaarRepository
)

from repositories.candidate_consent_repository import (
    CandidateConsentRepository
)

from repositories.ccrv_repository import (
    CCRVRepository
)

from services.ongrid.ccrv_generate_service import (
    CCRVGenerateService
)


class CCRVVerificationService:

    @staticmethod
    def verify(
            candidate_id,
            bgv_id
    ):

        ##################################################
        # PAN OCR
        ##################################################

        pan = PANRepository.get_pan_ocr_result(
            candidate_id
        )

        if not pan:
            raise Exception(
                "PAN OCR result not found"
            )

        full_name = pan.get(
            "full_name"
        )

        father_name = pan.get(
            "father_name"
        )

        date_of_birth = pan.get(
            "date_of_birth"
        )

        if not full_name:
            raise Exception(
                "PAN name not available"
            )

        if not father_name:
            raise Exception(
                "Father name not available"
            )

        if not date_of_birth:
            raise Exception(
                "PAN date of birth not available"
            )

        ##################################################
        # Aadhaar Address
        ##################################################

        aadhaar = (
            AadhaarRepository
            .get_aadhaar_verification_result(
                candidate_id
            )
        )

        if not aadhaar:
            raise Exception(
                "Aadhaar verification not found"
            )

        address = aadhaar.get(
            "address"
        )

        if not address:
            raise Exception(
                "Aadhaar address not available"
            )

        ##################################################
        # Consent
        ##################################################

        consent = (
            CandidateConsentRepository
            .get_candidate_consent(
                candidate_id,
                bgv_id,
                "CCRV"
            )
        )

        if not consent:
            raise Exception(
                "Candidate consent not found"
            )

        if consent.get("consent_status") != "APPROVED":
            raise Exception(
                "Candidate consent not approved"
            )

        ##################################################
        # Generate Report
        ##################################################

        response = (
            CCRVGenerateService
            .generate_report(
                full_name=full_name,
                father_name=father_name,
                address=address,
                date_of_birth=date_of_birth,
                consent="Y"
            )
        )

        ##################################################
        # Validate Response
        ##################################################

        if response.get("status") != 200:
            raise Exception(
                response.get(
                    "message",
                    "Failed to generate CCRV request"
                )
            )

        transaction_id = response.get(
            "transaction_id"
        )

        request_id = response.get(
            "request_id"
        )

        if not transaction_id:
            raise Exception(
                "Transaction ID not received"
            )

        ##################################################
        # Save Request
        ##################################################

        requested_at = datetime.now()

        expected_completion = (
            requested_at + timedelta(hours=8)
        )

        ccrv_request_id = (
            CCRVRepository
            .save_request(
                candidate_id=candidate_id,
                bgv_id=bgv_id,
                consent_id=consent["id"],
                provider_name="GRIDLINES",
                transaction_id=transaction_id,
                request_id=request_id,
                ccrv_status="REQUESTED",
                api_reference_id=request_id,
                raw_response=response,
                requested_at=requested_at,
                expected_completion_at=expected_completion,
                fetch_attempted=False
            )
        )

        ##################################################
        # Return
        ##################################################

        return {

            "success": True,

            "message":
                "CCRV verification requested successfully.",

            "ccrv_request_id":
                ccrv_request_id,

            "transaction_id":
                transaction_id,

            "request_id":
                request_id,

            "expected_completion_at":
                expected_completion,

            "status":
                "REQUESTED"

        }