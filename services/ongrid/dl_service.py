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
        print("=" * 80)
        print("GRIDLINES DL PAYLOAD")
        print(payload)
        print("=" * 80)
        response = OnGridClient.post(

            "/dl-api/fetch",

            payload
        )
        gridlines_success = (
            response.get(
                "data",
                {}
            ).get(
                "code"
            ) == "1000"
        )
        return {
            "success": gridlines_success,
            "provider": "ongrid",
            "request_id": response.get("request_id"),
            "status": response.get("status"),
            "response": response
        }