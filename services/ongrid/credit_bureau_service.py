import json

from services.ongrid.ongrid_client import OnGridClient
from repositories.credit_bureau_repository import CreditBureauRepository
from repositories.provider_usage_repository import ProviderUsageRepository


class CreditBureauService:

    @staticmethod
    def verify_credit_bureau(candidate_id, bgv_id, payload):

        ####################################################
        # REQUEST
        ####################################################
        print("=" * 80)
        print("CREDIT BUREAU REQUEST")
        print(json.dumps(payload, indent=4))
        print("=" * 80)

        ####################################################
        # GRIDLINES API
        ####################################################
        response = OnGridClient.post(
            "/profile-api/bureau/fetch-profile",
            payload
        )

        ####################################################
        # LOG RESPONSE
        ####################################################
        print("=" * 80)
        print("CREDIT BUREAU RESPONSE")
        print(json.dumps(response, indent=4))
        print("=" * 80)

        ####################################################
        # VALIDATIONS
        ####################################################
        if not response:
            raise Exception("Empty Credit Bureau response.")

        status = response.get("status")

        if status != 200:
            if status == 429:
                raise Exception(
                    "Gridlines API rate limit exceeded. Please try again later."
                )
            elif status == 401:
                raise Exception("Gridlines authentication failed.")
            elif status == 403:
                raise Exception("Gridlines API access denied.")
            elif status == 404:
                raise Exception("Gridlines API endpoint not found.")
            else:
                raise Exception(
                    response.get(
                        "raw_response",
                        "Credit Bureau verification failed."
                    )
                )

        # Parse success payload data
        data = response.get("data", {})
        code = data.get("code")

        ####################################################
        # RESPONSE CODES MANAGEMENT
        ####################################################
        if code == "1005":
            pass
        elif code == "1004":
            raise Exception("No Bureau records found for this candidate.")
        else:
            raise Exception(
                data.get(
                    "message",
                    "Credit Bureau verification failed."
                )
            )

        ####################################################
        # SAVE MAIN RESULT
        ####################################################
        result_id = CreditBureauRepository.save_credit_bureau_result(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            request_id=response.get("request_id"),
            transaction_id=response.get("transaction_id"),
            verification_status="COMPLETED",
            response_code=code,
            response_message=data.get("message"),
            provider_name="GRIDLINES",
            api_reference_id=response.get("request_id"),
            raw_response=response
        )

        ####################################################
        # PERSONAL INFORMATION
        ####################################################
        personal = data.get("personal_information", {})
        documents = data.get("national_document_data", {})

        CreditBureauRepository.save_personal_information(
            credit_bureau_result_id=result_id,
            full_name=personal.get("full_name"),
            first_name=personal.get("first_name"),
            last_name=personal.get("last_name"),
            gender=personal.get("gender"),
            age=personal.get("age"),
            date_of_birth=personal.get("date_of_birth"),
            pan_number=documents.get("pan"),
            aadhaar_number=documents.get("aadhaar"),
            passport_number=documents.get("passport"),
            driving_license_number=documents.get("driving_license"),
            voter_id=documents.get("voter_id"),
            ration_card_number=documents.get("ration_card")
        )

        ####################################################
        # ADDRESSES
        ####################################################
        for address in data.get("addresses", []):
            CreditBureauRepository.save_contact_information(
                credit_bureau_result_id=result_id,
                contact_type="ADDRESS",
                value=address.get("address"),
                state=address.get("state"),
                pincode=address.get("pincode"),
                address_type=address.get("address_type"),
                reported_date=address.get("reported_date"),
                serial_number=None
            )

        ####################################################
        # PHONES
        ####################################################
        for phone in data.get("phone_numbers", []):
            CreditBureauRepository.save_contact_information(
                credit_bureau_result_id=result_id,
                contact_type="PHONE",
                value=phone.get("number"),
                state=None,
                pincode=None,
                address_type=None,
                reported_date=phone.get("reported_date"),
                serial_number=phone.get("serial_number")
            )

        ####################################################
        # EMAILS
        ####################################################
        for email in data.get("email_addresses", []):
            CreditBureauRepository.save_contact_information(
                credit_bureau_result_id=result_id,
                contact_type="EMAIL",
                value=email.get("email"),
                state=None,
                pincode=None,
                address_type=None,
                reported_date=email.get("reported_date"),
                serial_number=email.get("serial_number")
            )

        ####################################################
        # CREDIT ACCOUNTS
        ####################################################
        for account in data.get("credit_accounts", []):
            CreditBureauRepository.save_credit_account(
                credit_bureau_result_id=result_id,
                account_number=account.get("account_number"),
                institution=account.get("institution"),
                account_type=account.get("account_type"),
                ownership_type=account.get("ownership_type"),
                balance=account.get("balance"),
                past_due_amount=account.get("past_due_amount"),
                open_status=account.get("open_status"),
                account_status=account.get("account_status"),
                date_opened=account.get("date_opened"),
                date_reported=account.get("date_reported"),
                source=account.get("source"),
                raw_account_response=account
            )

        ####################################################
        # SUMMARY
        ####################################################
        summary = data.get("summary", {})

        CreditBureauRepository.save_summary(
            credit_bureau_result_id=result_id,
            credit_score=summary.get("credit_score"),
            score_name=summary.get("score_name"),
            score_version=summary.get("score_version"),
            total_accounts=summary.get("total_accounts"),
            active_accounts=summary.get("active_accounts"),
            write_off_accounts=summary.get("write_off_accounts"),
            past_due_accounts=summary.get("past_due_accounts"),
            zero_balance_accounts=summary.get("zero_balance_accounts"),
            total_balance=summary.get("total_balance"),
            total_credit_limit=summary.get("total_credit_limit"),
            total_sanction_amount=summary.get("total_sanction_amount"),
            highest_credit=summary.get("highest_credit"),
            highest_balance=summary.get("highest_balance"),
            average_open_balance=summary.get("average_open_balance"),
            total_monthly_payment=summary.get("total_monthly_payment"),
            oldest_account=summary.get("oldest_account"),
            recent_account=summary.get("recent_account"),
            total_past_due=summary.get("total_past_due")
        )

        ####################################################
        # SCORE FACTORS
        ####################################################
        for factor in data.get("score_factors", []):
            CreditBureauRepository.save_score_factor(
                credit_bureau_result_id=result_id,
                factor_type=factor.get("factor_type"),
                factor_code=factor.get("factor_code"),
                description=factor.get("description")
            )

        ####################################################
        # PROVIDER USAGE
        ####################################################
        ProviderUsageRepository.increment_usage(
            provider_name="GRIDLINES",
            verification_type="CREDIT_BUREAU"
        )

        ####################################################
        # RETURN
        ####################################################
        return {
            "success": True,
            "provider": "GRIDLINES",
            "verification_status": "COMPLETED",
            "credit_bureau_result_id": result_id,
            "request_id": response.get("request_id"),
            "transaction_id": response.get("transaction_id")
        }