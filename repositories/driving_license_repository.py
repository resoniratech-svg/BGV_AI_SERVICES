import json

from db import get_connection


class DrivingLicenseRepository:

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
        raw_response

    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(

            """
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
            """,

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

        )

        connection.commit()

        result_id = cursor.lastrowid

        cursor.close()

        connection.close()

        return result_id

    # =====================================================
    # GET OCR RESULT
    # =====================================================

    @staticmethod
    def get_driving_license_ocr_result(

        ocr_result_id

    ):

        connection = get_connection()

        cursor = connection.cursor(

            dictionary=True

        )

        cursor.execute(

            """
            SELECT *
            FROM driving_license_ocr_results
            WHERE id=%s
            """,

            (

                ocr_result_id,

            )

        )

        result = cursor.fetchone()

        cursor.close()

        connection.close()

        return result

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
        raw_response

    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(

            """
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
            """,

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

        )

        connection.commit()

        result_id = cursor.lastrowid

        cursor.close()

        connection.close()

        return result_id

    # =====================================================
    # GET VERIFICATION RESULT
    # =====================================================

    @staticmethod
    def get_driving_license_result(

        candidate_id

    ):

        connection = get_connection()

        cursor = connection.cursor(

            dictionary=True

        )

        cursor.execute(

            """
            SELECT *
            FROM driving_license_results
            WHERE candidate_id=%s
            ORDER BY id DESC
            LIMIT 1
            """,

            (

                candidate_id,

            )

        )

        result = cursor.fetchone()

        cursor.close()

        connection.close()

        return result
    
    @staticmethod
    def get_driving_license_ocr_by_candidate(candidate_id):

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM driving_license_ocr_results
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