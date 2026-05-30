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
            verification_status,
            passport_number,
            full_name,
            nationality,
            country,
            date_of_birth,
            issue_date,
            expiry_date,
            provider_name,
            raw_response
        )

        cursor.execute(

            query,
            values
        )

        connection.commit()

        cursor.close()

        connection.close()