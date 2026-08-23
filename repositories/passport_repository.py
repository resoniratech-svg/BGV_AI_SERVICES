from datetime import datetime

from db import get_connection


class PassportRepository:
    # =====================================================
    # CLEAN DATE
    # =====================================================

    @staticmethod
    def clean_date(value):
        """
        Convert passport date values into MySQL-compatible
        YYYY-MM-DD format.

        Empty strings become None so MySQL stores NULL
        instead of an invalid empty DATE value.
        """

        # -------------------------------------------------
        # NONE
        # -------------------------------------------------

        if value is None:
            return None

        # -------------------------------------------------
        # CONVERT TO STRING
        # -------------------------------------------------

        value = str(value).strip()

        # -------------------------------------------------
        # EMPTY STRING
        # -------------------------------------------------

        if not value:
            return None

        # -------------------------------------------------
        # SUPPORTED DATE FORMATS
        # -------------------------------------------------

        formats = [
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%Y/%m/%d",
            "%d.%m.%Y",
            "%d %m %Y",
            "%d %b %Y",
            "%d %B %Y",
            "%b %d %Y",
            "%B %d %Y",
        ]

        # -------------------------------------------------
        # TRY TO PARSE DATE
        # -------------------------------------------------

        for date_format in formats:
            try:
                parsed_date = datetime.strptime(
                    value,
                    date_format,
                )

                return parsed_date.strftime("%Y-%m-%d")

            except ValueError:
                continue

        # -------------------------------------------------
        # INVALID DATE
        # -------------------------------------------------

        print("=" * 80)
        print("PASSPORT REPOSITORY DATE WARNING")
        print("ORIGINAL VALUE:", repr(value))
        print("INVALID DATE - SAVING NULL")
        print("=" * 80)

        return None

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
        raw_response,
    ):

        # -------------------------------------------------
        # CLEAN DATE VALUES
        # -------------------------------------------------

        date_of_birth = PassportRepository.clean_date(date_of_birth)

        issue_date = PassportRepository.clean_date(issue_date)

        expiry_date = PassportRepository.clean_date(expiry_date)

        # -------------------------------------------------
        # DEBUG
        # -------------------------------------------------

        print("=" * 80)
        print("SAVING PASSPORT OCR RESULT")
        print("=" * 80)

        print(
            "DATE OF BIRTH:",
            repr(date_of_birth),
        )

        print(
            "ISSUE DATE:",
            repr(issue_date),
        )

        print(
            "EXPIRY DATE:",
            repr(expiry_date),
        )

        print("=" * 80)

        # -------------------------------------------------
        # DATABASE CONNECTION
        # -------------------------------------------------

        connection = get_connection()
        cursor = connection.cursor()

        try:
            query = """
            INSERT INTO passport_ocr_results
            (
                candidate_id,
                bgv_id,
                document_id,
                passport_number,
                file_number,
                first_name,
                last_name,
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
                    # DATE
                    date_of_birth,
                    # DATE
                    issue_date,
                    # DATE
                    expiry_date,
                    nationality,
                    country,
                    guardian_name,
                    mother_name,
                    place_of_birth,
                    place_of_issue,
                    provider_name,
                    api_reference_id,
                    raw_response,
                ),
            )

            connection.commit()

            passport_ocr_result_id = cursor.lastrowid

            print("=" * 80)
            print(
                "PASSPORT OCR RESULT SAVED:",
                passport_ocr_result_id,
            )
            print("=" * 80)

            return passport_ocr_result_id

        except Exception:
            connection.rollback()

            raise

        finally:
            cursor.close()
            connection.close()

    # =====================================================
    # GET OCR RESULT
    # =====================================================

    @staticmethod
    def get_passport_ocr_result(candidate_id):

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT *
                FROM passport_ocr_results
                WHERE candidate_id = %s
                ORDER BY id DESC
                LIMIT 1
                """,
                (candidate_id,),
            )

            result = cursor.fetchone()

            return result

        finally:
            cursor.close()
            connection.close()

    # =====================================================
    # GET OCR RESULT BY ID
    # =====================================================

    @staticmethod
    def get_passport_ocr_result_by_id(passport_ocr_result_id):

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT *
                FROM passport_ocr_results
                WHERE id = %s
                LIMIT 1
                """,
                (passport_ocr_result_id,),
            )

            result = cursor.fetchone()

            return result

        finally:
            cursor.close()
            connection.close()

    # =====================================================
    # SAVE PASSPORT VERIFICATION RESULT
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
        raw_response,
    ):

        # -------------------------------------------------
        # IMPORTANT:
        # CLEAN DATES AGAIN BEFORE SECOND DB INSERT
        # -------------------------------------------------

        date_of_birth = PassportRepository.clean_date(date_of_birth)

        issue_date = PassportRepository.clean_date(issue_date)

        expiry_date = PassportRepository.clean_date(expiry_date)

        # -------------------------------------------------
        # DEBUG
        # -------------------------------------------------

        print("=" * 80)
        print("SAVING PASSPORT VERIFICATION RESULT")
        print("=" * 80)

        print(
            "DATE OF BIRTH:",
            repr(date_of_birth),
        )

        print(
            "ISSUE DATE:",
            repr(issue_date),
        )

        print(
            "EXPIRY DATE:",
            repr(expiry_date),
        )

        print(
            "VERIFICATION STATUS:",
            verification_status,
        )

        print("=" * 80)

        # -------------------------------------------------
        # DATABASE CONNECTION
        # -------------------------------------------------

        connection = get_connection()
        cursor = connection.cursor()

        try:
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
                    # DATE
                    date_of_birth,
                    # DATE
                    issue_date,
                    # DATE
                    expiry_date,
                    passport_match_status,
                    name_match_status,
                    dob_match_status,
                    provider_name,
                    api_reference_id,
                    raw_response,
                ),
            )

            connection.commit()

            passport_result_id = cursor.lastrowid

            print("=" * 80)
            print(
                "PASSPORT VERIFICATION RESULT SAVED:",
                passport_result_id,
            )
            print("=" * 80)

            return passport_result_id

        except Exception:
            connection.rollback()

            raise

        finally:
            cursor.close()
            connection.close()

    # =====================================================
    # GET PASSPORT VERIFICATION RESULT
    # =====================================================

    @staticmethod
    def get_passport_result(candidate_id):

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT *
                FROM passport_results
                WHERE candidate_id = %s
                ORDER BY id DESC
                LIMIT 1
                """,
                (candidate_id,),
            )

            result = cursor.fetchone()

            return result

        finally:
            cursor.close()
            connection.close()
