from db import get_connection


class FaceMatchRepository:
    @staticmethod
    def save_result(
        candidate_id,
        bgv_id,
        document_id,
        confidence_score,
        verification_status,
        provider_name,
        api_reference_id,
        raw_response,
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """

        INSERT INTO face_match_results(


            candidate_id,

            bgv_id,

            document_id,


            confidence_score,


            verification_status,


            provider_name,


            api_reference_id,


            raw_response


        )


        VALUES(

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

        cursor.execute(
            query,
            (
                candidate_id,
                bgv_id,
                document_id,
                confidence_score,
                verification_status,
                provider_name,
                api_reference_id,
                raw_response,
            ),
        )

        connection.commit()

        cursor.close()

        connection.close()

    @staticmethod
    def get_result(candidate_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        query = """


        SELECT *


        FROM face_match_results


        WHERE candidate_id=%s


        ORDER BY id DESC


        LIMIT 1


        """

        cursor.execute(query, (candidate_id,))

        result = cursor.fetchone()

        cursor.close()

        connection.close()

        return result

    # ==========================================


# GET FACE MATCH RESULT
# ==========================================


# @staticmethod
# def get_result(candidate_id):

#     connection = get_connection()

#     cursor = connection.cursor(dictionary=True)

#     query = """

#         SELECT *

#         FROM face_match_results

#         WHERE candidate_id=%s

#         ORDER BY id DESC

#         LIMIT 1

#     """

#     cursor.execute(query, (candidate_id,))

#     result = cursor.fetchone()

#     cursor.close()

#     connection.close()

#     return result
