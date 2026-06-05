from db import get_connection


class DiditRepository:

    @staticmethod
    def get_session_by_provider_session_id(

        provider_session_id
    ):

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
            SELECT *

            FROM verification_sessions

            WHERE provider_session_id = %s

            LIMIT 1
        """

        cursor.execute(

            query,

            (
                provider_session_id,
            )
        )

        result = cursor.fetchone()

        cursor.close()

        connection.close()

        return result
    
    @staticmethod
    def save_verification_session(

        data
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO verification_sessions (

                candidate_id,
                bgv_request_id,
                provider_name,
                verification_type,
                workflow_id,
                provider_session_id,
                verification_url,
                status

            )

            VALUES (

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

            data.get(
                "candidate_id"
            ),

            data.get(
                "bgv_request_id"
            ),

            data.get(
                "provider_name"
            ),

            data.get(
                "verification_type"
            ),

            data.get(
                "workflow_id"
            ),

            data.get(
                "provider_session_id"
            ),

            data.get(
                "verification_url"
            ),

            data.get(
                "status"
            )
        )

        cursor.execute(

            query,
            values
        )

        connection.commit()

        cursor.close()

        connection.close()