import json

from config import Config

from services.ongrid.ongrid_client import (
    OnGridClient
)

from repositories.aadhaar_repository import (
    AadhaarRepository
)


class AadhaarGenerateQRService:


    @staticmethod
    def generate_qr(

        candidate_id,
        bgv_id

    ):


        payload = {

            "template_id":

            Config.AADHAAR_TEMPLATE_ID,

            "consent":

            "Y",

            "expiry_time_in_seconds":

            300

        }


        response = (

            OnGridClient
            .post(

                "/uidai-api/ovse/generate-qr",

                payload

            )

        )


        # ==================================
        # RESPONSE VALIDATION
        # ==================================

        if not response:

            raise Exception(

                "Empty QR response"

            )


        if (

            response.get(

                "status"

            )

            !=

            200

        ):

            raise Exception(

                response.get(

                    "message",

                    "QR generation failed"

                )

            )


        if (

            response.get(

                "data",

                {}

            ).get(

                "code"

            )

            !=

            "1000"

        ):

            raise Exception(

                response.get(

                    "data",

                    {}

                ).get(

                    "message",

                    "QR generation failed"

                )

            )


        # ==================================
        # EXTRACT DATA
        # ==================================

        transaction_id = (

            response.get(

                "transaction_id"

            )

            or

            response.get(

                "data",

                {}

            ).get(

                "transaction_id"

            )

        )


        scan_uri = (

            response.get(

                "data",

                {}

            ).get(

                "scan_uri"

            )

        )


        expires_at = (

            response.get(

                "data",

                {}

            ).get(

                "expires_at"

            )

        )


        if not transaction_id:

            raise Exception(

                "Transaction ID not received"

            )


        if not scan_uri:

            raise Exception(

                "Scan URI not received"

            )


        AadhaarRepository.save_aadhaar_session(

            candidate_id=

            candidate_id,

            bgv_id=

            bgv_id,

            transaction_id=

            transaction_id,

            scan_uri=

            scan_uri,

            expires_at=

            expires_at,

            session_status=

            "PENDING",

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


        return {


            "success":

            True,


            "provider":

            "GRIDLINES",


            "transaction_id":

            transaction_id,


            "scan_uri":

            scan_uri,


            "expires_at":

            expires_at,


            "response":

            response

        }
