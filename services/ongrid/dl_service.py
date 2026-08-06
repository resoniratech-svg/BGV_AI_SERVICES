import json
import requests

from services.ongrid.ongrid_client import (
    OnGridClient
)

from repositories.provider_usage_repository import (
    ProviderUsageRepository
)


class OnGridDrivingLicenseService:

    PROVIDER_NAME = "GRIDLINES"

    @staticmethod
    def verify_driving_license(

            license_number,
            date_of_birth

    ):

        ###################################################
        # PAYLOAD
        ###################################################

        payload = {

            "driving_license_number":

            license_number,

            "date_of_birth":

            date_of_birth,

            "consent":

            "Y"

        }

        print("=" * 80)
        print("GRIDLINES DRIVING LICENSE FETCH PAYLOAD")
        print(json.dumps(payload, indent=4))
        print("=" * 80)

        ###################################################
        # API CALL
        ###################################################

        try:

            response = (

                OnGridClient.post(

                    "/dl-api/fetch",

                    payload

                )

            )

        except requests.exceptions.Timeout:

            raise Exception(

                "Gridlines Driving License verification timed out"

            )

        except requests.exceptions.ConnectionError:

            raise Exception(

                "Unable to connect to Gridlines Driving License service"

            )

        except Exception as e:

            raise Exception(

                f"Gridlines Driving License verification failed. {str(e)}"

            )

        print("=" * 80)
        print("GRIDLINES DRIVING LICENSE FETCH RESPONSE")
        print(json.dumps(response, indent=4))
        print("=" * 80)

        ###################################################
        # VALIDATION
        ###################################################

        if not response:

            raise Exception(

                "Empty response received from Gridlines"

            )

        if response.get("status") != 200:

            raise Exception(

                response.get(

                    "message",

                    "Driving License verification failed"

                )

            )

        data = response.get(

            "data",

            {}

        )

        if data.get("code") != "1000":

            raise Exception(

                data.get(

                    "message",

                    "Driving License verification failed"

                )

            )

        ###################################################
        # PROVIDER USAGE
        ###################################################

        ProviderUsageRepository.increment_usage(

            provider_name=OnGridDrivingLicenseService.PROVIDER_NAME,

            verification_type="DRIVING_LICENSE"

        )

        ###################################################
        # RETURN COMPLETE RESPONSE
        ###################################################

        return response 