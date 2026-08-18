import requests

from config import Config


class GridlinesService:
    @staticmethod
    def get_base_url():

        if Config.GRIDLINES_ENV == "LIVE":
            return Config.GRIDLINES_PRODUCTION_URL

        # return Config.GRIDLINES_SANDBOX_URL

        return Config.GRIDLINES_PRODUCTION_URL

    @staticmethod
    def get_headers():

        return {
            "Content-Type": ("application/json"),
            "X-API-KEY": (Config.GRIDLINES_API_KEY),
        }

    @staticmethod
    def verify_passport(passport_number, date_of_birth):

        try:
            base_url = GridlinesService.get_base_url()

            url = f"{base_url}/passport-api/fetch"

            headers = GridlinesService.get_headers()

            payload = {"file_number": (passport_number), "dob": (date_of_birth)}

            response = requests.post(url=url, headers=headers, json=payload, timeout=30)

            response_data = response.json()

            return {
                "success": True,
                "provider": "GRIDLINES",
                "verification_status": (response_data.get("status", "VERIFIED")),
                "raw_response": (response_data),
            }

        except Exception as e:
            return {"success": False, "provider": "GRIDLINES", "message": str(e)}
