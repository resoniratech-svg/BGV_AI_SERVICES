import json

from datetime import datetime

from services.ongrid.ongrid_client import (
    OnGridClient
)

from repositories.ccrv_repository import (
    CCRVRepository
)


class CCRVFetchService:

    @staticmethod
    def fetch_report(
            transaction_id
    ):

        ####################################################
        # GET REQUEST
        ####################################################

        request = (

            CCRVRepository
            .get_request_by_transaction_id(

                transaction_id

            )

        )

        if not request:

            raise Exception(

                "CCRV request not found"

            )

        ####################################################
        # MARK FETCH ATTEMPTED
        ####################################################

        CCRVRepository.mark_fetch_attempted(

            transaction_id=transaction_id,

            fetch_attempted_at=datetime.now()

        )

        ####################################################
        # CALL GRIDLINES
        ####################################################

        response = (

            OnGridClient.get(

                f"/ccrv-api/fetch-report/{transaction_id}"

            )

        )

        print("=" * 80)
        print("CCRV FETCH RESPONSE")
        print(json.dumps(response, indent=4))
        print("=" * 80)

        ####################################################
        # EMPTY RESPONSE
        ####################################################

        if not response:

            raise Exception(

                "Empty CCRV Fetch response"

            )

        ####################################################
        # API FAILURE
        ####################################################

        if response.get("status") != 200:

            CCRVRepository.update_request_failed(

                transaction_id=transaction_id,

                raw_response=json.dumps(response)

            )

            raise Exception(

                response.get(

                    "message",

                    "Unable to fetch CCRV report"

                )

            )

        ####################################################
        # RESPONSE DATA
        ####################################################

        data = response.get(

            "data",

            {}

        )

        ccrv_status = data.get(

            "ccrv_status"

        )

        ####################################################
        # STILL PROCESSING
        ####################################################

        if ccrv_status in (

                "REQUESTED",

                "IN_PROGRESS"

        ):

            CCRVRepository.update_request_status(

                transaction_id=transaction_id,

                ccrv_status=ccrv_status,

                raw_response=json.dumps(response)

            )

            return {

                "completed": False,

                "ccrv_status": ccrv_status

            }

        ####################################################
        # FAILED
        ####################################################

        if ccrv_status == "FAILED":

            CCRVRepository.update_request_failed(

                transaction_id=transaction_id,

                raw_response=json.dumps(response)

            )

            return {

                "completed": False,

                "ccrv_status": "FAILED"

            }

        ####################################################
        # COMPLETED
        ####################################################

        if ccrv_status != "COMPLETED":

            raise Exception(

                "Unknown CCRV status"

            )

        ####################################################
        # AVOID DUPLICATE SAVE
        ####################################################

        if CCRVRepository.result_exists(

                request["id"]

        ):

            return {

                "completed": True,

                "message": "CCRV result already exists"

            }

        ####################################################
        # REPORT
        ####################################################

        report = data.get(

            "report",

            {}

        )

        cases = report.get(

            "cases",

            []

        )

        ####################################################
        # SAVE RESULT
        ####################################################

        ccrv_result_id = (

            CCRVRepository.save_ccrv_result(

                ccrv_request_id=request["id"],

                candidate_id=request["candidate_id"],

                bgv_id=request["bgv_id"],

                verification_status=report.get(

                    "verification_status"

                ),

                ccrv_status=ccrv_status,

                risk_level=report.get(

                    "risk_level"

                ),

                total_cases=len(cases),

                transaction_id=transaction_id,

                request_id=response.get(

                    "request_id"

                ),

                provider_name="GRIDLINES",

                api_reference_id=response.get(

                    "request_id"

                ),

                raw_response=json.dumps(response)

            )

        )

        ####################################################
        # SAVE CASES
        ####################################################

        for case in cases:

            CCRVRepository.save_case(

                ccrv_result_id=ccrv_result_id,

                case_id=case.get("case_id"),

                filing_number=case.get("filing_number"),

                cnr_number=case.get("cnr_number"),

                case_url=case.get("case_url"),

                case_code=case.get("case_code"),

                case_category=case.get("case_category"),

                case_type=case.get("case_type"),

                case_status=case.get("case_status"),

                stage_of_case=case.get("stage_of_case"),

                case_decision=case.get("case_decision"),

                criminal_act_severity=case.get(

                    "criminal_act_severity"

                ),

                individual_role=case.get(

                    "individual_role"

                ),

                court_name=case.get(

                    "court_name"

                ),

                state=case.get(

                    "state"

                ),

                district=case.get(

                    "district"

                ),

                police_station=case.get(

                    "police_station"

                ),

                filing_date=case.get(

                    "filing_date"

                ),

                registration_date=case.get(

                    "registration_date"

                ),

                hearing_date=case.get(

                    "hearing_date"

                ),

                decision_date=case.get(

                    "decision_date"

                ),

                raw_case_data=json.dumps(case)

            )

        ####################################################
        # UPDATE REQUEST
        ####################################################

        CCRVRepository.update_request_completed(

            transaction_id=transaction_id,

            raw_response=json.dumps(response),

            completed_at=datetime.now()

        )

        ####################################################
        # RETURN
        ####################################################

        return {

            "completed": True,

            "transaction_id": transaction_id,

            "total_cases": len(cases),

            "verification_status": report.get(

                "verification_status"

            ),

            "risk_level": report.get(

                "risk_level"

            )

        }