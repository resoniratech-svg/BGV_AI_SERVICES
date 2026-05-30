from db import get_connection


class ReportRepository:

    @staticmethod
    def get_candidate_bgv_data(

        candidate_id
    ):

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        final_data = {}

        # ==========================================
        # PASSPORT
        # ==========================================

        cursor.execute(

            """

            SELECT *

            FROM passport_results

            WHERE candidate_id = %s

            ORDER BY id DESC

            LIMIT 1

            """,

            (candidate_id,)
        )

        final_data["passport"] = (
            cursor.fetchone()
        )

        # ==========================================
        # DRIVING LICENSE
        # ==========================================

        cursor.execute(

            """

            SELECT *

            FROM driving_license_results

            WHERE candidate_id = %s

            ORDER BY id DESC

            LIMIT 1

            """,

            (candidate_id,)
        )

        final_data["driving_license"] = (
            cursor.fetchone()
        )

        # ==========================================
        # AML
        # ==========================================

        cursor.execute(

            """

            SELECT *

            FROM aml_screening_results

            WHERE candidate_id = %s

            ORDER BY id DESC

            LIMIT 1

            """,

            (candidate_id,)
        )

        final_data["aml"] = (
            cursor.fetchone()
        )

        # ==========================================
        # WATCHLIST
        # ==========================================

        cursor.execute(

            """
            SELECT *

            FROM global_watchlist_results

            WHERE verification_id = %s


            ORDER BY id DESC

            LIMIT 1

            """,

            (
                final_data["aml"]["verification_id"]
                if final_data["aml"]
                else 0,
            )
        )

        final_data["watchlist"] = (
            cursor.fetchone()
        )

        cursor.close()

        connection.close()

        return final_data