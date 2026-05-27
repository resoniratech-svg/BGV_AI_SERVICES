from db import get_connection


class ApiLogRepository:

    @staticmethod
    def save_log(

        provider_name,
        api_name,
        request_data,
        response_data,
        status_code,
        status
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO resume_api_logs (

                provider_name,
                api_name,
                request_data,
                response_data,
                status_code,
                status

            )

            VALUES (

                %s, %s, %s,
                %s, %s, %s
            )
        """

        values = (

            provider_name,

            api_name,

            str(request_data),

            str(response_data),

            status_code,

            status
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        cursor.close()

        connection.close()