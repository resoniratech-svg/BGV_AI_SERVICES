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

        try:

            print("WATCHLIST INSERT STARTED")

            connection = get_connection()

            print("DB CONNECTED")

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

            print("VALUES:", values)

            cursor.execute(
                query,
                values
            )

            print("WATCHLIST INSERT EXECUTED")

            connection.commit()

            print("WATCHLIST INSERT COMMITTED")

            cursor.close()

            connection.close()

        except Exception as e:

            print("WATCHLIST INSERT ERROR:", str(e))