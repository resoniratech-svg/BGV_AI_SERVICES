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
            raw_response
        )

        cursor.execute(

            query,
            values
        )

        connection.commit()

        cursor.close()

        connection.close()