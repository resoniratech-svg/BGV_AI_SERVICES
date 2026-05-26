from db import mysql


class DiditRepository:

    @staticmethod
    def save_verification_session(data):

        cursor = mysql.connection.cursor()

        query = """
        INSERT INTO verification_sessions (

            candidate_id,
            provider_name,
            verification_type,
            workflow_id,
            provider_session_id,
            verification_url,
            status

        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (

            data["candidate_id"],

            data["provider_name"],

            data["verification_type"],

            data["workflow_id"],

            data["provider_session_id"],

            data["verification_url"],

            data["status"]
        )

        cursor.execute(query, values)

        mysql.connection.commit()

        session_id = cursor.lastrowid

        cursor.close()

        return session_id

    @staticmethod
    def save_provider_callback(data):

        cursor = mysql.connection.cursor()

        query = """
        INSERT INTO provider_callbacks (

            provider_name,
            provider_session_id,
            callback_type,
            callback_payload,
            callback_status

        ) VALUES (%s, %s, %s, %s, %s)
        """

        values = (

            data["provider_name"],

            data["provider_session_id"],

            data["callback_type"],

            data["callback_payload"],

            data["callback_status"]
        )

        cursor.execute(query, values)

        mysql.connection.commit()

        cursor.close()

    @staticmethod
    def save_verification_document(data):

        cursor = mysql.connection.cursor()

        query = """
        INSERT INTO verification_documents (

            session_id,
            candidate_id,
            document_type,
            document_number,
            full_name,
            nationality,
            issuing_country,
            verification_status,
            raw_response

        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (

            data["session_id"],

            data["candidate_id"],

            data["document_type"],

            data["document_number"],

            data["full_name"],

            data["nationality"],

            data["issuing_country"],

            data["verification_status"],

            data["raw_response"]
        )

        cursor.execute(query, values)

        mysql.connection.commit()

        cursor.close()
@staticmethod
def update_session_status(
    provider_session_id,
    status
):

    cursor = mysql.connection.cursor()

    query = """
    UPDATE verification_sessions
    SET status = %s
    WHERE provider_session_id = %s
    """

    cursor.execute(

        query,

        (
            status,
            provider_session_id
        )
    )

    mysql.connection.commit()

    cursor.close()