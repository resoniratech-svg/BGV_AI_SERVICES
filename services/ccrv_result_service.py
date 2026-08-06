from datetime import datetime, timedelta

from repositories.ccrv_repository import (
    CCRVRepository
)

from services.ongrid.ccrv_fetch_service import (
    CCRVFetchService
)


class CCRVResultService:

    @staticmethod
    def get_result(candidate_id):

        ####################################################
        # Latest CCRV Request
        ####################################################

        request = (

            CCRVRepository
            .get_latest_request(
                candidate_id
            )

        )

        if not request:

            raise Exception(

                "CCRV request not found"

            )

        ####################################################
        # Already completed
        ####################################################

        if request["ccrv_status"] == "COMPLETED":

            result = (

                CCRVRepository
                .get_result(
                    request["id"]
                )

            )

            if not result:

                return {

                    "success": False,

                    "verification_status": "COMPLETED",

                    "display_message":
                    "Verification completed. Report is being processed."

                }

            cases = (

                CCRVRepository
                .get_cases(
                    result["id"]
                )

            )

            return {

                "success": True,

                "verification_status": "COMPLETED",

                "display_message":
                "CCRV verification completed successfully.",

                "report": result,

                "cases": cases

            }

        ####################################################
        # Still processing
        ####################################################

        now = datetime.now()

        expected_completion = request.get(

            "expected_completion_at"

        )

        if expected_completion:

            if isinstance(expected_completion, str):

                expected_completion = datetime.strptime(

                    expected_completion,

                    "%Y-%m-%d %H:%M:%S"

                )

        ####################################################
        # Fetch only once
        ####################################################

        if (

            expected_completion

            and

            now >= expected_completion + timedelta(hours=1)

            and

            request["fetch_attempted"] == 0

        ):

            try:

                CCRVFetchService.fetch_report(

                    candidate_id=candidate_id,

                    transaction_id=request["transaction_id"]

                )

            except Exception as e:

                print(e)

            request = (

                CCRVRepository
                .get_latest_request(
                    candidate_id
                )

            )

            ####################################################
            # Completed after fetch
            ####################################################

            if request["ccrv_status"] == "COMPLETED":

                result = (

                    CCRVRepository
                    .get_result(
                        request["id"]
                    )

                )

                cases = (

                    CCRVRepository
                    .get_cases(
                        result["id"]
                    )

                )

                return {

                    "success": True,

                    "verification_status": "COMPLETED",

                    "display_message":
                    "CCRV verification completed successfully.",

                    "report": result,

                    "cases": cases

                }

        ####################################################
        # REQUESTED / IN_PROGRESS
        ####################################################

        return {

            "success": False,

            "verification_status":

            request["ccrv_status"],

            "display_message":

            "CCRV verification is in progress."

        }