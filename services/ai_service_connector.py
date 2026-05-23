import requests


class AIServiceConnector:

    BASE_URL = "http://127.0.0.1:5001/api/v1"

    @staticmethod
    def verify_ocr(extracted_data, expected_data, token):

        url = f"{AIServiceConnector.BASE_URL}/ocr/verify"

        payload = {
            "extracted_data": extracted_data,
            "expected_data": expected_data
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30
        )

        return response.json()

    @staticmethod
    def process_ocr(document_type, candidate_id, file_path, token):

        url = f"{AIServiceConnector.BASE_URL}/ocr"

        headers = {
            "Authorization": f"Bearer {token}"
        }

        files = {
            "file": open(file_path, "rb")
        }

        data = {
            "document_type": document_type,
            "candidate_id": candidate_id
        }

        response = requests.post(
            url,
            files=files,
            data=data,
            headers=headers,
            timeout=60
        )

        return response.json()