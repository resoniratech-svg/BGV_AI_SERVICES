from services.provider_router import (
    get_provider
)

from services.didit.passport_service import (
    DiditPassportService
)

from services.ongrid.passport_verification_service import (
    OnGridPassportVerificationService
)


class PassportVerificationService:

    @staticmethod
    def verify_passport(
        candidate_id,
        bgv_id,
        document_id
    ):

        provider = get_provider()

        # ======================================
        # DIDIT
        # ======================================

        if provider == "didit":

            return (
                DiditPassportService
                .verify_passport(

                    candidate_id=candidate_id,

                    bgv_id=bgv_id,

                    document_id=document_id
                )
            )

        # ======================================
        # ONGRID
        # ======================================

        if provider == "ongrid":

            return (
                OnGridPassportVerificationService
                .verify_passport(
                    document_id,
                    candidate_id,
                    bgv_id
                )
            )

        raise Exception(
            "Invalid provider"
        )