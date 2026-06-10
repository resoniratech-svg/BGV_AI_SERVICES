from services.provider_router import (
    get_provider
)

from services.didit.dl_service import (
    DiditDrivingLicenseService
)

from services.ongrid.driving_license_verification_service import (
    OnGridDrivingLicenseVerificationService
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

        # ======================================
        # DIDIT
        # ======================================


        if provider == "didit":

            return (
                DiditDrivingLicenseService
                .verify_driving_license(
                    candidate_id,
                    bgv_id,
                    front_document_id,
                    back_document_id
                )
            )

        if provider == "ongrid":
            return (
                OnGridDrivingLicenseVerificationService
                .verify_driving_license(

                    candidate_id=candidate_id,

                    bgv_id=bgv_id,

                    document_id=front_document_id
                )
            )

        