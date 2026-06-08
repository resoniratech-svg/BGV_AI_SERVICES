from multiprocessing import connection

from db import get_connection


class DrivingLicenseRepository:

    @staticmethod
    def save_driving_license_result(
        candidate_id,
        bgv_id,
        verification_status,
        license_number,
        full_name,
        date_of_birth,
        issue_date,
        expiry_date,
        provider_name,
        api_reference_id,
        raw_response
    ):
        connection = get_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO driving_license_results (

                candidate_id,
                bgv_id,
                verification_status,
                license_number,
                full_name,
                date_of_birth,
                issue_date,
                expiry_date,
                api_reference_id,
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
                %s.
                %s
            )
        """

        values = (

            candidate_id,
            bgv_id,
            verification_status,
            license_number,
            full_name,
            date_of_birth,
            issue_date,
            expiry_date,
            provider_name,
            api_reference_id,
            raw_response
        )

        cursor.execute(

            query,
            values
        )

        connection.commit()
        driving_license_result_id = cursor.lastrowid

        cursor.close()
        connection.close()
        return driving_license_result_id