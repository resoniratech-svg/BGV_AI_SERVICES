from db import get_connection

from datetime import datetime


class ProviderUsageRepository:

    @staticmethod
    def get_monthly_usage(

        provider_name,
        verification_type
    ):

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        usage_month = datetime.now().strftime(
            "%Y-%m"
        )

        query = """

            SELECT total_count

            FROM provider_usage_tracking

            WHERE provider_name = %s
            AND verification_type = %s
            AND usage_month = %s

        """

        values = (

            provider_name,
            verification_type,
            usage_month
        )

        cursor.execute(
            query,
            values
        )

        result = cursor.fetchone()

        cursor.close()

        connection.close()

        if result:

            return result["total_count"]

        return 0

    @staticmethod
    def increment_usage(

        provider_name,
        verification_type
    ):

        connection = get_connection()

        cursor = connection.cursor()

        usage_month = datetime.now().strftime(
            "%Y-%m"
        )

        check_query = """

            SELECT id

            FROM provider_usage_tracking

            WHERE provider_name = %s
            AND verification_type = %s
            AND usage_month = %s

        """

        values = (

            provider_name,
            verification_type,
            usage_month
        )

        cursor.execute(
            check_query,
            values
        )

        existing = cursor.fetchone()

        # ==========================================
        # UPDATE EXISTING RECORD
        # ==========================================

        if existing:

            update_query = """

                UPDATE provider_usage_tracking

                SET total_count = total_count + 1

                WHERE id = %s

            """

            cursor.execute(

                update_query,

                (
                    existing[0],
                )
            )

        # ==========================================
        # CREATE NEW RECORD
        # ==========================================

        else:

            insert_query = """

                INSERT INTO provider_usage_tracking (

                    provider_name,
                    verification_type,
                    usage_month,
                    total_count

                )

                VALUES (

                    %s,
                    %s,
                    %s,
                    %s
                )

            """

            cursor.execute(

                insert_query,

                (

                    provider_name,
                    verification_type,
                    usage_month,
                    1
                )
            )

        connection.commit()

        cursor.close()

        connection.close()