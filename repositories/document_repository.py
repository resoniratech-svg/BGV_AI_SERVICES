from db import get_connection


class DocumentRepository:
    @staticmethod
    def get_uploaded_document(document_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT *
            FROM candidate_uploaded_documents
            WHERE id = %s
            LIMIT 1
        """

        cursor.execute(query, (document_id,))

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result

    @staticmethod
    def get_document_by_id(document_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            id,
            file_path,
            original_filename,
            document_type,
            mime_type
        FROM candidate_uploaded_documents
        WHERE id = %s
        LIMIT 1
        """

        cursor.execute(query, (document_id,))

        document = cursor.fetchone()

        cursor.close()
        connection.close()

        if not document:
            return None

        return {
            "id": document["id"],
            "file_path": document["file_path"],
            "original_filename": document["original_filename"],
            "document_type": document["document_type"],
            "mime_type": document["mime_type"],
        }
