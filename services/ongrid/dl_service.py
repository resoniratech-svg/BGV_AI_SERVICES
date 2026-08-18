import json

from services.ongrid.ongrid_client import OnGridClient

from repositories.provider_usage_repository import (
    ProviderUsageRepository,
)


class OnGridDrivingLicenseService:
    PROVIDER_NAME = "GRIDLINES"

    # =====================================================
    # FETCH DRIVING LICENSE DETAILS
    # =====================================================

    @staticmethod
    def verify_driving_license(
        license_number,
        date_of_birth,
    ):

        # =================================================
        # VALIDATE INPUT
        # =================================================

        if not license_number:
            raise Exception("Driving License number is required")

        if not date_of_birth:
            raise Exception(
                "Date of birth is required for Driving License verification"
            )

        # =================================================
        # PAYLOAD
        # =================================================

        payload = {
            "driving_license_number": license_number,
            "date_of_birth": date_of_birth,
            "consent": "Y",
        }

        print("=" * 80)
        print("GRIDLINES DRIVING LICENSE FETCH")
        print("=" * 80)

        print(
            "LICENSE NUMBER:",
            license_number,
        )

        print(
            "DATE OF BIRTH:",
            date_of_birth,
        )

        print(
            "CONSENT:",
            "Y",
        )

        print(
            "ENDPOINT:",
            "/dl-api/fetch",
        )

        print("PAYLOAD:")
        print(
            json.dumps(
                payload,
                indent=4,
                default=str,
            )
        )

        print("=" * 80)

        # =================================================
        # GRIDLINES API CALL
        # =================================================

        try:
            response = OnGridClient.post(
                "/dl-api/fetch",
                payload,
            )

        except Exception as error:
            raise Exception(
                "Unable to connect to Gridlines "
                f"Driving License Fetch service. {str(error)}"
            )

        # =================================================
        # DEBUG RESPONSE
        # =================================================

        print("=" * 80)
        print("GRIDLINES DRIVING LICENSE FETCH RESPONSE")
        print("=" * 80)

        print(
            json.dumps(
                response,
                indent=4,
                default=str,
            )
        )

        print("=" * 80)

        # =================================================
        # EMPTY RESPONSE
        # =================================================

        if not response:
            raise Exception(
                "No response received from Gridlines Driving License service"
            )

        # =================================================
        # HTTP STATUS VALIDATION
        # =================================================

        response_status = response.get("status")

        if response_status != 200:
            error_message = (
                response.get("data", {}).get("message")
                or response.get("message")
                or response.get("raw_response")
                or "Driving License verification failed"
            )

            raise Exception(
                f"Gridlines Driving License verification failed: {error_message}"
            )

        # =================================================
        # RESPONSE DATA
        # =================================================

        data = response.get(
            "data",
            {},
        )

        if not isinstance(data, dict):
            raise Exception(
                "Invalid data received from Gridlines Driving License service"
            )

        # =================================================
        # GRIDLINES RESPONSE CODE
        # =================================================

        response_code = data.get("code")

        # =================================================
        # SUCCESS
        # =================================================

        if response_code == "1000":
            dl_data = data.get("driving_license_data")

            if not dl_data:
                raise Exception(
                    "Gridlines returned success but Driving License data is missing"
                )

            # -------------------------------------------------
            # REQUIRED PROVIDER FIELDS
            # -------------------------------------------------

            provider_license_number = dl_data.get("document_id")

            provider_name = dl_data.get("name")

            provider_dob = dl_data.get("date_of_birth")

            if not provider_license_number:
                raise Exception(
                    "Gridlines response does not contain Driving License number"
                )

            if not provider_name:
                raise Exception(
                    "Gridlines response does not contain Driving License holder name"
                )

            if not provider_dob:
                raise Exception("Gridlines response does not contain date of birth")

            print("=" * 80)
            print("GRIDLINES DRIVING LICENSE FETCH SUCCESS")
            print("=" * 80)

            print(
                "LICENSE NUMBER:",
                provider_license_number,
            )

            print(
                "NAME:",
                provider_name,
            )

            print(
                "DATE OF BIRTH:",
                provider_dob,
            )

            print("=" * 80)

            # =================================================
            # PROVIDER USAGE
            # =================================================

            ProviderUsageRepository.increment_usage(
                provider_name=(OnGridDrivingLicenseService.PROVIDER_NAME),
                verification_type="DRIVING_LICENSE",
            )

            # =================================================
            # RETURN COMPLETE RESPONSE
            # =================================================

            return response

        # =================================================
        # LICENSE DOES NOT EXIST
        # Gridlines code: 1001
        # =================================================

        if response_code == "1001":
            message = data.get(
                "message",
                "Driving License does not exist",
            )

            raise Exception(f"Gridlines Driving License verification failed: {message}")

        # =================================================
        # INVALID LICENSE
        # =================================================

        if response_code == "INVALID_DRIVING_LICENSE":
            message = data.get(
                "message",
                "Invalid Driving License number",
            )

            raise Exception(f"Gridlines rejected the Driving License: {message}")

        # =================================================
        # UNKNOWN GRIDLINES RESPONSE CODE
        # =================================================

        message = data.get(
            "message",
            "Driving License verification failed",
        )

        raise Exception(
            f"Gridlines Driving License verification failed "
            f"(code: {response_code}): {message}"
        )
