import json
import re

from services.ongrid.ongrid_client import (
    OnGridClient
)

from repositories.pan_repository import (
    PanRepository
)

from repositories.provider_usage_repository import (
    ProviderUsageRepository
)


class OnGridPANService:


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
    def verify_pan(

        candidate_id,
        bgv_id,
        pan_ocr_result_id,
        pan_number,
        full_name,
        date_of_birth

    ):


        payload = {

            "pan_number":

            pan_number,


            "consent":

            "Y"

        }


        response = (

            OnGridClient.post(

                "/pan-api/fetch-detailed",

                payload

            )

        )


        if not response:

            raise Exception(

                "Empty PAN response"

            )


        if response.get(

            "status"

        ) != 200:


            raise Exception(

                response.get(

                    "message",

                    "PAN verification failed"

                )

            )


        code = (

            response.get(

                "data",

                {}

            ).get(

                "code"

            )

        )


        if code != "1000":

            raise Exception(

                response.get(

                    "data",

                    {}

                ).get(

                    "message",

                    "PAN does not exist"

                )

            )


        pan_data = (

            response.get(

                "data",

                {}

            ).get(

                "pan_data",

                {}

            )

        )


        provider_pan_number = (

            pan_data.get(

                "document_id"

            )

            or

            ""

        )


        provider_full_name = (

            pan_data.get(

                "name"

            )

            or

            ""

        )


        provider_dob = (

            pan_data.get(

                "date_of_birth"

            )

            or

            ""

        )


        provider_full_name = (

            OnGridPANService

            .normalize_name(

                provider_full_name

            )

        )


        ocr_name = (

            OnGridPANService

            .normalize_name(

                full_name

            )

        )


        pan_match_status = (

            "MATCH"

            if

            pan_number.upper()

            ==

            provider_pan_number.upper()

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

        str(date_of_birth).strip()

        ==

        str(provider_dob).strip()

        else

        "NOT_MATCH"

)


        verification_status = (

            "VERIFIED"

            if (

                pan_match_status

                ==

                "MATCH"

                and


                name_match_status

                ==

                "MATCH"

                and


                dob_match_status

                ==

                "MATCH"

            )

            else

            "FAILED"

        )


        PanRepository.save_pan_verification_result(


            candidate_id=

            candidate_id,


            bgv_id=

            bgv_id,


            pan_ocr_result_id=

            pan_ocr_result_id,


            verification_status=

            verification_status,


            pan_number=

            provider_pan_number,


            full_name=

            provider_full_name,


            date_of_birth=

            provider_dob,


            pan_match_status=

            pan_match_status,


            name_match_status=

            name_match_status,


            dob_match_status=

            dob_match_status,


            provider_name=

            "GRIDLINES",


            api_reference_id=

            response.get(

                "request_id"

            ),


            raw_response=

            json.dumps(

                response

            )

        )


        ProviderUsageRepository.increment_usage(


            provider_name=

            "GRIDLINES",


            verification_type=

            "PAN"

        )


        return {


            "success":

            verification_status

            ==

            "VERIFIED",


            "verification_status":

            verification_status,


            "pan_match_status":

            pan_match_status,


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