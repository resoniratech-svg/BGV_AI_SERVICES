from repositories.provider_usage_repository import (
    ProviderUsageRepository
)


def get_provider():

    monthly_count = (
        ProviderUsageRepository.get_monthly_usage(
            provider_name="didit",
            verification_type="passport_dl"
        )
    )

    if monthly_count < 500:
        return "didit"

    return "ongrid"