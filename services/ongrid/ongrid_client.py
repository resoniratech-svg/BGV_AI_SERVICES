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
            response.raise_for_status()

        return response.json()