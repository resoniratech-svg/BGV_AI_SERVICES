import requests

from config import Config
from utils import response


class OnGridClient:

    @staticmethod
    def post(endpoint, payload):

        headers = {

            "X-API-Key": Config.GRIDLINES_API_KEY,

            "X-Auth-Type": "API-Key",

            "Content-Type": "application/json",

            "Accept": "application/json"
        }
        print("=" * 80)
        print("GRIDLINES REQUEST")
        print("URL =", f"{Config.GRIDLINES_PRODUCTION_URL}{endpoint}")
        print("HEADERS =", headers)
        print("PAYLOAD =", payload)
        print("=" * 80)
        response = requests.post(

            f"{Config.GRIDLINES_PRODUCTION_URL}{endpoint}",

            headers=headers,

            json=payload,

            timeout=60
        )
        if not response.ok:

            print("=" * 80)
            print("GRIDLINES ERROR RESPONSE")
            print("STATUS =", response.status_code)
            print("BODY =", response.text)
            print("=" * 80)
            return {

                "success": False,

                "verification_status": "FAILED",

                "status": response.status_code,

                "request_id": None,

                "raw_response": response.text
            }   

        return response.json()