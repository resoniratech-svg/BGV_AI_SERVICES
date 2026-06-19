import requests

from config import Config


class OnGridClient:

    @staticmethod
    def post(

        endpoint,
        payload

    ):

        headers = {

            "X-API-Key":
            Config.GRIDLINES_API_KEY,

            "X-Auth-Type":
            "API-Key",

            "Content-Type":
            "application/json",

            "Accept":
            "application/json"

        }

        try:

            response = requests.post(

                f"{Config.GRIDLINES_PRODUCTION_URL}{endpoint}",

                headers=headers,

                json=payload,

                timeout=60

            )

        except Exception as e:

            return {

                "success": False,

                "status": 500,

                "request_id": None,

                "raw_response": str(e)

            }

        if not response.ok:

            print("=" * 80)
            print("GRIDLINES ERROR RESPONSE")

            print(

                "STATUS =",

                response.status_code

            )

            print(

                "BODY =",

                response.text

            )

            print("=" * 80)

            return {

                "success": False,

                "verification_status":
                "FAILED",

                "status":
                response.status_code,

                "request_id":
                None,

                "raw_response":
                response.text

            }

        return response.json()

    @staticmethod
    def get(

        endpoint,

        headers=None

    ):

        request_headers = {

            "X-API-Key":
            Config.GRIDLINES_API_KEY,

            "X-Auth-Type":
            "API-Key",

            "Content-Type":
            "application/json",

            "Accept":
            "application/json"

        }

        if headers:

            request_headers.update(

                headers

            )

        try:

            response = requests.get(

                f"{Config.GRIDLINES_PRODUCTION_URL}{endpoint}",

                headers=request_headers,

                timeout=60

            )

        except Exception as e:

            return {

                "success": False,

                "status": 500,

                "request_id": None,

                "raw_response": str(e)

            }

        if not response.ok:

            print("=" * 80)
            print("GRIDLINES ERROR RESPONSE")

            print(

                "STATUS =",

                response.status_code

            )

            print(

                "BODY =",

                response.text

            )

            print("=" * 80)

            return {

                "success": False,

                "status":
                response.status_code,

                "request_id":
                None,

                "raw_response":
                response.text

            }

        return response.json()