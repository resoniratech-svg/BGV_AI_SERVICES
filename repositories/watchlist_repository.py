from db import get_connection


class WatchlistRepository:

    @staticmethod
    def save_watchlist_result(

        candidate_id,
        verification_id,
        full_name,
        country,
        aml_status,
        risk_level,
        pep_match,
        sanctions_match,
        adverse_media_match,
        provider_name,
        raw_response
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO watchlist_results (

                candidate_id,
                verification_id,
                full_name,
                country,
                aml_status,
                risk_level,
                pep_match,
                sanctions_match,
                adverse_media_match,
                provider_name,
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
                %s,
                %s,
                %s,
                %s
            )
        """

        values = (

            candidate_id,
            verification_id,
            full_name,
            country,
            aml_status,
            risk_level,
            pep_match,
            sanctions_match,
            adverse_media_match,
            provider_name,
            raw_response
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        cursor.close()

        connection.close()

    @staticmethod
    def get_watchlist_result(

        candidate_id
    ):

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
            SELECT *

            FROM watchlist_results

            WHERE candidate_id = %s
        """

        cursor.execute(
            query,
            (candidate_id,)
        )

        result = cursor.fetchall()

        cursor.close()

        connection.close()

        return result