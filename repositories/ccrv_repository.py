from datetime import datetime

from db import get_connection


class CCRVRepository:
    # =====================================================
    # SAVE CCRV REQUEST
    # =====================================================
    @staticmethod
    def save_request(
        candidate_id,
        bgv_id,
        consent_id,
        provider_name,
        transaction_id,
        request_id,
        ccrv_status,
        api_reference_id,
        raw_response,
        requested_at,
        expected_completion_at,
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        INSERT INTO ccrv_requests
        (
            candidate_id,
            bgv_id,
            consent_id,
            provider_name,
            transaction_id,
            request_id,
            ccrv_status,
            api_reference_id,
            raw_response,
            requested_at,
            expected_completion_at,
            fetch_attempted,
            fetch_attempted_at
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,0,NULL
        )
        """

        cursor.execute(
            query,
            (
                candidate_id,
                bgv_id,
                consent_id,
                provider_name,
                transaction_id,
                request_id,
                ccrv_status,
                api_reference_id,
                raw_response,
                requested_at,
                expected_completion_at,
            ),
        )

        connection.commit()

        request_id_db = cursor.lastrowid

        cursor.close()

        connection.close()

        return request_id_db

    # =====================================================
    # GET LATEST REQUEST
    # =====================================================
    @staticmethod
    def get_latest_request(candidate_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """

            SELECT *

            FROM ccrv_requests

            WHERE candidate_id=%s

            ORDER BY id DESC

            LIMIT 1

            """,
            (candidate_id,),
        )

        result = cursor.fetchone()

        cursor.close()

        connection.close()

        return result

    # =====================================================
    # GET REQUEST USING TRANSACTION ID
    # =====================================================
    @staticmethod
    def get_request_by_transaction_id(transaction_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """

            SELECT *

            FROM ccrv_requests

            WHERE transaction_id=%s

            LIMIT 1

            """,
            (transaction_id,),
        )

        result = cursor.fetchone()

        cursor.close()

        connection.close()

        return result

    # =====================================================
    # UPDATE REQUEST STATUS
    # =====================================================
    @staticmethod
    def update_request_status(
        transaction_id, ccrv_status, raw_response=None, completed_at=None
    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """

            UPDATE ccrv_requests

            SET

                ccrv_status=%s,

                raw_response=%s,

                completed_at=%s

            WHERE transaction_id=%s

            """,
            (ccrv_status, raw_response, completed_at, transaction_id),
        )

        connection.commit()

        cursor.close()

        connection.close()

    # =====================================================
    # MARK FETCH ATTEMPTED
    # =====================================================
    @staticmethod
    def mark_fetch_attempted(transaction_id, fetch_attempted_at):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """

            UPDATE ccrv_requests

            SET

                fetch_attempted=1,

                fetch_attempted_at=%s

            WHERE transaction_id=%s

            """,
            (fetch_attempted_at, transaction_id),
        )

        connection.commit()

        cursor.close()

        connection.close()

    # =====================================================
    # UPDATE REQUEST COMPLETED
    # =====================================================
    @staticmethod
    def update_request_completed(transaction_id, raw_response, completed_at):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """

            UPDATE ccrv_requests

            SET

                ccrv_status='COMPLETED',

                raw_response=%s,

                completed_at=%s

            WHERE transaction_id=%s

            """,
            (raw_response, completed_at, transaction_id),
        )

        connection.commit()

        cursor.close()

        connection.close()

    # =====================================================
    # UPDATE REQUEST FAILED
    # =====================================================
    @staticmethod
    def update_request_failed(transaction_id, raw_response):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """

            UPDATE ccrv_requests

            SET

                ccrv_status='FAILED',

                raw_response=%s

            WHERE transaction_id=%s

            """,
            (raw_response, transaction_id),
        )

        connection.commit()

        cursor.close()

        connection.close()

    # =====================================================
    # DELETE EXISTING RESULT
    # =====================================================
    @staticmethod
    def delete_existing_result(ccrv_request_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """

            SELECT id

            FROM ccrv_results

            WHERE ccrv_request_id=%s

            LIMIT 1

            """,
            (ccrv_request_id,),
        )

        result = cursor.fetchone()

        if result:
            ccrv_result_id = result["id"]

            cursor.execute(
                """

                DELETE FROM ccrv_case_results

                WHERE ccrv_result_id=%s

                """,
                (ccrv_result_id,),
            )

            cursor.execute(
                """

                DELETE FROM ccrv_results

                WHERE id=%s

                """,
                (ccrv_result_id,),
            )

        connection.commit()

        cursor.close()

        connection.close()

        # =====================================================

    # SAVE CCRV RESULT
    # =====================================================
    @staticmethod
    def save_ccrv_result(
        ccrv_request_id,
        candidate_id,
        bgv_id,
        verification_status,
        ccrv_status,
        risk_level,
        total_cases,
        transaction_id,
        request_id,
        provider_name,
        api_reference_id,
        raw_response,
        verified_at=None,
    ):

        ####################################################
        # DEFAULT VERIFIED TIME
        ####################################################

        if verified_at is None:
            verified_at = datetime.now()

        ####################################################
        # CONNECTION
        ####################################################

        connection = get_connection()

        cursor = connection.cursor()

        query = """

        INSERT INTO ccrv_results
        (

            ccrv_request_id,
            candidate_id,
            bgv_id,
            verification_status,
            ccrv_status,
            risk_level,
            total_cases,
            transaction_id,
            request_id,
            provider_name,
            api_reference_id,
            raw_response,
            verified_at

        )

        VALUES
        (

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
            ccrv_request_id,
            candidate_id,
            bgv_id,
            verification_status,
            ccrv_status,
            risk_level,
            total_cases,
            transaction_id,
            request_id,
            provider_name,
            api_reference_id,
            raw_response,
            verified_at,
        )

        cursor.execute(query, values)

        connection.commit()

        ccrv_result_id = cursor.lastrowid

        cursor.close()

        connection.close()

        return ccrv_result_id

    # =====================================================
    # RESULT EXISTS
    # =====================================================
    @staticmethod
    def result_exists(ccrv_request_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """

            SELECT id

            FROM ccrv_results

            WHERE ccrv_request_id=%s

            LIMIT 1

            """,
            (ccrv_request_id,),
        )

        result = cursor.fetchone()

        cursor.close()

        connection.close()

        return result is not None

    # =====================================================
    # GET CCRV RESULT
    # =====================================================
    @staticmethod
    def get_result(ccrv_request_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """

            SELECT *

            FROM ccrv_results

            WHERE ccrv_request_id=%s

            ORDER BY id DESC

            LIMIT 1

            """,
            (ccrv_request_id,),
        )

        result = cursor.fetchone()

        cursor.close()

        connection.close()

        return result

    # =====================================================
    # SAVE CCRV CASE
    # =====================================================
    @staticmethod
    def save_case(
        ccrv_result_id,
        case_id,
        filing_number,
        cnr_number,
        case_url,
        case_code,
        case_category,
        case_type,
        case_status,
        stage_of_case,
        case_decision,
        criminal_act_severity,
        individual_role,
        court_name,
        state,
        district,
        police_station,
        filing_date,
        registration_date,
        hearing_date,
        decision_date,
        raw_case_data,
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """

        INSERT INTO ccrv_case_results
        (

            ccrv_result_id,
            case_id,
            filing_number,
            cnr_number,
            case_url,
            case_code,
            case_category,
            case_type,
            case_status,
            stage_of_case,
            case_decision,
            criminal_act_severity,
            individual_role,
            court_name,
            state,
            district,
            police_station,
            filing_date,
            registration_date,
            hearing_date,
            decision_date,
            raw_case_data

        )

        VALUES
        (

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
            ccrv_result_id,
            case_id,
            filing_number,
            cnr_number,
            case_url,
            case_code,
            case_category,
            case_type,
            case_status,
            stage_of_case,
            case_decision,
            criminal_act_severity,
            individual_role,
            court_name,
            state,
            district,
            police_station,
            filing_date,
            registration_date,
            hearing_date,
            decision_date,
            raw_case_data,
        )

        cursor.execute(query, values)

        connection.commit()

        cursor.close()

        connection.close()

    # =====================================================
    # GET CCRV CASES
    # =====================================================
    @staticmethod
    def get_cases(ccrv_result_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """

            SELECT *

            FROM ccrv_case_results

            WHERE ccrv_result_id=%s

            ORDER BY id

            """,
            (ccrv_result_id,),
        )

        results = cursor.fetchall()

        cursor.close()

        connection.close()

        return results
