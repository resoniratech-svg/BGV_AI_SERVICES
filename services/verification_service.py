from db import get_connection

from repositories.verification_repository import (
    VerificationRepository
)


class VerificationService:

    @staticmethod
    def initiate_resume_verification(
        candidate_id
    ):

        verification_id = (
            VerificationRepository
            .create_verification_request(

                candidate_id=candidate_id,

                verification_type="RESUME_PARSING",

                provider_name="RChilli",

                status="INITIATED"
            )
        )

        return verification_id

    
    @staticmethod
    def get_bgv_request_id(candidate_id):

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT id
            FROM bgv_requests
            WHERE candidate_id = %s
            ORDER BY id DESC
            LIMIT 1
        """

        cursor.execute(query, (candidate_id,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if not result:
            raise Exception(
                f"No BGV request found for candidate {candidate_id}"
            )

        return result["id"]
    
    @staticmethod
    def update_verification_result(

        verification_id,
        status,
        module_score,
        remarks,
        document_path
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """

            UPDATE verification_results

            SET

                status = %s,
                module_score = %s,
                remarks = %s,
                document_path = %s,
                completed_at = NOW()

            WHERE id = %s
        """

        values = (

            status,
            module_score,
            remarks,
            document_path,
            verification_id
        )

        cursor.execute(

            query,
            values
        )

        connection.commit()

        cursor.close()

        connection.close()