import json

from db import get_connection


class VerificationRepository:

    @staticmethod
    def create_verification_request(

        candidate_id,
        verification_type,
        provider_name,
        status="INITIATED"
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO verification_sessions (

                candidate_id,
                verification_type,
                provider_name,
                status

            )

            VALUES (

                %s, %s, %s, %s
            )
        """

        values = (

            candidate_id,

            verification_type,

            provider_name,

            status
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        verification_id = (
            cursor.lastrowid
        )

        cursor.close()

        connection.close()

        return verification_id

    @staticmethod
    def update_verification_status(

        verification_id,
        status
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """

            UPDATE verification_sessions

            SET status = %s

            WHERE id = %s
        """

        values = (

            status,
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
    def mark_verification_completed(

        verification_id
    ):

        VerificationRepository.update_verification_status(

            verification_id,
            "COMPLETED"
        )

    @staticmethod
    def save_resume_raw_data(

        candidate_id,
        raw_data
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO resume_raw_data (

                candidate_id,
                raw_data

            )

            VALUES (

                %s,
                %s
            )
        """

        values = (

            candidate_id,
            raw_data
        )
        print("SAVE METHOD CALLED")
        print(values)
        cursor.execute(

            query,
            values
        )

        connection.commit()

        cursor.close()

        connection.close()

    @staticmethod
    def save_resume_parsing_result(

        candidate_id,
        parsed_data,
        skills,
        experience_years,
        education_summary,
        parsing_status,
        parser_provider,
        raw_response
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO resume_parsing_results (

                candidate_id,
                parsed_data,
                skills,
                experience_years,
                education_summary,
                parsing_status,
                parser_provider,
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
                %s
            )
        """

        values = (

            candidate_id,
            parsed_data,
            skills,
            experience_years,
            education_summary,
            parsing_status,
            parser_provider,
            raw_response
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        cursor.close()

        connection.close()