from db import get_connection


class PassportRepository:

    @staticmethod
    def save_passport_result(
        candidate_id,
        bgv_id,
        verification_status,
        passport_number,
        full_name,
        nationality,
        country,
        date_of_birth,
        issue_date,
        expiry_date,
        provider_name,
        api_reference_id,
        raw_response
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO passport_results (

                candidate_id,
                bgv_id,
                verification_status,
                passport_number,
                full_name,
                nationality,
                country,
                date_of_birth,
                issue_date,
                expiry_date,
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
            verification_status,
            passport_number,
            full_name,
            nationality,
            country,
            date_of_birth,
            issue_date,
            expiry_date,
            provider_name,
            api_reference_id,
            raw_response
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        passport_result_id = (
            cursor.lastrowid
        )

        cursor.close()
        connection.close()

        return passport_result_id

    @staticmethod
    def get_passport_result(
        candidate_id
    ):

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM passport_results
            WHERE candidate_id = %s
            ORDER BY id DESC
            LIMIT 1
            """,
            (candidate_id,)
        )

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result