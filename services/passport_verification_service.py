from services.provider_router import (
    get_provider
)

from services.didit.passport_service import (
    DiditPassportService
)


class PassportVerificationService:

    @staticmethod
    def verify_passport(
        candidate_id,
        bgv_id,
        document_id
    ):

        provider = get_provider()

        if provider == "didit":

            return (
                DiditPassportService
                .verify_passport(
                    candidate_id=candidate_id,
                    bgv_id=bgv_id,
                    document_id=document_id
                )
            )

        raise Exception(
            "OnGrid passport verification not implemented yet"
        )