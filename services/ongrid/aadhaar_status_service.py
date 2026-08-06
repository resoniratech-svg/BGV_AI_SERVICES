import json

from services.ongrid.ongrid_client import OnGridClient

from repositories.aadhaar_repository import AadhaarRepository


class AadhaarStatusService:
    @staticmethod
    def fetch_status(candidate_id):

        session = AadhaarRepository.get_aadhaar_session(candidate_id)

        # ==================================
        # SESSION NOT FOUND
        # ==================================

        if not session:
            return {"success": True, "status": "NOT_STARTED"}

        # ==================================
        # CONSENT ALREADY COMPLETED
        # ==================================

        if session["session_status"] == "SUCCESS":
            return {
                "success": True,
                "status": "SUCCESS",
                "response": json.loads(session["raw_response"]),
            }

        transaction_id = session["transaction_id"]

        response = OnGridClient.get(
            "/uidai-api/ovse/status", headers={"X-Transaction-ID": transaction_id}
        )

        # ==================================
        # RESPONSE VALIDATION
        # ==================================

        if not response:
            raise Exception("Empty OVSE response")

        if response.get("status") == 429:
            return {
                "success": False,
                "status": "PENDING",
                "message": "Waiting for consent",
            }

        if response.get("status") != 200:
            raise Exception(response.get("message", "OVSE fetch failed"))

        code = response.get("data", {}).get("code")

        # ==================================
        # CALLBACK RECEIVED
        # ==================================

        if code == "1001":
            AadhaarRepository.update_session_status(
                transaction_id=transaction_id,
                session_status="SUCCESS",
                raw_response=json.dumps(response),
            )

            return {"success": True, "status": "SUCCESS", "response": response}

        # ==================================
        # WAITING FOR CONSENT
        # ==================================

        if code == "1002":
            AadhaarRepository.update_session_status(
                transaction_id=transaction_id,
                session_status="PENDING",
                raw_response=json.dumps(response),
            )

            return {"success": False, "status": "PENDING", "response": response}

        # ==================================
        # CONSENT DENIED
        # ==================================

        if code == "1004":
            AadhaarRepository.update_session_status(
                transaction_id=transaction_id,
                session_status="REJECTED",
                raw_response=json.dumps(response),
            )

            return {"success": False, "status": "REJECTED", "response": response}

        return {"success": False, "status": "UNKNOWN", "response": response}
