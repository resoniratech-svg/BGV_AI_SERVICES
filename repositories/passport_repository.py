from db import get_connection


class PassportRepository:

    # =====================================================
    # SAVE PASSPORT OCR RESULT
    # =====================================================

    @staticmethod
    def save_passport_ocr_result(
        candidate_id,
        bgv_id,
        document_id,
        passport_number,
        file_number,
        given_name,
        surname,
        full_name,
        gender,
        date_of_birth,
        issue_date,
        expiry_date,
        nationality,
        country,
        guardian_name,
        mother_name,
        place_of_birth,
        place_of_issue,
        provider_name,
        api_reference_id,
        raw_response
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        INSERT INTO passport_ocr_results
        (
            candidate_id,
            bgv_id,
            document_id,
            passport_number,
            file_number,
            given_name,
            surname,
            full_name,
            gender,
            date_of_birth,
            issue_date,
            expiry_date,
            nationality,
            country,
            guardian_name,
            mother_name,
            place_of_birth,
            place_of_issue,
            provider_name,
            api_reference_id,
            raw_response
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
            %s
        )
        """

        cursor.execute(
            query,
            (
                candidate_id,
                bgv_id,
                document_id,
                passport_number,
                file_number,
                given_name,
                surname,
                full_name,
                gender,
                date_of_birth,
                issue_date,
                expiry_date,
                nationality,
                country,
                guardian_name,
                mother_name,
                place_of_birth,
                place_of_issue,
                provider_name,
                api_reference_id,
                raw_response
            )
        )

        connection.commit()

        passport_ocr_result_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return passport_ocr_result_id

    # =====================================================
    # GET OCR RESULT
    # =====================================================

    @staticmethod
    def get_passport_ocr_result(candidate_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM passport_ocr_results
            WHERE candidate_id=%s
            ORDER BY id DESC
            LIMIT 1
            """,
            (candidate_id,)
        )

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result

    # =====================================================
    # SAVE VERIFICATION RESULT
    # =====================================================

    @staticmethod
    def save_passport_result(
        candidate_id,
        bgv_id,
        passport_ocr_result_id,
        verification_status,
        passport_number,
        full_name,
        nationality,
        country,
        date_of_birth,
        issue_date,
        expiry_date,
        passport_match_status,
        name_match_status,
        dob_match_status,
        provider_name,
        api_reference_id,
        raw_response
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        INSERT INTO passport_results
        (
            candidate_id,
            bgv_id,
            passport_ocr_result_id,
            verification_status,
            passport_number,
            full_name,
            nationality,
            country,
            date_of_birth,
            issue_date,
            expiry_date,
            passport_match_status,
            name_match_status,
            dob_match_status,
            provider_name,
            api_reference_id,
            raw_response
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
            %s
        )
        """

        cursor.execute(
            query,
            (
                candidate_id,
                bgv_id,
                passport_ocr_result_id,
                verification_status,
                passport_number,
                full_name,
                nationality,
                country,
                date_of_birth,
                issue_date,
                expiry_date,
                passport_match_status,
                name_match_status,
                dob_match_status,
                provider_name,
                api_reference_id,
                raw_response
            )
        )

        connection.commit()

        passport_result_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return passport_result_id

    # =====================================================
    # GET PASSPORT RESULT
    # =====================================================

    @staticmethod
    def get_passport_result(candidate_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM passport_results
            WHERE candidate_id=%s
            ORDER BY id DESC
            LIMIT 1
            """,
            (candidate_id,)
        )

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result