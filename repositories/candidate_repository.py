from db import get_connection


class CandidateRepository:

    @staticmethod
    def save_candidate(candidate):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO parsed_candidates (

                full_name,
                email,
                phone,
                linkedin,
                city,
                state,
                country,
                skills,
                experience_years,
                current_company,
                designation

            )

            VALUES (

                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )
        """

        skills = candidate.get(
            "skills",
            []
        )

        if isinstance(skills, list):

            skills = ",".join(skills)

        values = (

            candidate.get("full_name"),

            candidate.get("email"),

            candidate.get("phone"),

            candidate.get("linkedin"),

            candidate.get("city"),

            candidate.get("state"),

            candidate.get("country"),

            skills,

            candidate.get("experience_years"),

            candidate.get("current_company"),

            candidate.get("designation")
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        candidate_id = cursor.lastrowid

        cursor.close()

        connection.close()

        return candidate_id


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
                raw_json

            )

            VALUES (%s, %s)
        """

        values = (

            candidate_id,

            str(raw_data)
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        cursor.close()

        connection.close()