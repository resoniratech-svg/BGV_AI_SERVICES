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
    # SAVE OCR RESULT
    # ==========================================

    @staticmethod
    def save_aadhaar_ocr_result(
        candidate_id,
        bgv_id,
        document_id,
        full_name,
        date_of_birth,
        gender,
        provider_name,
        api_reference_id,
        raw_response,
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """

            INSERT INTO aadhaar_ocr_results (

                candidate_id,
                bgv_id,
                document_id,
                full_name,
                date_of_birth,
                gender,
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
            document_id,
            full_name,
            date_of_birth,
            gender,
            provider_name,
            api_reference_id,
            raw_response,
        )

        cursor.execute(query, values)

        connection.commit()

        aadhaar_ocr_result_id = cursor.lastrowid

        cursor.close()

        connection.close()

        return aadhaar_ocr_result_id

    # ==========================================
    # SAVE FINAL VERIFICATION RESULT
    # ==========================================

    @staticmethod
    def save_aadhaar_verification_result(
        candidate_id,
        bgv_id,
        aadhaar_ocr_result_id,
        verification_status,
        resident_name,
        date_of_birth,
        name_match_status,
        dob_match_status,
        resident_image,
        provider_name,
        api_reference_id,
        raw_response,
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """

            INSERT INTO aadhaar_verification_results (

                candidate_id,
                bgv_id,
                aadhaar_ocr_result_id,
                verification_status,
                resident_name,
                date_of_birth,
                name_match_status,
                dob_match_status,
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
                %s,
                %s

            )

        """

        values = (
            candidate_id,
            bgv_id,
            aadhaar_ocr_result_id,
            verification_status,
            resident_name,
            date_of_birth,
            name_match_status,
            dob_match_status,
            resident_image,
            provider_name,
            api_reference_id,
            raw_response,
        )

        cursor.execute(query, values)

        connection.commit()

        verification_result_id = cursor.lastrowid

        cursor.close()

        connection.close()

        return verification_result_id

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

            ORDER BY id DESC

            LIMIT 1

        """

        cursor.execute(query, (candidate_id,))

        result = cursor.fetchone()

        cursor.close()

        connection.close()

        return result
