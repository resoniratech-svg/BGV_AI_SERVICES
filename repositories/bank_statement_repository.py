from db import get_connection


class BankStatementRepository:
    ###############################################################
    # GET UPLOADED BANK STATEMENT
    ###############################################################
    @staticmethod
    def get_uploaded_bank_statement(candidate_id, bgv_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT
                    id,
                    candidate_id,
                    bgv_id,
                    document_type,
                    original_filename,
                    stored_filename,
                    file_path,
                    mime_type,
                    file_size,
                    upload_status,
                    verification_status,
                    uploaded_at
                FROM candidate_uploaded_documents
                WHERE candidate_id=%s
                    AND bgv_id=%s
                    AND document_type='BANK_STATEMENT_ANALYZER'
                    AND upload_status='UPLOADED'
                ORDER BY id DESC
                LIMIT 1
                """,
                (candidate_id, bgv_id),
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    ###############################################################
    # GET BANK STATEMENT CONSENT
    ###############################################################
    @staticmethod
    def get_bank_statement_consent(candidate_id, bgv_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT
                    id,
                    candidate_id,
                    bgv_id,
                    verification_type,
                    consent_status,
                    created_at
                FROM candidate_consents
                WHERE candidate_id=%s
                    AND bgv_id=%s
                    AND verification_type='bank_statement_analyzer'
                    AND consent_status='GIVEN'
                ORDER BY id DESC
                LIMIT 1
                """,
                (candidate_id, bgv_id),
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    ###############################################################
    # SAVE BANK STATEMENT REQUEST
    ###############################################################
    @staticmethod
    def save_request(
        candidate_id,
        bgv_id,
        document_id,
        provider,
        transaction_id,
        provider_request_id,
        request_status,
        provider_status_code,
        request_payload,
        response_payload,
        completed_at=None,
    ):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            query = """
            INSERT INTO bank_statement_requests
            (
                candidate_id,
                bgv_id,
                document_id,
                provider,
                transaction_id,
                provider_request_id,
                request_status,
                provider_status_code,
                request_payload,
                response_payload,
                completed_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (
                    candidate_id,
                    bgv_id,
                    document_id,
                    provider,
                    transaction_id,
                    provider_request_id,
                    request_status,
                    provider_status_code,
                    request_payload,
                    response_payload,
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
                SELECT
                    id,
                    candidate_id,
                    bgv_id,
                    document_id,
                    provider,
                    transaction_id,
                    provider_request_id,
                    request_status,
                    provider_status_code,
                    request_payload,
                    response_payload,
                    created_at,
                    updated_at,
                    completed_at
                FROM bank_statement_requests
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
    # CHECK WHETHER REQUEST IS ALREADY COMPLETED
    ###############################################################
    @staticmethod
    def is_request_completed(transaction_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT request_status
                FROM bank_statement_requests
                WHERE transaction_id=%s
                LIMIT 1
                """,
                (transaction_id,),
            )
            row = cursor.fetchone()
            if not row:
                return False
            return row["request_status"] == "COMPLETED"
        finally:
            cursor.close()
            connection.close()

    ###############################################################
    # UPDATE REQUEST STATUS
    ###############################################################
    @staticmethod
    def update_request_status(
        transaction_id,
        request_status,
        provider_status_code=None,
        response_payload=None,
        completed_at=None,
        provider_request_id=None,
    ):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                UPDATE bank_statement_requests
                SET
                    provider_request_id = COALESCE(%s, provider_request_id),
                    request_status = %s,
                    provider_status_code = COALESCE(%s, provider_status_code),
                    response_payload = COALESCE(%s, response_payload),
                    completed_at = COALESCE(%s, completed_at),
                    updated_at = NOW()
                WHERE transaction_id = %s
                """,
                (
                    provider_request_id,
                    request_status,
                    provider_status_code,
                    response_payload,
                    completed_at,
                    transaction_id,
                ),
            )
            connection.commit()
            return cursor.rowcount
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    ###############################################################
    # SAVE BANK STATEMENT RESULT
    ###############################################################
    @staticmethod
    def save_result(
        request_id,
        candidate_id,
        bgv_id,
        provider,
        transaction_id,
        provider_request_id,
        provider_status_code,
        provider_json_url,
        provider_excel_url,
        json_file_path,
        excel_file_path,
        report_generated_at,
    ):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            query = """
            INSERT INTO bank_statement_results
            (
                request_id,
                candidate_id,
                bgv_id,
                provider,
                transaction_id,
                provider_request_id,
                provider_status_code,
                provider_json_url,
                provider_excel_url,
                json_file_path,
                excel_file_path,
                report_generated_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (
                    request_id,
                    candidate_id,
                    bgv_id,
                    provider,
                    transaction_id,
                    provider_request_id,
                    provider_status_code,
                    provider_json_url,
                    provider_excel_url,
                    json_file_path,
                    excel_file_path,
                    report_generated_at,
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
    # CHECK WHETHER RESULT EXISTS
    ###############################################################
    @staticmethod
    def result_exists(request_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT id
                FROM bank_statement_results
                WHERE request_id=%s
                LIMIT 1
                """,
                (request_id,),
            )
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            connection.close()

    ###############################################################
    # DELETE EXISTING RESULT
    ###############################################################
    @staticmethod
    def delete_existing_result(request_id):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM bank_statement_results
                WHERE request_id=%s
                """,
                (request_id,),
            )
            connection.commit()
            return cursor.rowcount
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    ###############################################################
    # UPDATE BANK STATEMENT RESULT
    ###############################################################
    @staticmethod
    def update_result(
        request_id,
        transaction_id,
        provider_request_id,
        provider_status_code,
        provider_json_url,
        provider_excel_url,
        json_file_path,
        excel_file_path,
        report_generated_at,
    ):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                UPDATE bank_statement_results
                SET
                    transaction_id=%s,
                    provider_request_id=%s,
                    provider_status_code=%s,
                    provider_json_url=%s,
                    provider_excel_url=%s,
                    json_file_path=%s,
                    excel_file_path=%s,
                    report_generated_at=%s,
                    updated_at=NOW()
                WHERE request_id=%s
                """,
                (
                    transaction_id,
                    provider_request_id,
                    provider_status_code,
                    provider_json_url,
                    provider_excel_url,
                    json_file_path,
                    excel_file_path,
                    report_generated_at,
                    request_id,
                ),
            )
            connection.commit()
            return cursor.rowcount
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    ###############################################################
    # GET BANK STATEMENT RESULT
    ###############################################################
    @staticmethod
    def get_result(candidate_id, bgv_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT
                    id,
                    request_id,
                    candidate_id,
                    bgv_id,
                    provider,
                    transaction_id,
                    provider_request_id,
                    provider_status_code,
                    provider_json_url,
                    provider_excel_url,
                    json_file_path,
                    excel_file_path,
                    report_generated_at,
                    created_at,
                    updated_at
                FROM bank_statement_results
                WHERE candidate_id=%s
                    AND bgv_id=%s
                ORDER BY id DESC
                LIMIT 1
                """,
                (candidate_id, bgv_id),
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()
