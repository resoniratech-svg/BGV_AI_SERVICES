from datetime import datetime

from db import get_connection


def get_current_month_usage():
    """
    Returns current month's Didit Passport + DL usage count.
    """

    current_month = datetime.now().strftime("%Y-%m")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT verification_count
        FROM provider_usage
        WHERE provider = %s
        AND verification_type = %s
        AND usage_month = %s
        """,
        (
            "didit",
            "passport_dl",
            current_month
        )
    )

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if not result:
        return 0

    return result["verification_count"]