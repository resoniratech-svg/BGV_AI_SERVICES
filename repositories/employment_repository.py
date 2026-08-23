from db import get_connection


class EmploymentRepository:
    ###############################################################
    # SAVE EMPLOYMENT REQUEST
    ###############################################################
    @staticmethod
    def save_request(
        candidate_id,
        bgv_id,
        consent_id,
        provider_name,
        transaction_id,
        request_id,
        verification_status,
        api_reference_id,
        raw_response,
        requested_at,
        completed_at=None,
    ):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            query = """
            INSERT INTO employment_requests
            (
                candidate_id,
                bgv_id,
                consent_id,
                provider_name,
                transaction_id,
                request_id,
                verification_status,
                api_reference_id,
                raw_response,
                requested_at,
                completed_at
            )
            VALUES
            (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
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
                    verification_status,
                    api_reference_id,
                    raw_response,
                    requested_at,
                    completed_at,
                ),
            )
            connection.commit()
            return cursor.lastrowid
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    ###############################################################
    # GET REQUEST BY TRANSACTION ID
    ###############################################################
    @staticmethod
    def get_request_by_transaction_id(transaction_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT *
                FROM employment_requests
                WHERE transaction_id=%s
                LIMIT 1
                """,
                (transaction_id,),
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    ###############################################################
    # UPDATE REQUEST STATUS
    ###############################################################
    @staticmethod
    def update_request_status(
        transaction_id, verification_status, raw_response=None, completed_at=None
    ):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                UPDATE employment_requests
                SET
                    verification_status=%s,
                    raw_response=%s,
                    completed_at=%s,
                    updated_at=NOW()
                WHERE transaction_id=%s
                """,
                (verification_status, raw_response, completed_at, transaction_id),
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    ###############################################################
    # SAVE EMPLOYMENT RESULT
    ###############################################################
    @staticmethod
    def save_result(
        employment_request_id,
        candidate_id,
        bgv_id,
        uan,
        name,
        pan_number,
        dob,
        gender,
        mobile_number,
        email,
        masked_aadhaar_number,
        guardian_name,
        guardian_relation,
        bank_account_number,
        ifsc,
        provider_name,
        request_id,
        transaction_id,
        api_reference_id,
        raw_response,
        verified_at,
    ):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            query = """
            INSERT INTO employment_results
            (
                employment_request_id,
                candidate_id,
                bgv_id,
                uan,
                name,
                pan_number,
                dob,
                gender,
                mobile_number,
                email,
                masked_aadhaar_number,
                guardian_name,
                guardian_relation,
                bank_account_number,
                ifsc,
                provider_name,
                request_id,
                transaction_id,
                api_reference_id,
                raw_response,
                verified_at
            )
            VALUES
            (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )
            """

            cursor.execute(
                query,
                (
                    employment_request_id,
                    candidate_id,
                    bgv_id,
                    uan,
                    name,
                    pan_number,
                    dob,
                    gender,
                    mobile_number,
                    email,
                    masked_aadhaar_number,
                    guardian_name,
                    guardian_relation,
                    bank_account_number,
                    ifsc,
                    provider_name,
                    request_id,
                    transaction_id,
                    api_reference_id,
                    raw_response,
                    verified_at,
                ),
            )
            connection.commit()
            return cursor.lastrowid
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    ###############################################################
    # RESULT EXISTS
    ###############################################################
    @staticmethod
    def result_exists(employment_request_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT id
                FROM employment_results
                WHERE employment_request_id=%s
                LIMIT 1
                """,
                (employment_request_id,),
            )
            result = cursor.fetchone()
            return result is not None
        finally:
            cursor.close()
            connection.close()

    ###############################################################
    # DELETE EXISTING RESULT
    ###############################################################
    @staticmethod
    def delete_existing_result(employment_request_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            # 1. GET RESULT
            cursor.execute(
                """
                SELECT id
                FROM employment_results
                WHERE employment_request_id=%s
                LIMIT 1
                """,
                (employment_request_id,),
            )
            result = cursor.fetchone()

            if result:
                employment_result_id = result["id"]

                # 2. DELETE EMPLOYMENT HISTORY
                cursor.execute(
                    """
                    DELETE FROM employment_history_results
                    WHERE employment_result_id=%s
                    """,
                    (employment_result_id,),
                )

                # 3. DELETE EMPLOYER DETAILS
                cursor.execute(
                    """
                    DELETE FROM employment_employer_details
                    WHERE employment_result_id=%s
                    """,
                    (employment_result_id,),
                )

                # 4. DELETE RESULT
                cursor.execute(
                    """
                    DELETE FROM employment_results
                    WHERE id=%s
                    """,
                    (employment_result_id,),
                )

            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    ###############################################################
    # GET RESULT
    ###############################################################
    @staticmethod
    def get_result(candidate_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT *
                FROM employment_results
                WHERE candidate_id=%s
                ORDER BY id DESC
                LIMIT 1
                """,
                (candidate_id,),
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    ###############################################################
    # SAVE EMPLOYMENT HISTORY
    ###############################################################
    @staticmethod
    def save_history(
        employment_result_id,
        uan,
        employee_name,
        establishment_name,
        member_id,
        joining_date,
        exit_date,
        guardian_name,
        name_match_score,
        raw_history,
    ):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            query = """
            INSERT INTO employment_history_results
            (
                employment_result_id,
                uan,
                employee_name,
                establishment_name,
                member_id,
                joining_date,
                exit_date,
                guardian_name,
                name_match_score,
                raw_history
            )
            VALUES
            (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """

            cursor.execute(
                query,
                (
                    employment_result_id,
                    uan,
                    employee_name,
                    establishment_name,
                    member_id,
                    joining_date,
                    exit_date,
                    guardian_name,
                    name_match_score,
                    raw_history,
                ),
            )
            connection.commit()
            return cursor.lastrowid
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    ###############################################################
    # GET EMPLOYMENT HISTORY
    ###############################################################
    @staticmethod
    def get_history(employment_result_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT *
                FROM employment_history_results
                WHERE employment_result_id=%s
                ORDER BY joining_date ASC, id ASC
                """,
                (employment_result_id,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

    ###############################################################
    # SAVE EMPLOYER DETAILS
    ###############################################################
    @staticmethod
    def save_employer_details(
        employment_result_id,
        candidate_id,
        bgv_id,
        establishment_id,
        establishment_name,
        business_activity,
        pan_status,
        ownership_type,
        employer_status,
        date_of_setup,
        date_of_coverage,
        last_updated,
        address_line1,
        address_line2,
        city,
        district,
        state,
        pf_payment_details,
        provider_name,
        request_id,
        transaction_id,
        api_reference_id,
        raw_response,
        verified_at,
    ):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            query = """
            INSERT INTO employment_employer_details
            (
                employment_result_id,
                candidate_id,
                bgv_id,
                establishment_id,
                establishment_name,
                business_activity,
                pan_status,
                ownership_type,
                employer_status,
                date_of_setup,
                date_of_coverage,
                last_updated,
                address_line1,
                address_line2,
                city,
                district,
                state,
                pf_payment_details,
                provider_name,
                request_id,
                transaction_id,
                api_reference_id,
                raw_response,
                verified_at
            )
            VALUES
            (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            """

            cursor.execute(
                query,
                (
                    employment_result_id,
                    candidate_id,
                    bgv_id,
                    establishment_id,
                    establishment_name,
                    business_activity,
                    pan_status,
                    ownership_type,
                    employer_status,
                    date_of_setup,
                    date_of_coverage,
                    last_updated,
                    address_line1,
                    address_line2,
                    city,
                    district,
                    state,
                    pf_payment_details,
                    provider_name,
                    request_id,
                    transaction_id,
                    api_reference_id,
                    raw_response,
                    verified_at,
                ),
            )
            connection.commit()
            return cursor.lastrowid
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    ###############################################################
    # GET EMPLOYER DETAILS
    ###############################################################
    @staticmethod
    def get_employer_details(employment_result_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT *
                FROM employment_employer_details
                WHERE employment_result_id=%s
                LIMIT 1
                """,
                (employment_result_id,),
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()
