import requests
from config import Config


class OnGridClient:
    @staticmethod
    def post(endpoint, payload):
        headers = {
            "X-API-Key": Config.GRIDLINES_API_KEY,
            "X-Auth-Type": "API-Key",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        try:
            response = requests.post(
                f"{Config.GRIDLINES_PRODUCTION_URL}{endpoint}",
                headers=headers,
                json=payload,
                timeout=60,
            )
        except Exception as e:
            return {
                "success": False,
                "status": 500,
                "request_id": None,
                "raw_response": str(e),
            }

        if not response.ok:
            print("=" * 80)
            print("GRIDLINES ERROR RESPONSE")
            print("STATUS =", response.status_code)
            print("BODY =", response.text)
            print("=" * 80)

            return {
                "success": False,
                "status": response.status_code,
                "request_id": None,
                "raw_response": response.text,
            }

        try:
            return response.json()
        except Exception:
            return {
                "success": False,
                "status": response.status_code,
                "request_id": None,
                "raw_response": response.text,
            }

    @staticmethod
    def get(endpoint, headers=None):
        request_headers = {
            "X-API-Key": Config.GRIDLINES_API_KEY,
            "X-Auth-Type": "API-Key",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if headers:
            request_headers.update(headers)

        try:
            response = requests.get(
                f"{Config.GRIDLINES_PRODUCTION_URL}{endpoint}",
                headers=request_headers,
                timeout=60,
            )
        except Exception as e:
            return {
                "success": False,
                "status": 500,
                "request_id": None,
                "raw_response": str(e),
            }

        if not response.ok:
            print("=" * 80)
            print("GRIDLINES ERROR RESPONSE")
            print("STATUS =", response.status_code)
            print("BODY =", response.text)
            print("=" * 80)

            return {
                "success": False,
                "status": response.status_code,
                "request_id": None,
                "raw_response": response.text,
            }

        try:
            return response.json()
        except Exception:
            return {
                "success": False,
                "status": response.status_code,
                "request_id": None,
                "raw_response": response.text,
            }

    @staticmethod
    def post_multipart(endpoint, files, data=None):
        headers = {
            "X-API-Key": Config.GRIDLINES_API_KEY,
            "X-Auth-Type": "API-Key",
            "Accept": "application/json",
        }

        try:
            response = requests.post(
                f"{Config.GRIDLINES_PRODUCTION_URL}{endpoint}",
                headers=headers,
                files=files,
                data=data,
                timeout=60,
            )

            print("=" * 80)
            print("GRIDLINES MULTIPART RESPONSE")
            print("ENDPOINT =", endpoint)
            print("STATUS =", response.status_code)
            print("BODY =", response.text)
            print("=" * 80)

        except Exception as e:
            print("=" * 80)
            print("GRIDLINES MULTIPART CONNECTION ERROR")
            print(e)
            print("=" * 80)

            return {
                "success": False,
                "status": 500,
                "message": str(e),
            }

        if not response.ok:
            return {
                "success": False,
                "status": response.status_code,
                "message": response.text,
                "raw_response": response.text,
            }

        try:
            body = response.text.strip()

            if not body:
                return {
                    "success": False,
                    "status": response.status_code,
                    "message": "Empty response body",
                }

            return response.json()

        except Exception as e:
            print("=" * 80)
            print("GRIDLINES JSON PARSE ERROR")
            print(e)
            print("RAW BODY")
            print(response.text)
            print("=" * 80)

            return {
                "success": False,
                "status": response.status_code,
                "message": response.text,
            }
