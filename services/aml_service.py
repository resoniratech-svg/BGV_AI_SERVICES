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

        verification_id = None

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
                f"/checkIndividual"
            )

            # ==========================================
            # HEADERS
            # ==========================================

            headers = {

                "x-api-key": (
                    Config.DILISENSE_API_KEY
                )
            }

            # ==========================================
            # PARAMS
            # ==========================================

            params = {

                "names": full_name,

                "fuzzy_search": 1
            }

            if country:

                params["country"] = country

            # ==========================================
            # API CALL
            # ==========================================

            response = requests.get(

                url,

                headers=headers,

                params=params,

                timeout=Config.DILISENSE_TIMEOUT
            )

            response.raise_for_status()

            response_data = (
                response.json()
            )

            # ==========================================
            # AML RESULT EXTRACTION
            # ==========================================

            matches = response_data.get(
                "matches",
                []
            )

            aml_status = (
                "MATCH_FOUND"
                if matches
                else "CLEAR"
            )

            risk_level = (
                "HIGH"
                if matches
                else "LOW"
            )

            pep_match = False

            sanctions_match = False

            adverse_media_match = False

            for match in matches:

                source_type = str(
                    match.get(
                        "source_type",
                        ""
                    )
                ).upper()

                if "PEP" in source_type:

                    pep_match = True

                if "SANCTION" in source_type:

                    sanctions_match = True

                if "CRIMINAL" in source_type:

                    adverse_media_match = True

            # ==========================================
            # SAVE RESULT
            # ==========================================

            print("WATCHLIST INSERT STARTED")

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

                provider_name="DILISENSE",

                raw_response=json.dumps(
                    response_data
                )
            )

            print("WATCHLIST INSERT EXECUTED")

            # ==========================================
            # MARK COMPLETED
            # ==========================================

            VerificationService.mark_verification_completed(

                verification_id
            )

            print("WATCHLIST INSERT COMMITTED")

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

            print("AML ERROR:", str(e))

            if verification_id:

                VerificationService.mark_verification_failed(
                    verification_id
                )

            return {

                "success": False,

                "message": (
                    "AML screening failed"
                ),

                "error": str(e)
            }

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

    @staticmethod
    def save_screening_result(

        candidate_id,
        verification_id,
        full_name,
        country,
        response_data
    ):

        WatchlistRepository.save_watchlist_result(

            candidate_id=candidate_id,

            verification_id=verification_id,

            full_name=full_name,

            country=country,

            aml_status="CLEAR",

            risk_level="LOW",

            pep_match=False,

            sanctions_match=False,

            adverse_media_match=False,

            provider_name="DILISENSE",

            raw_response=json.dumps(
                response_data
            )
        )

        VerificationService.mark_verification_completed(

            verification_id
        )