from db import get_connection


class PanRepository:
    @staticmethod
    def save_pan_ocr_result(
        candidate_id,
        bgv_id,
        document_id,
        pan_number,
        full_name,
        father_name,
        date_of_birth,
        provider_name,
        api_reference_id,
        raw_response,
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """

            INSERT INTO pan_ocr_results (

                candidate_id,
                bgv_id,
                document_id,
                pan_number,
                full_name,
                father_name,
                date_of_birth,
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
                %s

            )

        """

        values = (
            candidate_id,
            bgv_id,
            document_id,
            pan_number,
            full_name,
            father_name,
            date_of_birth,
            provider_name,
            api_reference_id,
            raw_response,
        )

        cursor.execute(query, values)

        connection.commit()

        pan_ocr_result_id = cursor.lastrowid

        cursor.close()

        connection.close()

        return pan_ocr_result_id

    @staticmethod
    def save_pan_verification_result(
        candidate_id,
        bgv_id,
        pan_ocr_result_id,
        verification_status,
        pan_number,
        full_name,
        date_of_birth,
        pan_match_status,
        name_match_status,
        dob_match_status,
        provider_name,
        api_reference_id,
        raw_response,
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """

            INSERT INTO pan_verification_results (

                candidate_id,
                bgv_id,
                pan_ocr_result_id,
                verification_status,
                pan_number,
                full_name,
                date_of_birth,
                pan_match_status,
                name_match_status,
                dob_match_status,
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
                %s,
                %s

            )

        """

        values = (
            candidate_id,
            bgv_id,
            pan_ocr_result_id,
            verification_status,
            pan_number,
            full_name,
            date_of_birth,
            pan_match_status,
            name_match_status,
            dob_match_status,
            provider_name,
            api_reference_id,
            raw_response,
        )

        cursor.execute(query, values)

        connection.commit()

        pan_verification_result_id = cursor.lastrowid

        cursor.close()

        connection.close()

        return pan_verification_result_id

    @staticmethod
    def get_pan_verification_result(candidate_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """

            SELECT *

            FROM pan_verification_results

            WHERE candidate_id = %s

            ORDER BY id DESC

            LIMIT 1

            """,
            (candidate_id,),
        )

        result = cursor.fetchone()

        cursor.close()

        connection.close()

        return result

    @staticmethod
    def get_pan_ocr_result(candidate_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """

            SELECT *

            FROM pan_ocr_results

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

    ###PATH:BGV_AI_SERVICES/repositories/__init__.py
