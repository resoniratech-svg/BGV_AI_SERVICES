from db import get_connection


class DocumentRepository:

    @staticmethod
    def get_uploaded_document(

        document_id
    ):

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
            SELECT *

            FROM candidate_uploaded_documents

            WHERE id = %s

            LIMIT 1
        """

        cursor.execute(

            query,

            (
                document_id,
            )
        )

        result = cursor.fetchone()

        cursor.close()

        connection.close()

        return result 