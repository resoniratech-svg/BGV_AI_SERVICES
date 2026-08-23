# import json

# from db import get_connection


# class DrivingLicenseRepository:
#     # =====================================================
#     # SAVE OCR RESULT
#     # =====================================================

#     @staticmethod
#     def save_driving_license_ocr_result(
#         candidate_id,
#         bgv_id,
#         document_id,
#         license_number,
#         full_name,
#         dependent_name,
#         date_of_birth,
#         issue_date,
#         expiry_date,
#         place_of_issue,
#         address,
#         provider_name,
#         api_reference_id,
#         raw_response,
#     ):

#         connection = get_connection()

#         cursor = connection.cursor()

#         cursor.execute(
#             """
#             INSERT INTO driving_license_ocr_results
#             (

#                 candidate_id,
#                 bgv_id,
#                 document_id,
#                 license_number,
#                 full_name,
#                 dependent_name,
#                 date_of_birth,
#                 issue_date,
#                 expiry_date,
#                 place_of_issue,
#                 address,
#                 provider_name,
#                 api_reference_id,
#                 raw_response

#             )

#             VALUES
#             (

#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s

#             )
#             """,
#             (
#                 candidate_id,
#                 bgv_id,
#                 document_id,
#                 license_number,
#                 full_name,
#                 dependent_name,
#                 date_of_birth,
#                 issue_date,
#                 expiry_date,
#                 place_of_issue,
#                 address,
#                 provider_name,
#                 api_reference_id,
#                 raw_response,
#             ),
#         )

#         connection.commit()

#         result_id = cursor.lastrowid

#         cursor.close()

#         connection.close()

#         return result_id

#     # =====================================================
#     # GET OCR RESULT
#     # =====================================================

#     @staticmethod
#     def get_driving_license_ocr_result(ocr_result_id):

#         connection = get_connection()

#         cursor = connection.cursor(dictionary=True)

#         cursor.execute(
#             """
#             SELECT *
#             FROM driving_license_ocr_results
#             WHERE id=%s
#             """,
#             (ocr_result_id,),
#         )

#         result = cursor.fetchone()

#         cursor.close()

#         connection.close()

#         return result

#     # =====================================================
#     # SAVE VERIFICATION RESULT
#     # =====================================================

#     @staticmethod
#     def save_driving_license_verification_result(
#         candidate_id,
#         bgv_id,
#         driving_license_ocr_result_id,
#         verification_status,
#         license_number,
#         full_name,
#         dependent_name,
#         date_of_birth,
#         issue_date,
#         expiry_date,
#         place_of_issue,
#         address,
#         dl_number_match_status,
#         name_match_status,
#         dob_match_status,
#         address_match_status,
#         provider_name,
#         api_reference_id,
#         raw_response,
#     ):

#         connection = get_connection()

#         cursor = connection.cursor()

#         cursor.execute(
#             """
#             INSERT INTO driving_license_results
#             (

#                 candidate_id,
#                 bgv_id,
#                 driving_license_ocr_result_id,
#                 verification_status,
#                 license_number,
#                 full_name,
#                 dependent_name,
#                 date_of_birth,
#                 issue_date,
#                 expiry_date,
#                 place_of_issue,
#                 address,
#                 dl_number_match_status,
#                 name_match_status,
#                 dob_match_status,
#                 address_match_status,
#                 provider_name,
#                 api_reference_id,
#                 raw_response

#             )

#             VALUES
#             (

#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s

#             )
#             """,
#             (
#                 candidate_id,
#                 bgv_id,
#                 driving_license_ocr_result_id,
#                 verification_status,
#                 license_number,
#                 full_name,
#                 dependent_name,
#                 date_of_birth,
#                 issue_date,
#                 expiry_date,
#                 place_of_issue,
#                 address,
#                 dl_number_match_status,
#                 name_match_status,
#                 dob_match_status,
#                 address_match_status,
#                 provider_name,
#                 api_reference_id,
#                 raw_response,
#             ),
#         )

#         connection.commit()

#         result_id = cursor.lastrowid

#         cursor.close()

#         connection.close()

#         return result_id

#     # =====================================================
#     # GET VERIFICATION RESULT
#     # =====================================================

#     @staticmethod
#     def get_driving_license_result(candidate_id):

#         connection = get_connection()

#         cursor = connection.cursor(dictionary=True)

#         cursor.execute(
#             """
#             SELECT *
#             FROM driving_license_results
#             WHERE candidate_id=%s
#             ORDER BY id DESC
#             LIMIT 1
#             """,
#             (candidate_id,),
#         )

#         result = cursor.fetchone()

#         cursor.close()

#         connection.close()

#         return result

#     @staticmethod
#     def get_driving_license_ocr_by_candidate(candidate_id):

#         connection = get_connection()
#         cursor = connection.cursor(dictionary=True)

#         cursor.execute(
#             """
#             SELECT *
#             FROM driving_license_ocr_results
#             WHERE candidate_id=%s
#             ORDER BY id DESC
#             LIMIT 1
#             """,
#             (candidate_id,),
#         )

#         result = cursor.fetchone()

#         cursor.close()
#         connection.close()

#         return result


import json
from datetime import datetime

from db import get_connection


