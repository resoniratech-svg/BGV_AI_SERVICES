import json
import requests

from config import Config

from repositories.watchlist_repository import (
    WatchlistRepository
)




class AMLService:

    @staticmethod
    def screen_watchlist(
    candidate_id,
    full_name,
    dob=None,
    gender=None
):

        verification_id = None

        try:

            # ==========================================
            # CREATE VERIFICATION SESSION
            # ==========================================
            verification_id = None

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

            if dob:

                params["dob"] = dob

            if gender:

                params["gender"] = gender

            # ==========================================
            # API CALL
            # ==========================================
            print("DILISENSE PARAMS")
            print(params)
            response = requests.get(

                url,

                headers=headers,

                params=params,

                timeout=Config.DILISENSE_TIMEOUT
            )

            print("STATUS CODE:")
            print(response.status_code)

            print("RAW RESPONSE:")
            print(response.text)

            response.raise_for_status()

            response_data = response.json()
                        
            # --- DEBUGGING FOR ISSUE 2 ---
            print("DILISENSE RESPONSE:")
            print(json.dumps(response_data, indent=2))

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
            # SAVE AML SCREENING RESULT
            # ==========================================

            WatchlistRepository.save_aml_screening_result(

                candidate_id=candidate_id,

                verification_id=verification_id,

                full_name=full_name,
                country=None,
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

            # ==========================================
            # SAVE GLOBAL WATCHLIST RESULT
            # ==========================================

            WatchlistRepository.save_global_watchlist_result(

                candidate_id=candidate_id,

                verification_id=verification_id,

                full_name=full_name,
                country=None,
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

            # ==========================================
            # MARK COMPLETED
            # ==========================================

            

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
        print("DILISENSE PARAMS")
        print(params)
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
        response_data,
        country=None
    ):

        WatchlistRepository.save_aml_screening_result(

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

        WatchlistRepository.save_global_watchlist_result(

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

        