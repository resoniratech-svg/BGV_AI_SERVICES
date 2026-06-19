import json

from repositories.pan_repository import (
    PanRepository
)


class PANResultService:


    @staticmethod
    def get_pan_result(

        candidate_id

    ):


        result = (

            PanRepository
            .get_pan_verification_result(

                candidate_id

            )

        )


        if not result:

            raise Exception(

                "PAN verification result not found"

            )


        raw_response = {}

        if result.get(

            "raw_response"

        ):

            raw_response = json.loads(

                result[

                    "raw_response"

                ]

            )


        provider_error = None


        display_message = None


        if raw_response.get(

            "error"

        ):


            provider_error = (

                raw_response[

                    "error"

                ].get(

                    "message"

                )

            )


            display_message = (

                "GRIDLINES PAN Verification "

                "is not enabled for this API key"

            )


        elif (

            result[

                "verification_status"

            ]

            ==

            "APPROVED"

        ):


            display_message = (

                "PAN verification completed "

                "successfully"

            )


        elif (

            result[

                "name_match_status"

            ]

            ==

            "NOT_MATCH"

            and


            result[

                "dob_match_status"

            ]

            ==

            "MATCH"

        ):


            display_message = (

                "PAN holder name "

                "does not match"

            )


        elif (

            result[

                "name_match_status"

            ]

            ==

            "MATCH"

            and


            result[

                "dob_match_status"

            ]

            ==

            "NOT_MATCH"

        ):


            display_message = (

                "PAN holder date of birth "

                "does not match"

            )


        elif (

            result[

                "name_match_status"

            ]

            ==

            "NOT_MATCH"

            and


            result[

                "dob_match_status"

            ]

            ==

            "NOT_MATCH"

        ):


            display_message = (

                "PAN holder name and "

                "date of birth do not match"

            )


        else:


            display_message = (

                "PAN verification failed"

            )


        return {


            "verification_status":

            result[

                "verification_status"

            ],


            "provider_name":

            result[

                "provider_name"

            ],


            "name_match_status":

            result[

                "name_match_status"

            ],


            "dob_match_status":

            result[

                "dob_match_status"

            ],


            "provider_error":

            provider_error,


            "display_message":

            display_message

        }
