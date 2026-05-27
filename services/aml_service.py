import json
import requests
from config import Config

from repositories.watchlist_repository import (
    WatchlistRepository
)

from services.verification_service import (
    VerificationService
)


class AMLService:

    @staticmethod
    def screen_candidate(

        candidate_id,
        full_name,
        country
    ):

        try:

            # ==========================================
            # CREATE VERIFICATION SESSION
            # ==========================================

            verification_id = (
                VerificationService
                .initiate_watchlist_verification(
                    candidate_id
                )
            )

            # ==========================================
            # API URL
            # ==========================================

            url = (
                f"{Config.DILISENSE_BASE_URL}"
            )

            # ==========================================
            # HEADERS
            # ==========================================

            headers = {

                "Authorization": (
                    f"Bearer "
                    f"{Config.DILISENSE_API_KEY}"
                ),

                "Content-Type": (
                    "application/json"
                )
            }

            # ==========================================
            # PAYLOAD
            # ==========================================

            payload = {

                "name": full_name,

                "country": country
            }

            # ==========================================
            # API CALL
            # ==========================================

            response = requests.post(

                url,

                headers=headers,

                json=payload,

                timeout=Config.DILISENSE_TIMEOUT
            )

            response_data = (
                response.json()
            )

            # ==========================================
            # SAMPLE EXTRACTION
            # ==========================================

            aml_status = "CLEAR"

            risk_level = "LOW"

            pep_match = False

            sanctions_match = False

            adverse_media_match = False

            # ==========================================
            # SAVE RESULT
            # ==========================================

            WatchlistRepository.save_watchlist_result(

                candidate_id=candidate_id,

                verification_id=verification_id,

                full_name=full_name,

                country=country,

                aml_status=aml_status,

                risk_level=risk_level,

                pep_match=pep_match,

                sanctions_match=sanctions_match,

                adverse_media_match=adverse_media_match,

                provider_name="Dilisense",

                raw_response=json.dumps(
                    response_data
                )
            )

            # ==========================================
            # MARK COMPLETED
            # ==========================================

            VerificationService.mark_verification_completed(

                verification_id
            )

            # ==========================================
            # FINAL RESPONSE
            # ==========================================

            return {

                "success": True,

                "candidate_id": (
                    candidate_id
                ),

                "verification_id": (
                    verification_id
                ),

                "aml_status": aml_status,

                "risk_level": risk_level,

                "pep_match": pep_match,

                "sanctions_match": sanctions_match,

                "adverse_media_match": (
                    adverse_media_match
                ),

                "provider_response": (
                    response_data
                )
            }

        except Exception as e:

            return {

                "success": False,

                "message": (
                    "AML screening failed"
                ),

                "error": str(e)
            }
    import requests




class AMLService:

    @staticmethod
    def screen_individual(

        full_name,
        dob=None,
        gender=None
    ):

        url = (
            f"{Config.DILISENSE_BASE_URL}"
            f"/checkIndividual"
        )

        headers = {

            "x-api-key": (
                Config.DILISENSE_API_KEY
            )
        }

        params = {

            "names": full_name,

            "fuzzy_search": 1
        }

        if dob:

            params["dob"] = dob

        if gender:

            params["gender"] = gender

        response = requests.get(

            url,

            headers=headers,

            params=params,

            timeout=30
        )

        response.raise_for_status()

        return response.json()