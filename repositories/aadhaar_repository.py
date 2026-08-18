from db import get_connection


class AadhaarRepository:
    # ==========================================
    # SAVE AADHAAR SESSION
    # ==========================================

    @staticmethod
    def save_aadhaar_session(
        candidate_id,
        bgv_id,
        transaction_id,
        scan_uri,
        expires_at,
        session_status,
        provider_name,
        api_reference_id,
        raw_response,
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """

            INSERT INTO aadhaar_verification_sessions (

                candidate_id,
                bgv_id,
                transaction_id,
                scan_uri,
                expires_at,
                session_status,
                provider_name,
                api_reference_id,
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
                %s

            )

        """

        values = (
            candidate_id,
            bgv_id,
            transaction_id,
            scan_uri,
            expires_at,
            session_status,
            provider_name,
            api_reference_id,
            raw_response,
        )

        cursor.execute(query, values)

        connection.commit()

        aadhaar_session_id = cursor.lastrowid

        cursor.close()

        connection.close()

        return aadhaar_session_id

    # ==========================================
    # GET SESSION
    # ==========================================

    @staticmethod
    def get_aadhaar_session(candidate_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        query = """

            SELECT *

            FROM aadhaar_verification_sessions

            WHERE candidate_id = %s

            ORDER BY id DESC

            LIMIT 1

        """

        cursor.execute(query, (candidate_id,))

        result = cursor.fetchone()

        cursor.close()

        connection.close()

        return result

    # ==========================================
    # GET SESSION BY TRANSACTION ID
    # ==========================================

    @staticmethod
    def get_aadhaar_session_by_transaction_id(transaction_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        query = """

            SELECT *

            FROM aadhaar_verification_sessions

            WHERE transaction_id = %s

            LIMIT 1

        """

        cursor.execute(query, (transaction_id,))

        result = cursor.fetchone()

        cursor.close()

        connection.close()

        return result

    # ==========================================
    # UPDATE SESSION STATUS
    # ==========================================

    @staticmethod
    def update_session_status(transaction_id, session_status, raw_response=None):

        connection = get_connection()

        cursor = connection.cursor()

        query = """

            UPDATE
            aadhaar_verification_sessions

            SET
            session_status = %s,
            raw_response = %s

            WHERE
            transaction_id = %s

        """

        cursor.execute(query, (session_status, raw_response, transaction_id))

        connection.commit()

        cursor.close()

        connection.close()

    # ==========================================
    # SAVE FINAL VERIFICATION RESULT
    # ==========================================

    @staticmethod
    def save_aadhaar_verification_result(
        candidate_id,
        bgv_id,
        verification_status,
        resident_name,
        date_of_birth,
        gender,
        address,
        resident_image,
        provider_name,
        api_reference_id,
        raw_response,
    ):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            # ==================================================
            # CHECK EXISTING RESULT
            # ==================================================

            check_query = """
                SELECT id
                FROM aadhaar_verification_results
                WHERE candidate_id = %s
                AND bgv_id = %s
                ORDER BY id DESC
                LIMIT 1
            """

            cursor.execute(
                check_query,
                (
                    candidate_id,
                    bgv_id,
                ),
            )

            existing_result = cursor.fetchone()

            # ==================================================
            # UPDATE EXISTING RESULT
            # ==================================================

            if existing_result:
                verification_result_id = existing_result[0]

                update_query = """
                    UPDATE aadhaar_verification_results
                    SET
                        verification_status = %s,
                        resident_name = %s,
                        date_of_birth = %s,
                        gender = %s,
                        address = %s,
                        resident_image = %s,
                        provider_name = %s,
                        api_reference_id = %s,
                        raw_response = %s,
                        verified_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """

                values = (
                    verification_status,
                    resident_name,
                    date_of_birth,
                    gender,
                    address,
                    resident_image,
                    provider_name,
                    api_reference_id,
                    raw_response,
                    verification_result_id,
                )

                cursor.execute(update_query, values)

                connection.commit()

                print("=" * 80)
                print("AADHAAR RESULT UPDATED")
                print("RESULT ID:", verification_result_id)
                print("=" * 80)

                return verification_result_id

            # ==================================================
            # INSERT NEW RESULT
            # ==================================================

            insert_query = """
                INSERT INTO aadhaar_verification_results (
                    candidate_id,
                    bgv_id,
                    verification_status,
                    resident_name,
                    date_of_birth,
                    gender,
                    address,
                    resident_image,
                    provider_name,
                    api_reference_id,
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
                    %s
                )
            """

            values = (
                candidate_id,
                bgv_id,
                verification_status,
                resident_name,
                date_of_birth,
                gender,
                address,
                resident_image,
                provider_name,
                api_reference_id,
                raw_response,
            )

            cursor.execute(insert_query, values)

            connection.commit()

            verification_result_id = cursor.lastrowid

            print("=" * 80)
            print("AADHAAR RESULT INSERTED")
            print("RESULT ID:", verification_result_id)
            print("=" * 80)

            return verification_result_id

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    # ==========================================

    # GET VERIFICATION RESULT
    # ==========================================

    @staticmethod
    def get_aadhaar_verification_result(candidate_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT *
            FROM aadhaar_verification_results
            WHERE candidate_id = %s
            AND resident_image IS NOT NULL
            ORDER BY id DESC
            LIMIT 1
        """

        cursor.execute(query, (candidate_id,))

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result
