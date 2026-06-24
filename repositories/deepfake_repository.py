from db import get_connection

class DeepfakeRepository:

    # ==========================================
    # SAVE RESULT
    # ==========================================
    @staticmethod
    def save_result(
        candidate_id,
        bgv_id,
        document_id,
        transaction_id,
        fake_probability,
        verification_status,
        provider_name,
        api_reference_id,
        raw_response
    ):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO deepfake_results (
            candidate_id,
            bgv_id,
            document_id,
            transaction_id,
            fake_probability,
            verification_status,
            provider_name,
            api_reference_id,
            raw_response
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            candidate_id,
            bgv_id,
            document_id,
            transaction_id,
            fake_probability,
            verification_status,
            provider_name,
            api_reference_id,
            raw_response
        )

        cursor.execute(query, values)
        connection.commit()
        
        deepfake_result_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return deepfake_result_id

    # ==========================================
    # GET RESULT
    # ==========================================
    @staticmethod
    def get_result(candidate_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT *
        FROM deepfake_results
        WHERE candidate_id = %s
        ORDER BY id DESC
        LIMIT 1
        """

        cursor.execute(query, (candidate_id,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result