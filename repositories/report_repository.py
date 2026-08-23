from db import get_connection


class ReportRepository:
    @staticmethod
    def get_candidate_bgv_data(candidate_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
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
            (candidate_id,),
        )
        final_data["passport"] = cursor.fetchone()

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
            (candidate_id,),
        )
        final_data["driving_license"] = cursor.fetchone()

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
            (candidate_id,),
        )
        final_data["aml"] = cursor.fetchone()

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
            (final_data["aml"]["verification_id"] if final_data["aml"] else 0,),
        )
        final_data["watchlist"] = cursor.fetchone()

        cursor.close()
        connection.close()

        return final_data

    @staticmethod
    def save_report_details(report_data):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO bgv_reports (
            candidate_id,
            report_reference_id,
            report_name,
            report_type,
            report_status,
            verification_status,
            file_name,
            file_path,
            file_url,
            storage_provider
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            report_data["candidate_id"],
            report_data["report_reference_id"],
            report_data["report_name"],
            report_data["report_type"],
            report_data["report_status"],
            report_data["verification_status"],
            report_data["file_name"],
            report_data["file_path"],
            report_data["file_url"],
            report_data["storage_provider"],
        )

        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()

    # Change 3: Added update_report_details below save_report_details
    @staticmethod
    def update_report_details(report_data):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        UPDATE bgv_reports
        SET
            report_reference_id = %s,
            report_name = %s,
            report_type = %s,
            report_status = %s,
            verification_status = %s,
            file_name = %s,
            file_path = %s,
            file_url = %s,
            storage_provider = %s
        WHERE candidate_id = %s
        """

        values = (
            report_data["report_reference_id"],
            report_data["report_name"],
            report_data["report_type"],
            report_data["report_status"],
            report_data["verification_status"],
            report_data["file_name"],
            report_data["file_path"],
            report_data["file_url"],
            report_data["storage_provider"],
            report_data["candidate_id"],
        )

        cursor.execute(query, values)

        connection.commit()

        cursor.close()

        connection.close()

    @staticmethod
    def get_report_history():
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT *
        FROM bgv_reports
        ORDER BY id DESC
        """

        cursor.execute(query)
        reports = cursor.fetchall()
        cursor.close()
        connection.close()

        return reports

    @staticmethod
    def get_latest_report(candidate_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT *
        FROM bgv_reports
        WHERE candidate_id = %s
        ORDER BY id DESC
        LIMIT 1
        """

        cursor.execute(query, (candidate_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        return result

    # Change 2: Added get_report_by_candidate below get_latest_report
    @staticmethod
    def get_report_by_candidate(candidate_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT *
        FROM bgv_reports
        WHERE candidate_id = %s
        LIMIT 1
        """

        cursor.execute(query, (candidate_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        return result

    # ==========================================
    # FETCH DATABASE DATA
    # ==========================================
    @staticmethod
    def get_candidate_details(candidate_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            CONCAT(
                first_name,
                ' ',
                COALESCE(last_name, '')
            ) AS full_name
        FROM candidates
        WHERE id = %s
        """

        cursor.execute(query, (candidate_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        return result

    @staticmethod
    def get_candidate_summary(candidate_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT *
        FROM candidate_verification_summary
        WHERE candidate_id = %s
        LIMIT 1
        """

        cursor.execute(query, (candidate_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        # Change 1: Fixed returning the result instead of None
        return result
