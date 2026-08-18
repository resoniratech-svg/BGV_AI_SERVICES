import json


from db import get_connection


class CreditBureauRepository:
    ###############################################################
    # MAIN RESULT
    ###############################################################

    @staticmethod
    def save_credit_bureau_result(
        candidate_id,
        bgv_id,
        request_id,
        transaction_id,
        verification_status,
        response_code,
        response_message,
        provider_name,
        api_reference_id,
        raw_response,
    ):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO credit_bureau_results
            (
                candidate_id,
                bgv_id,
                request_id,
                transaction_id,
                verification_status,
                response_code,
                response_message,
                provider_name,
                api_reference_id,
                raw_response
            )
            VALUES
            (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )
            """,
            (
                candidate_id,
                bgv_id,
                request_id,
                transaction_id,
                verification_status,
                response_code,
                response_message,
                provider_name,
                api_reference_id,
                json.dumps(raw_response, default=str),  # Safely handles dates/decimals
            ),
        )

        connection.commit()

        result_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return result_id

    ###############################################################
    # PERSONAL INFORMATION
    ###############################################################

    @staticmethod
    def save_personal_information(
        credit_bureau_result_id,
        full_name,
        first_name,
        last_name,
        gender,
        age,
        date_of_birth,
        pan_number,
        aadhaar_number,
        passport_number,
        driving_license_number,
        voter_id,
        ration_card_number,
    ):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO credit_bureau_personal_information
            (
                credit_bureau_result_id,
                full_name,
                first_name,
                last_name,
                gender,
                age,
                date_of_birth,
                pan_number,
                aadhaar_number,
                passport_number,
                driving_license_number,
                voter_id,
                ration_card_number
            )
            VALUES
            (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )
            """,
            (
                credit_bureau_result_id,
                full_name,
                first_name,
                last_name,
                gender,
                age,
                date_of_birth,
                pan_number,
                aadhaar_number,
                passport_number,
                driving_license_number,
                voter_id,
                ration_card_number,
            ),
        )

        connection.commit()

        cursor.close()
        connection.close()

    ###############################################################
    # CONTACT INFORMATION
    ###############################################################

    @staticmethod
    def save_contact_information(
        credit_bureau_result_id,
        contact_type,
        value,
        state,
        pincode,
        address_type,
        reported_date,
        serial_number,
    ):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO credit_bureau_contact_information
            (
                credit_bureau_result_id,
                contact_type,
                value,
                state,
                pincode,
                address_type,
                reported_date,
                serial_number
            )
            VALUES
            (
                %s,%s,%s,%s,%s,%s,%s,%s
            )
            """,
            (
                credit_bureau_result_id,
                contact_type,
                value,
                state,
                pincode,
                address_type,
                reported_date,
                serial_number,
            ),
        )

        connection.commit()

        cursor.close()
        connection.close()

    ###############################################################
    # CREDIT ACCOUNT
    ###############################################################

    @staticmethod
    def save_credit_account(
        credit_bureau_result_id,
        account_number,
        institution,
        account_type,
        ownership_type,
        balance,
        past_due_amount,
        open_status,
        account_status,
        date_opened,
        date_reported,
        source,
        raw_account_response,
    ):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO credit_bureau_accounts
            (
                credit_bureau_result_id,
                account_number,
                institution,
                account_type,
                ownership_type,
                balance,
                past_due_amount,
                open_status,
                account_status,
                date_opened,
                date_reported,
                source,
                raw_account_response
            )
            VALUES
            (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )
            """,
            (
                credit_bureau_result_id,
                account_number,
                institution,
                account_type,
                ownership_type,
                balance,
                past_due_amount,
                open_status,
                account_status,
                date_opened,
                date_reported,
                source,
                json.dumps(
                    raw_account_response, default=str
                ),  # Safely handles dates/decimals
            ),
        )

        connection.commit()

        cursor.close()
        connection.close()

    ###############################################################
    # SUMMARY
    ###############################################################

    @staticmethod
    def save_summary(
        credit_bureau_result_id,
        credit_score,
        score_name,
        score_version,
        total_accounts,
        active_accounts,
        write_off_accounts,
        past_due_accounts,
        zero_balance_accounts,
        total_balance,
        total_credit_limit,
        total_sanction_amount,
        highest_credit,
        highest_balance,
        average_open_balance,
        total_monthly_payment,
        oldest_account,
        recent_account,
        total_past_due,
    ):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO credit_bureau_summary
            (
                credit_bureau_result_id,
                credit_score,
                score_name,
                score_version,
                total_accounts,
                active_accounts,
                write_off_accounts,
                past_due_accounts,
                zero_balance_accounts,
                total_balance,
                total_credit_limit,
                total_sanction_amount,
                highest_credit,
                highest_balance,
                average_open_balance,
                total_monthly_payment,
                oldest_account,
                recent_account,
                total_past_due
            )
            VALUES
            (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )
            """,
            (
                credit_bureau_result_id,
                credit_score,
                score_name,
                score_version,
                total_accounts,
                active_accounts,
                write_off_accounts,
                past_due_accounts,
                zero_balance_accounts,
                total_balance,
                total_credit_limit,
                total_sanction_amount,
                highest_credit,
                highest_balance,
                average_open_balance,
                total_monthly_payment,
                oldest_account,
                recent_account,
                total_past_due,
            ),
        )

        connection.commit()

        cursor.close()
        connection.close()

    ###############################################################
    # SCORE FACTORS
    ###############################################################

    @staticmethod
    def save_score_factor(
        credit_bureau_result_id, factor_type, factor_code, description
    ):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO credit_bureau_score_factors
            (
                credit_bureau_result_id,
                factor_type,
                factor_code,
                description
            )
            VALUES
            (
                %s,%s,%s,%s
            )
            """,
            (credit_bureau_result_id, factor_type, factor_code, description),
        )

        connection.commit()

        cursor.close()
        connection.close()

    ####################################################
    # GET CREDIT BUREAU RESULT
    ####################################################

    @staticmethod
    def get_credit_bureau_result(candidate_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM credit_bureau_results
            WHERE candidate_id=%s
            ORDER BY id DESC
            LIMIT 1
            """,
            (candidate_id,),
        )

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result

    ####################################################
    # GET PERSONAL INFORMATION
    ####################################################

    @staticmethod
    def get_personal_information(credit_bureau_result_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM credit_bureau_personal_information
            WHERE credit_bureau_result_id=%s
            LIMIT 1
            """,
            (credit_bureau_result_id,),
        )

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result

    ####################################################
    # GET CONTACT INFORMATION
    ####################################################

    @staticmethod
    def get_contact_information(credit_bureau_result_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM credit_bureau_contact_information
            WHERE credit_bureau_result_id=%s
            """,
            (credit_bureau_result_id,),
        )

        result = cursor.fetchall()

        cursor.close()
        connection.close()

        return result

    ####################################################
    # GET CREDIT ACCOUNTS
    ####################################################

    @staticmethod
    def get_credit_accounts(credit_bureau_result_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM credit_bureau_accounts
            WHERE credit_bureau_result_id=%s
            ORDER BY id
            """,
            (credit_bureau_result_id,),
        )

        result = cursor.fetchall()

        cursor.close()
        connection.close()

        return result

    ####################################################
    # GET CREDIT SUMMARY
    ####################################################

    @staticmethod
    def get_summary(credit_bureau_result_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM credit_bureau_summary
            WHERE credit_bureau_result_id=%s
            LIMIT 1
            """,
            (credit_bureau_result_id,),
        )

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result

    ####################################################
    # GET SCORE FACTORS
    ####################################################

    @staticmethod
    def get_score_factors(credit_bureau_result_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM credit_bureau_score_factors
            WHERE credit_bureau_result_id=%s
            ORDER BY id
            """,
            (credit_bureau_result_id,),
        )

        result = cursor.fetchall()

        cursor.close()
        connection.close()

        return result
