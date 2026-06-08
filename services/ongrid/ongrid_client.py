import requests

from config import Config


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

        response.raise_for_status()

        return response.json()