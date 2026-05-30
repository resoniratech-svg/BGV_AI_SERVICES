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
    def mark_verification_completed(
        verification_id
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """

            UPDATE verification_results

            SET

                status = %s,
                completed_at = NOW()

            WHERE id = %s
        """

        values = (

            "COMPLETED",
            verification_id
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        cursor.close()

        connection.close()

    @staticmethod
    def mark_verification_failed(

        verification_id,
        remarks=None
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """

            UPDATE verification_results

            SET

                status = %s,
                remarks = %s,
                completed_at = NOW()

            WHERE id = %s
        """

        values = (

            "FAILED",
            remarks,
            verification_id
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        cursor.close()

        connection.close()

    @staticmethod
    def initiate_watchlist_verification(

        candidate_id
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO verification_results (

                bgv_id,
                verification_type_id,
                status,
                started_at

            )

            VALUES (

                %s,
                %s,
                %s,
                NOW()
            )
        """

        values = (

            candidate_id,
            1,
            "INITIATED"
        )

        cursor.execute(

            query,
            values
        )

        connection.commit()

        verification_id = cursor.lastrowid

        cursor.close()

        connection.close()

        return verification_id

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