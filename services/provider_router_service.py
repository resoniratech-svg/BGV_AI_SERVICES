from repositories.provider_usage_repository import (
    ProviderUsageRepository
)


class ProviderRouterService:

    DIDIT_FREE_LIMIT = 500

    @staticmethod
    def get_provider(

        verification_type
    ):

        didit_usage = (

            ProviderUsageRepository.get_monthly_usage(

                provider_name="DIDIT",

                verification_type=verification_type
            )
        )

        # ==========================================
        # USE DIDIT
        # ==========================================

        if didit_usage < (

            ProviderRouterService.DIDIT_FREE_LIMIT
        ):

            return "DIDIT"

        # ==========================================
        # SWITCH TO GRIDLINES
        # ==========================================

        return "GRIDLINES"