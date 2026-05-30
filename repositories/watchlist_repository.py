from db import get_connection


class WatchlistRepository:

    @staticmethod
    def save_aml_screening_result(

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
            INSERT INTO aml_screening_results (

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
    def save_global_watchlist_result(

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
            INSERT INTO global_watchlist_results (

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