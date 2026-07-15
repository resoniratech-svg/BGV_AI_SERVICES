from db import get_connection


class ConsentRepository:

    ###############################################################
    # SAVE CANDIDATE CONSENT
    ###############################################################

    @staticmethod
    def save_candidate_consent(

            candidate_id,
            bgv_id,
            verification_type,
            consent_status,
            consent_text,
            consent_version,
            consent_source,
            consent_given_at,
            ip_address,
            user_agent,
            provider_name,
            api_reference_id,
            raw_response

    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO candidate_consents
            (
                candidate_id,
                bgv_id,
                verification_type,
                consent_status,
                consent_text,
                consent_version,
                consent_source,
                consent_given_at,
                ip_address,
                user_agent,
                provider_name,
                api_reference_id,
                raw_response
            )

            VALUES
            (
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
                %s,
                %s,
                %s
            )
            """,
            (
                candidate_id,
                bgv_id,
                verification_type,
                consent_status,
                consent_text,
                consent_version,
                consent_source,
                consent_given_at,
                ip_address,
                user_agent,
                provider_name,
                api_reference_id,
                raw_response
            )
        )

        connection.commit()

        consent_id = cursor.lastrowid

        cursor.close()

        connection.close()

        return consent_id

    ###############################################################
    # GET CANDIDATE CONSENT
    ###############################################################

    @staticmethod
    def get_candidate_consent(

            candidate_id,
            bgv_id,
            verification_type

    ):

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM candidate_consents
            WHERE candidate_id=%s
            AND bgv_id=%s
            AND verification_type=%s
            ORDER BY id DESC
            LIMIT 1
            """,
            (
                candidate_id,
                bgv_id,
                verification_type
            )
        )

        result = cursor.fetchone()

        cursor.close()

        connection.close()

        return result

    ###############################################################
    # UPDATE CANDIDATE CONSENT
    ###############################################################

    @staticmethod
    def update_candidate_consent(

            consent_id,
            consent_status,
            consent_given_at,
            ip_address,
            user_agent,
            provider_name,
            api_reference_id,
            raw_response

    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE candidate_consents
            SET
                consent_status=%s,
                consent_given_at=%s,
                ip_address=%s,
                user_agent=%s,
                provider_name=%s,
                api_reference_id=%s,
                raw_response=%s
            WHERE id=%s
            """,
            (
                consent_status,
                consent_given_at,
                ip_address,
                user_agent,
                provider_name,
                api_reference_id,
                raw_response,
                consent_id
            )
        )

        connection.commit()

        cursor.close()

        connection.close()

    ###############################################################
    # EXPIRE CONSENT
    ###############################################################

    @staticmethod
    def expire_candidate_consent(

            consent_id

    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE candidate_consents
            SET
                consent_status='EXPIRED'
            WHERE id=%s
            """,
            (
                consent_id,
            )
        )

        connection.commit()

        cursor.close()

        connection.close()

        ####################################################
    # UPDATE CANDIDATE CONSENT
    ####################################################

    @staticmethod
    def update_candidate_consent(

            candidate_id,
            bgv_id,
            verification_type,
            consent_status,
            consent_text,
            consent_version,
            consent_source,
            consent_given_at,
            ip_address,
            user_agent,
            provider_name=None,
            api_reference_id=None,
            raw_response=None

    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE candidate_consents

            SET

                consent_status=%s,

                consent_text=%s,

                consent_version=%s,

                consent_source=%s,

                consent_given_at=%s,

                ip_address=%s,

                user_agent=%s,

                provider_name=%s,

                api_reference_id=%s,

                raw_response=%s,

                updated_at=NOW()

            WHERE

                candidate_id=%s

            AND

                bgv_id=%s

            AND

                verification_type=%s
            """,
            (

                consent_status,

                consent_text,

                consent_version,

                consent_source,

                consent_given_at,

                ip_address,

                user_agent,

                provider_name,

                api_reference_id,

                raw_response,

                candidate_id,

                bgv_id,

                verification_type

            )
        )

        connection.commit()

        cursor.close()

        connection.close()