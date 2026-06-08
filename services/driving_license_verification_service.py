from services.provider_router import (
    get_provider
)

from services.didit.dl_service import (
    DiditDrivingLicenseService
)

from services.ongrid.dl_service import (
    OnGridDrivingLicenseService
)


class DrivingLicenseVerificationService:

    @staticmethod
    def verify_driving_license(
        candidate_id,
        bgv_id,
        front_document_id,
        back_document_id
    ):

        provider = get_provider()

        # ==================================
        # DIDIT
        # ==================================

        if provider == "didit":

            return (
                DiditDrivingLicenseService
                .verify_driving_license(

                    candidate_id=candidate_id,

                    bgv_id=bgv_id,

                    front_document_id=front_document_id,

                    back_document_id=back_document_id
                )
            )

        # ==================================
        # ONGRID
        # ==================================

        if provider == "ongrid":

            raise Exception(
                "OnGrid requires DL number and DOB. OCR extraction integration pending."
            )

        raise Exception(
            "Invalid provider"
        )