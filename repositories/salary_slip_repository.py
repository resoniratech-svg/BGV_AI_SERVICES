from db import get_connection


class SalarySlipRepository:
    ###############################################################
    # SAVE SALARY SLIP OCR RESULT
    ###############################################################

    @staticmethod
    def save_salary_slip_ocr_result(
        candidate_id,
        bgv_id,
        document_id,
        employee_name,
        employee_id,
        pan_number,
        uan_number,
        bank_account_number,
        pf_number,
        grade,
        designation,
        company_business_name,
        office_state,
        office_address,
        joining_date,
        payslip_date,
        pf_amount,
        net_pay,
        provider_name,
        api_reference_id,
        raw_response,
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """

        INSERT INTO salary_slip_ocr_results
        (

            candidate_id,
            bgv_id,
            document_id,
            employee_name,
            employee_id,
            pan_number,
            uan_number,
            bank_account_number,
            pf_number,
            grade,
            designation,
            company_business_name,
            office_state,
            office_address,
            joining_date,
            payslip_date,
            pf_amount,
            net_pay,
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
            document_id,
            employee_name,
            employee_id,
            pan_number,
            uan_number,
            bank_account_number,
            pf_number,
            grade,
            designation,
            company_business_name,
            office_state,
            office_address,
            joining_date,
            payslip_date,
            pf_amount,
            net_pay,
            provider_name,
            api_reference_id,
            raw_response,
        )

        cursor.execute(query, values)

        connection.commit()

        salary_slip_result_id = cursor.lastrowid

        cursor.close()

        connection.close()

        return salary_slip_result_id

    ###############################################################
    # GET SALARY SLIP OCR RESULT
    ###############################################################

    @staticmethod
    def get_salary_slip_ocr_result(candidate_id):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """

            SELECT *

            FROM salary_slip_ocr_results

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

    ###############################################################
    # UPDATE SALARY SLIP OCR RESULT
    ###############################################################

    @staticmethod
    def update_salary_slip_ocr_result(
        result_id,
        employee_name,
        employee_id,
        pan_number,
        uan_number,
        bank_account_number,
        pf_number,
        grade,
        designation,
        company_business_name,
        office_state,
        office_address,
        joining_date,
        payslip_date,
        pf_amount,
        net_pay,
        provider_name,
        api_reference_id,
        raw_response,
    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """

            UPDATE salary_slip_ocr_results

            SET

                employee_name=%s,
                employee_id=%s,
                pan_number=%s,
                uan_number=%s,
                bank_account_number=%s,
                pf_number=%s,
                grade=%s,
                designation=%s,
                company_business_name=%s,
                office_state=%s,
                office_address=%s,
                joining_date=%s,
                payslip_date=%s,
                pf_amount=%s,
                net_pay=%s,
                provider_name=%s,
                api_reference_id=%s,
                raw_response=%s,
                updated_at=NOW()

            WHERE id=%s

            """,
            (
                employee_name,
                employee_id,
                pan_number,
                uan_number,
                bank_account_number,
                pf_number,
                grade,
                designation,
                company_business_name,
                office_state,
                office_address,
                joining_date,
                payslip_date,
                pf_amount,
                net_pay,
                provider_name,
                api_reference_id,
                raw_response,
                result_id,
            ),
        )

        connection.commit()

        cursor.close()

        connection.close()
