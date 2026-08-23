import json

from db import get_connection


class CourtRecordRepository:
    @staticmethod
    def save_court_record_result(
        candidate_id,
        verification_id,
        full_name,
        query_used,
        total_cases,
        case_found,
        court_name,
        case_title,
        document_id,
        judgment_date,
        risk_level,
        provider_name,
        raw_response,
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO court_record_results (

                candidate_id,
                verification_id,
                full_name,
                search_query,
                total_matches,
                match_found,
                court_name,
                case_title,
                document_id,
                judgment_date,
                risk_level,
                provider_name,
                raw_response

            )

            VALUES (

                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """

        values = (
            candidate_id,
            verification_id,
            full_name,
            query_used,
            total_cases,
            case_found,
            court_name,
            case_title,
            document_id,
            judgment_date,
            risk_level,
            provider_name,
            json.dumps(raw_response),
        )

        cursor.execute(query, values)

        connection.commit()

        cursor.close()

        connection.close()

    @staticmethod
    def save_court_record_log(
        candidate_id, request_url, request_headers, response_data, status_code
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO api_logs (

                module_name,
                provider_name,
                endpoint,
                request_payload,
                response_payload,
                response_status_code,
                status,
                api_name

            )

            VALUES (

                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """

        payload = {"candidate_id": candidate_id, "headers": request_headers}

        values = (
            "COURT_RECORD_VERIFICATION",
            "Indian Kanoon",
            request_url,
            json.dumps(payload),
            json.dumps(response_data),
            status_code,
            "SUCCESS",
            "Court Record Search",
        )

        cursor.execute(query, values)

        connection.commit()

        cursor.close()

        connection.close()
