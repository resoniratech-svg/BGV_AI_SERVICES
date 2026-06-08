import uuid

from services.ongrid.ongrid_client import (
    OnGridClient
)


class OnGridPassportService:

    @staticmethod
    def verify_passport(
        passport_number,
        file_number,
        surname,
        given_name,
        date_of_birth
    ):

        payload = {

            "passport_number": passport_number,

            "file_number": file_number,

            "surname": surname,

            "given_name": given_name,

            "date_of_birth": date_of_birth,

            "consent": "Y"
        }

        response = OnGridClient.post(

            "/passport-api/verify",

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