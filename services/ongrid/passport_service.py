import json
import re

from services.ongrid.ongrid_client import (
    OnGridClient
)

from repositories.passport_repository import (
    PassportRepository
)

from repositories.provider_usage_repository import (
    ProviderUsageRepository
)


class OnGridPassportService:


    @staticmethod
    def normalize_name(value):

        if not value:
            return ""

        value = value.upper()

        value = re.sub(
            r"\s+",
            " ",
            value
        )

        return value.strip()


    @staticmethod
    def verify_passport(

        candidate_id,
        bgv_id,

        passport_ocr_result_id,

        passport_number,
        file_number,

        given_name,
        surname,

        date_of_birth,

        issue_date,
        expiry_date,

        nationality,
        country

    ):

        ####################################################
        # FETCH PAYLOAD
        ####################################################

        payload = {

            "file_number": file_number,

            "date_of_birth": date_of_birth,

            "consent": "Y"

        }

        print("=" * 80)
        print("GRIDLINES PASSPORT FETCH PAYLOAD")
        print(payload)
        print("=" * 80)

        response = OnGridClient.post(

            "/passport-api/fetch",

            payload

        )

        ####################################################
        # RESPONSE VALIDATION
        ####################################################

        if not response:

            raise Exception(

                "Empty Passport Fetch response"

            )

        if response.get("status") != 200:

            raise Exception(

                response.get(

                    "message",

                    "Passport Fetch failed"

                )

            )

        if (

            response
            .get("data", {})
            .get("code")

        ) != "1006":

            raise Exception(

                response
                .get("data", {})
                .get(

                    "message",

                    "Passport not found"

                )

            )

        ####################################################
        # PROVIDER DATA
        ####################################################

        passport_data = (

            response

            .get(

                "data",

                {}

            )

            .get(

                "passport_data",

                {}

            )

        )

        provider_passport_number = (

            passport_data.get(

                "document_id"

            )

            or ""

        )

        provider_first_name = (

            passport_data.get(

                "first_name"

            )

            or ""

        )

        provider_last_name = (

            passport_data.get(

                "last_name"

            )

            or ""

        )

        provider_dob = (

            passport_data.get(

                "date_of_birth"

            )

            or ""

        )

        provider_issue_date = (

            passport_data.get(

                "issue_date"

            )

            or ""

        )

        ####################################################
        # NAME NORMALIZATION
        ####################################################

        ocr_name = (

            OnGridPassportService

            .normalize_name(

                f"{given_name} {surname}"

            )

        )

        provider_full_name = (

            OnGridPassportService

            .normalize_name(

                f"{provider_first_name} {provider_last_name}"

            )

        )

        ####################################################
        # COMPARISON
        ####################################################

        passport_match_status = (

            "MATCH"

            if

            passport_number.upper()

            ==

            provider_passport_number.upper()

            else

            "NOT_MATCH"

        )

        name_match_status = (

            "MATCH"

            if

            ocr_name

            ==

            provider_full_name

            else

            "NOT_MATCH"

        )

        dob_match_status = (

            "MATCH"

            if

            date_of_birth

            ==

            provider_dob

            else

            "NOT_MATCH"

        )

        ####################################################
        # FINAL STATUS
        ####################################################

        verification_status = (

            "VERIFIED"

            if (

                passport_match_status == "MATCH"

                and

                name_match_status == "MATCH"

                and

                dob_match_status == "MATCH"

            )

            else

            "FAILED"

        )

        ####################################################
        # SAVE RESULT
        ####################################################

        PassportRepository.save_passport_result(

            candidate_id=candidate_id,

            bgv_id=bgv_id,

            passport_ocr_result_id=passport_ocr_result_id,

            verification_status=verification_status,

            passport_number=provider_passport_number,

            full_name=provider_full_name,

            nationality=nationality,

            country=country,

            date_of_birth=provider_dob,

            issue_date=provider_issue_date,

            expiry_date=expiry_date,

            passport_match_status=passport_match_status,

            name_match_status=name_match_status,

            dob_match_status=dob_match_status,

            provider_name="GRIDLINES",

            api_reference_id=response.get(

                "request_id"

            ),

            raw_response=json.dumps(

                response

            )

        )

        ####################################################
        # PROVIDER USAGE
        ####################################################

        ProviderUsageRepository.increment_usage(

            provider_name="GRIDLINES",

            verification_type="PASSPORT"

        )

        ####################################################
        # RETURN
        ####################################################

        return {

            "success":

            verification_status == "VERIFIED",

            "verification_status":

            verification_status,

            "passport_match_status":

            passport_match_status,

            "name_match_status":

            name_match_status,

            "dob_match_status":

            dob_match_status,

            "provider":

            "GRIDLINES",

            "request_id":

            response.get(

                "request_id"

            ),

            "response":

            response

        }