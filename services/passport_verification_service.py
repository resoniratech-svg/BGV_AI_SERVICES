from repositories.document_repository import (
    DocumentRepository
)

from repositories.passport_repository import (
    PassportRepository
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


class PassportVerificationService:

    PASSPORT_VERIFICATION = (
        "PASSPORT"
    )

    @staticmethod
    def verify_passport(

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

                    PassportVerificationService
                    .PASSPORT_VERIFICATION
                )
            )
        )

        # ======================================
        # DIDIT PROVIDER
        # ======================================

        if provider == "DIDIT":

            result = (
                DiditService
                .verify_passport_document(

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
            # GRIDLINES PROVIDER
            # ==================================

            result = (
                GridlinesService
                .verify_passport_document(

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

        PassportRepository.save_passport_result(

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

            passport_number=(
                result.get(
                    "passport_number"
                )
            ),

            full_name=(
                result.get(
                    "full_name"
                )
            ),

            nationality=(
                result.get(
                    "nationality"
                )
            ),

            country=(
                result.get(
                    "country"
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

                PassportVerificationService
                .PASSPORT_VERIFICATION
            )
        )

        # ======================================
        # FINAL RESPONSE
        # ======================================

        return {

            "success": result.get(
                "success",
                False
            ),

            "provider": provider,

            "verification_status": (
                result.get(
                    "verification_status"
                )
            ),

            "provider_message": (
                result.get(
                    "message"
                )
            ),

            "message": (
                "Passport verification completed"
            )
        }