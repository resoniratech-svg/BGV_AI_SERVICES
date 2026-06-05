from repositories.document_repository import (
    DocumentRepository
)

from repositories.driving_license_repository import (
    DrivingLicenseRepository
)

from repositories.provider_usage_repository import (
    ProviderUsageRepository
)

from services.provider_router_service import (
    ProviderRouterService
)

from services.didit_service import (
    DiditService
)

from services.gridlines_service import (
    GridlinesService
)


class DrivingLicenseVerificationService:

    DRIVING_LICENSE_VERIFICATION = (
        "DRIVING_LICENSE"
    )

    @staticmethod
    def verify_driving_license(

        candidate_id,
        bgv_id,
        document_id
    ):

        # ======================================
        # FETCH UPLOADED DOCUMENT
        # ======================================

        document = (
            DocumentRepository
            .get_uploaded_document(
                document_id
            )
        )

        if not document:

            return {

                "success": False,

                "message": (
                    "Uploaded document not found"
                )
            }

        # ======================================
        # PROVIDER ROUTING
        # ======================================

        provider = (
            ProviderRouterService
            .get_provider(

                verification_type=(

                    DrivingLicenseVerificationService
                    .DRIVING_LICENSE_VERIFICATION
                )
            )
        )

        # ======================================
        # DIDIT PROVIDER
        # ======================================

        if provider == "DIDIT":

            result = (
                DiditService
                .verify_driving_license_document(

                    candidate_id=(
                        candidate_id
                    ),

                    bgv_id=(
                        bgv_id
                    ),

                    document_path=(
                        document.get(
                            "file_path"
                        )
                    )
                )
            )

        else:

            # ==================================
            # ONGRID PROVIDER
            # ==================================

            result = (
                GridlinesService
                .verify_driving_license_document(

                    candidate_id=(
                        candidate_id
                    ),

                    bgv_id=(
                        bgv_id
                    ),

                    document_path=(
                        document.get(
                            "file_path"
                        )
                    )
                )
            )

        # ======================================
        # SAVE RESULT
        # ======================================

        DrivingLicenseRepository.save_driving_license_result(

            candidate_id=(
                candidate_id
            ),

            bgv_id=(
                bgv_id
            ),

            verification_status=(
                result.get(
                    "verification_status"
                )
            ),

            license_number=(
                result.get(
                    "license_number"
                )
            ),

            full_name=(
                result.get(
                    "full_name"
                )
            ),

            date_of_birth=(
                result.get(
                    "date_of_birth"
                )
            ),

            issue_date=(
                result.get(
                    "issue_date"
                )
            ),

            expiry_date=(
                result.get(
                    "expiry_date"
                )
            ),

            provider_name=(
                provider
            ),

            raw_response=str(result)
        )

        # ======================================
        # INCREMENT PROVIDER USAGE
        # ======================================

        ProviderUsageRepository.increment_usage(

            provider_name=(
                provider
            ),

            verification_type=(

                DrivingLicenseVerificationService
                .DRIVING_LICENSE_VERIFICATION
            )
        )

        # ======================================
        # FINAL RESPONSE
        # ======================================

        return {

            "success": True,

            "provider": provider,

            "verification_status": (
                result.get(
                    "verification_status"
                )
            ),

            "message": (
                "Driving license verification completed"
            )
        }