import os
import requests


class SurepassClient:

    def __init__(self):

        self.base_url = "https://kyc-api.surepass.io"

        self.api_key = os.getenv("SUREPASS_API_KEY")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def post(self, endpoint, payload):

        url = f"{self.base_url}/{endpoint}"

        response = requests.post(
            url,
            json=payload,
            headers=self.headers
        )

        return response.json()