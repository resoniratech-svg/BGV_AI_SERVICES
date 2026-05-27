from repositories.verification_repository import (
    VerificationRepository
)

class VerificationService:

    @staticmethod
    def initiate_resume_verification(
        candidate_id
    ):

        verification_id = (
            VerificationRepository
            .create_verification_request(

                candidate_id=candidate_id,

                verification_type="RESUME_PARSING",

                provider_name="RChilli",

                status="INITIATED"
            )
        )

        return verification_id
    @staticmethod
    def mark_verification_completed(
        verification_id
    ):

        VerificationRepository.update_verification_status(

            verification_id,

            "COMPLETED"
        )

    @staticmethod
    def mark_verification_failed(
        verification_id
    ):

        VerificationRepository.update_verification_status(

            verification_id,

            "FAILED"
        )
        @staticmethod
        def initiate_watchlist_verification(
            candidate_id
        ):

            from repositories.verification_repository import (
                VerificationRepository
            )

            return VerificationRepository.create_verification_request(

                candidate_id=candidate_id,

                verification_type="AML_SCREENING",

                provider_name="DILISENSE"
            )
        