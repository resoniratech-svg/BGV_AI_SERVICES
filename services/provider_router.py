from repositories.provider_usage_repository import (
    ProviderUsageRepository
)


DIDIT_MONTHLY_LIMIT = 500


def get_provider():

    passport_usage = (
        ProviderUsageRepository
        .get_monthly_usage(
            provider_name="DIDIT",
            verification_type="PASSPORT"
        )
    )

    dl_usage = (
        ProviderUsageRepository
        .get_monthly_usage(
            provider_name="DIDIT",
            verification_type="DRIVING_LICENSE"
        )
    )

    total_usage = passport_usage + dl_usage

    if total_usage >= DIDIT_MONTHLY_LIMIT:

        return "ongrid"

    return "didit"