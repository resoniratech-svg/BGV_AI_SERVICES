import os
import requests

from config import Config


class DiditService:

    @staticmethod
    def verify_passport_document(

        candidate_id,
        bgv_id,
        document_path
    ):

        # ======================================
        # VALIDATE FILE
        # ======================================

        if not os.path.exists(

            document_path
        ):

            return {

                "success": False,

                "verification_status": (
                    "FAILED"
                ),

                "message": (
                    "Passport document not found"
                )
            }

        # ======================================
        # DIDIT API ENDPOINT
        # ======================================

        url = (
            f"{Config.DIDIT_BASE_URL}"
        )

        # ======================================
        # HEADERS
        # ======================================

        headers = {

            "x-api-key": (
                Config.DIDIT_API_KEY
            )
        }

        # ======================================
        # FILE UPLOAD
        # ======================================

        files = {

            "document": open(
                document_path,
                "rb"
            )
        }

        # ======================================
        # METADATA
        # ======================================

        data = {

            "candidate_id": (
                candidate_id
            ),

            "bgv_id": (
                bgv_id
            ),

            "document_type": (
                "PASSPORT"
            )
        }

        # ======================================
        # PROVIDER API CALL
        # ======================================

        try:

            response = requests.post(

                url=url,

                headers=headers,

                files=files,

                data=data,

                timeout=60
            )

            print("STATUS:", response.status_code)
            print("RESPONSE:", response.text)

            result = response.json()

        except Exception as e:

            return {

                "success": False,

                "verification_status": (
                    "FAILED"
                ),

                "message": str(e)
            }

        # ======================================
        # NORMALIZED RESPONSE
        # ======================================

        return {

            "success": True,

            "verification_status": (
                result.get(
                    "status",
                    "VERIFIED"
                )
            ),

            "passport_number": (
                result.get(
                    "passport_number"
                )
            ),

            "full_name": (
                result.get(
                    "full_name"
                )
            ),

            "nationality": (
                result.get(
                    "nationality"
                )
            ),

            "country": (
                result.get(
                    "country"
                )
            ),

            "date_of_birth": (
                result.get(
                    "date_of_birth"
                )
            ),

            "issue_date": (
                result.get(
                    "issue_date"
                )
            ),

            "expiry_date": (
                result.get(
                    "expiry_date"
                )
            ),

            "raw_response": result
        }