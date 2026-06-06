from db import get_connection


class SalarySlipRepository:

    @staticmethod
    def save_salary_slip_result(

        candidate_id,
        verification_id,
        employee_name,
        employee_id,
        designation,
        salary_amount,
        net_salary,
        gross_salary,
        pan_number,
        uan_number,
        bank_account_last4,
        document_type,
        fraud_score,
        fraud_flags,
        extraction_status,
        provider_name,
        raw_text
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO salary_slip_results (

                candidate_id,
                verification_id,
                employee_name,
                employee_id,
                designation,
                salary_amount,
                net_salary,
                gross_salary,
                pan_number,
                uan_number,
                bank_account_last4,
                document_type,
                fraud_score,
                fraud_flags,
                extraction_status,
                provider_name,
                raw_text

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
            employee_name,
            employee_id,
            designation,
            salary_amount,
            net_salary,
            gross_salary,
            pan_number,
            uan_number,
            bank_account_last4,
            document_type,
            fraud_score,
            fraud_flags,
            extraction_status,
            provider_name,
            raw_text
        )

        cursor.execute(query, values)

        connection.commit()

        salary_slip_id = cursor.lastrowid

        cursor.close()

        connection.close()

        return salary_slip_id

    @staticmethod
    def save_api_log(

        module_name,
        provider_name,
        endpoint,
        request_payload,
        response_payload,
        status_code
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO api_logs (

                module_name,
                provider_name,
                endpoint,
                request_payload,
                response_payload,
                status_code

            )

            VALUES (

                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """

        values = (

            module_name,
            provider_name,
            endpoint,
            request_payload,
            response_payload,
            status_code
        )

        cursor.execute(query, values)

        connection.commit()

        cursor.close()

        connection.close()

    @staticmethod
    def save_salary_slip_document(

        candidate_id,
        verification_id,
        original_file_name,
        stored_file_name,
        file_path,
        file_size,
        mime_type,
        upload_status
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO salary_slip_documents (

                candidate_id,
                verification_id,
                original_file_name,
                stored_file_name,
                file_path,
                file_size,
                mime_type,
                upload_status

            )

            VALUES (

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
            original_file_name,
            stored_file_name,
            file_path,
            file_size,
            mime_type,
            upload_status
        )

        cursor.execute(query, values)

        connection.commit()

        cursor.close()

        connection.close()

    @staticmethod
    def save_salary_slip_log(

        candidate_id,
        verification_id,
        file_name,
        request_payload,
        response_payload,
        processing_status,
        error_message
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO salary_slip_logs (

                candidate_id,
                verification_id,
                file_name,
                request_payload,
                response_payload,
                processing_status,
                error_message

            )

            VALUES (

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
            file_name,
            request_payload,
            response_payload,
            processing_status,
            error_message
        )

        cursor.execute(query, values)

        connection.commit()

        cursor.close()

        connection.close()

    @staticmethod
    def save_fraud_check(

        salary_slip_id,
        fraud_type,
        fraud_score,
        fraud_status,
        remarks
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO salary_slip_fraud_checks (

                salary_slip_id,
                fraud_type,
                fraud_score,
                fraud_status,
                remarks

            )

            VALUES (

                %s,
                %s,
                %s,
                %s,
                %s
            )
        """

        values = (

            salary_slip_id,
            fraud_type,
            fraud_score,
            fraud_status,
            remarks
        )

        cursor.execute(query, values)

        connection.commit()

        cursor.close()

        connection.close()