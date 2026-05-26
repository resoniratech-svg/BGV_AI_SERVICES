import requests

from app.repositories.didit_repository import (
    DiditRepository
)
from config import Config


class DiditService:

    @staticmethod
    def create_session(
        workflow_id,
        candidate_id,
        callback_url,
        verification_type
    ):

        url = (
            f"{Config.DIDIT_BASE_URL}/v3/session/"
        )

        headers = {

            "x-api-key": Config.DIDIT_API_KEY,

            "Content-Type": "application/json"
        }

        payload = {

            "workflow_id": workflow_id,

            "vendor_data": str(candidate_id),

            "callback": Config.DIDIT_WEBHOOK_URL
        }

        response = requests.post(

            url=url,

            headers=headers,

            json=payload
        )

        result = response.json()

        # ==========================================
        # SAVE VERIFICATION SESSION
        # ==========================================

        DiditRepository.save_verification_session({

            "candidate_id": candidate_id,

            "provider_name": "DIDIT",

            "verification_type": verification_type,

            "workflow_id": workflow_id,

            "provider_session_id": result.get(
                "session_id"
            ),

            "verification_url": result.get(
                "url"
            ),

            "status": result.get(
                "status"
            )
        })

        return result