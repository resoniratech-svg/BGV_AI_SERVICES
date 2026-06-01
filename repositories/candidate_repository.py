from db import get_connection

import json


class CandidateRepository:

    @staticmethod
    def save_candidate(candidate):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO parsed_candidates (

                candidate_id,
                full_name,
                email,
                phone,
                linkedin,
                city,
                state,
                country,
                skills,
                experience_years,
                total_experience_months,
                highest_qualification,
                current_location,
                preferred_location,
                github_url,
                portfolio_url,
                resume_file_name,
                resume_score,
                current_company,
                designation,
                parser_provider,
                parsing_status

            )

            VALUES (

                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s
            )
        """

        skills = candidate.get(
            "skills",
            []
        )

        if isinstance(skills, list):

            skills = ",".join(skills)

        values = (

            candidate.get("candidate_id"),

            candidate.get("full_name"),

            candidate.get("email"),

            candidate.get("phone"),

            candidate.get("linkedin"),

            candidate.get("city"),

            candidate.get("state"),

            candidate.get("country"),

            skills,

            candidate.get("experience_years"),

            candidate.get(
                "total_experience_months"
            ),

            candidate.get(
                "highest_qualification"
            ),

            candidate.get(
                "current_location"
            ),

            candidate.get(
                "preferred_location"
            ),

            candidate.get(
                "github_url"
            ),

            candidate.get(
                "portfolio_url"
            ),

            candidate.get(
                "resume_file_name"
            ),

            candidate.get(
                "resume_score"
            ),

            candidate.get(
                "current_company"
            ),

            candidate.get(
                "designation"
            ),

            "RCHILLI",

            "PARSED"
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        parsed_candidate_id = (
            cursor.lastrowid
        )

        cursor.close()

        connection.close()

        return parsed_candidate_id

    @staticmethod
    def save_raw_resume_data(

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

            json.dumps(raw_data)
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        cursor.close()

        connection.close()

    @staticmethod
    def save_resume_api_log(

        candidate_id,
        api_provider,
        request_payload,
        response_payload,
        status
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO resume_api_logs (

                candidate_id,
                api_provider,
                request_payload,
                response_payload,
                status

            )

            VALUES (

                %s,
                %s,
                %s,
                %s,
                %s
            )
        """

        values = (

            candidate_id,

            api_provider,

            json.dumps(request_payload),

            json.dumps(response_payload),

            status
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        cursor.close()

        connection.close()