class DrivingLicenseRepository:
    # =====================================================
    # CLEAN DATE
    # =====================================================

    @staticmethod
    def clean_date(value):
        """
        Convert Driving License date values into
        MySQL-compatible YYYY-MM-DD format.

        Invalid / empty dates become None.
        """

        if value is None:
            return None

        value = str(value).strip()

        if not value:
            return None

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

        for date_format in formats:
            try:
                parsed_date = datetime.strptime(
                    value,
                    date_format,
                )

                return parsed_date.strftime("%Y-%m-%d")

            except ValueError:
                continue

        print("=" * 80)
        print("DRIVING LICENSE REPOSITORY DATE WARNING")
        print("ORIGINAL VALUE:", repr(value))
        print("INVALID DATE - SAVING NULL")
        print("=" * 80)

        return None

    # =====================================================
    # SAVE OCR RESULT
    # =====================================================

    @staticmethod
    def save_driving_license_ocr_result(
        candidate_id,
        bgv_id,
        document_id,
        license_number,
        full_name,
        dependent_name,
        date_of_birth,
        issue_date,
        expiry_date,
        place_of_issue,
        address,
        provider_name,
        api_reference_id,
        raw_response,
    ):

        # -------------------------------------------------
        # CLEAN DATES
        # -------------------------------------------------

        date_of_birth = DrivingLicenseRepository.clean_date(date_of_birth)

        issue_date = DrivingLicenseRepository.clean_date(issue_date)

        expiry_date = DrivingLicenseRepository.clean_date(expiry_date)

        # -------------------------------------------------
        # DATABASE
        # -------------------------------------------------

        connection = get_connection()
        cursor = connection.cursor()

        try:
            query = """
                INSERT INTO driving_license_ocr_results
                (
                    candidate_id,
                    bgv_id,
                    document_id,
                    license_number,
                    full_name,
                    dependent_name,
                    date_of_birth,
                    issue_date,
                    expiry_date,
                    place_of_issue,
                    address,
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
                    %s
                )
            """

            cursor.execute(
                query,
                (
                    candidate_id,
                    bgv_id,
                    document_id,
                    license_number,
                    full_name,
                    dependent_name,
                    date_of_birth,
                    issue_date,
                    expiry_date,
                    place_of_issue,
                    address,
                    provider_name,
                    api_reference_id,
                    raw_response,
                ),
            )

            connection.commit()

            result_id = cursor.lastrowid

            print("=" * 80)
            print("DRIVING LICENSE OCR RESULT SAVED")
            print("OCR RESULT ID:", result_id)
            print("=" * 80)

            return result_id

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
    def get_driving_license_ocr_result(ocr_result_id):

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT *
                FROM driving_license_ocr_results
                WHERE id = %s
                LIMIT 1
                """,
                (ocr_result_id,),
            )

            return cursor.fetchone()

        finally:
            cursor.close()
            connection.close()

    # =====================================================
    # GET OCR RESULT BY CANDIDATE
    # =====================================================

    @staticmethod
    def get_driving_license_ocr_by_candidate(candidate_id):

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT *
                FROM driving_license_ocr_results
                WHERE candidate_id = %s
                ORDER BY id DESC
                LIMIT 1
                """,
                (candidate_id,),
            )

            return cursor.fetchone()

        finally:
            cursor.close()
            connection.close()

    # =====================================================
    # SAVE VERIFICATION RESULT
    # =====================================================

    @staticmethod
    def save_driving_license_verification_result(
        candidate_id,
        bgv_id,
        driving_license_ocr_result_id,
        verification_status,
        license_number,
        full_name,
        dependent_name,
        date_of_birth,
        issue_date,
        expiry_date,
        place_of_issue,
        address,
        dl_number_match_status,
        name_match_status,
        dob_match_status,
        address_match_status,
        provider_name,
        api_reference_id,
        raw_response,
    ):

        # -------------------------------------------------
        # CONVERT RAW RESPONSE TO JSON STRING
        # -------------------------------------------------

        if isinstance(raw_response, (dict, list)):
            raw_response = json.dumps(raw_response)

        # -------------------------------------------------
        # CLEAN DATES
        # -------------------------------------------------

        date_of_birth = DrivingLicenseRepository.clean_date(date_of_birth)

        issue_date = DrivingLicenseRepository.clean_date(issue_date)

        expiry_date = DrivingLicenseRepository.clean_date(expiry_date)

        # -------------------------------------------------
        # DATABASE
        # -------------------------------------------------

        connection = get_connection()
        cursor = connection.cursor()

        try:
            query = """
                INSERT INTO driving_license_results
                (
                    candidate_id,
                    bgv_id,
                    driving_license_ocr_result_id,
                    verification_status,
                    license_number,
                    full_name,
                    dependent_name,
                    date_of_birth,
                    issue_date,
                    expiry_date,
                    place_of_issue,
                    address,
                    dl_number_match_status,
                    name_match_status,
                    dob_match_status,
                    address_match_status,
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
                    %s
                )
            """

            cursor.execute(
                query,
                (
                    candidate_id,
                    bgv_id,
                    driving_license_ocr_result_id,
                    verification_status,
                    license_number,
                    full_name,
                    dependent_name,
                    date_of_birth,
                    issue_date,
                    expiry_date,
                    place_of_issue,
                    address,
                    dl_number_match_status,
                    name_match_status,
                    dob_match_status,
                    address_match_status,
                    provider_name,
                    api_reference_id,
                    raw_response,
                ),
            )

            connection.commit()

            result_id = cursor.lastrowid

            print("=" * 80)
            print("DRIVING LICENSE VERIFICATION RESULT SAVED")
            print("RESULT ID:", result_id)
            print("STATUS:", verification_status)
            print("=" * 80)

            return result_id

        except Exception:
            connection.rollback()

            raise

        finally:
            cursor.close()
            connection.close()

    # =====================================================
    # GET VERIFICATION RESULT
    # =====================================================

    @staticmethod
    def get_driving_license_result(candidate_id):

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT *
                FROM driving_license_results
                WHERE candidate_id = %s
                ORDER BY id DESC
                LIMIT 1
                """,
                (candidate_id,),
            )

            return cursor.fetchone()

        finally:
            cursor.close()
            connection.close()
