from services.ongrid.ongrid_client import (
    OnGridClient
)


class OnGridDrivingLicenseService:

    @staticmethod
    def verify_driving_license(
        dl_number,
        date_of_birth
    ):

        payload = {

            "driving_license_number": dl_number,

            "date_of_birth": date_of_birth,

            "consent": "Y"
        }

        response = OnGridClient.post(

            "/dl-api/fetch",

            payload
        )

        return {

            "success": True,

            "provider": "ongrid",

            "request_id": response.get(
                "request_id"
            ),

            "status": response.get(
                "status"
            ),

            "response": response
        }