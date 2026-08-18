# import json

# from services.ongrid.ongrid_client import OnGridClient
# from repositories.credit_bureau_repository import CreditBureauRepository
# from repositories.provider_usage_repository import ProviderUsageRepository


# class CreditBureauService:
#     @staticmethod
#     def verify_credit_bureau(candidate_id, bgv_id, payload):

#         ####################################################
#         # REQUEST
#         ####################################################
#         print("=" * 80)
#         print("CREDIT BUREAU REQUEST")
#         print(json.dumps(payload, indent=4))
#         print("=" * 80)

#         ####################################################
#         # GRIDLINES API
#         ####################################################
#         response = OnGridClient.post("/profile-api/bureau/fetch-profile", payload)

#         ####################################################
#         # LOG RESPONSE
#         ####################################################
#         print("=" * 80)
#         print("CREDIT BUREAU RESPONSE")
#         print(json.dumps(response, indent=4))
#         print("=" * 80)

#         ####################################################
#         # VALIDATIONS
#         ####################################################
#         if not response:
#             raise Exception("Empty Credit Bureau response.")

#         status = response.get("status")

#         if status != 200:
#             if status == 429:
#                 raise Exception(
#                     "Gridlines API rate limit exceeded. Please try again later."
#                 )
#             elif status == 401:
#                 raise Exception("Gridlines authentication failed.")
#             elif status == 403:
#                 raise Exception("Gridlines API access denied.")
#             elif status == 404:
#                 raise Exception("Gridlines API endpoint not found.")
#             else:
#                 raise Exception(
#                     response.get("raw_response", "Credit Bureau verification failed.")
#                 )

#         # Parse success payload data
#         data = response.get("data", {})
#         code = data.get("code")

#         ####################################################
#         # RESPONSE CODES MANAGEMENT
#         ####################################################
#         if code == "1005":
#             pass
#         elif code == "1004":
#             raise Exception("No Bureau records found for this candidate.")
#         else:
#             raise Exception(data.get("message", "Credit Bureau verification failed."))

#         ####################################################
#         # SAVE MAIN RESULT
#         ####################################################
#         result_id = CreditBureauRepository.save_credit_bureau_result(
#             candidate_id=candidate_id,
#             bgv_id=bgv_id,
#             request_id=response.get("request_id"),
#             transaction_id=response.get("transaction_id"),
#             verification_status="COMPLETED",
#             response_code=code,
#             response_message=data.get("message"),
#             provider_name="GRIDLINES",
#             api_reference_id=response.get("request_id"),
#             raw_response=response,
#         )

#         ####################################################
#         # PERSONAL INFORMATION
#         ####################################################
#         personal = data.get("personal_information", {})
#         documents = data.get("national_document_data", {})

#         CreditBureauRepository.save_personal_information(
#             credit_bureau_result_id=result_id,
#             full_name=personal.get("full_name"),
#             first_name=personal.get("first_name"),
#             last_name=personal.get("last_name"),
#             gender=personal.get("gender"),
#             age=personal.get("age"),
#             date_of_birth=personal.get("date_of_birth"),
#             pan_number=documents.get("pan"),
#             aadhaar_number=documents.get("aadhaar"),
#             passport_number=documents.get("passport"),
#             driving_license_number=documents.get("driving_license"),
#             voter_id=documents.get("voter_id"),
#             ration_card_number=documents.get("ration_card"),
#         )

#         ####################################################
#         # ADDRESSES
#         ####################################################
#         for address in data.get("addresses", []):
#             CreditBureauRepository.save_contact_information(
#                 credit_bureau_result_id=result_id,
#                 contact_type="ADDRESS",
#                 value=address.get("address"),
#                 state=address.get("state"),
#                 pincode=address.get("pincode"),
#                 address_type=address.get("address_type"),
#                 reported_date=address.get("reported_date"),
#                 serial_number=None,
#             )

#         ####################################################
#         # PHONES
#         ####################################################
#         for phone in data.get("phone_numbers", []):
#             CreditBureauRepository.save_contact_information(
#                 credit_bureau_result_id=result_id,
#                 contact_type="PHONE",
#                 value=phone.get("number"),
#                 state=None,
#                 pincode=None,
#                 address_type=None,
#                 reported_date=phone.get("reported_date"),
#                 serial_number=phone.get("serial_number"),
#             )

#         ####################################################
#         # EMAILS
#         ####################################################
#         for email in data.get("email_addresses", []):
#             CreditBureauRepository.save_contact_information(
#                 credit_bureau_result_id=result_id,
#                 contact_type="EMAIL",
#                 value=email.get("email"),
#                 state=None,
#                 pincode=None,
#                 address_type=None,
#                 reported_date=email.get("reported_date"),
#                 serial_number=email.get("serial_number"),
#             )

#         ####################################################
#         # CREDIT ACCOUNTS
#         ####################################################
#         for account in data.get("credit_accounts", []):
#             CreditBureauRepository.save_credit_account(
#                 credit_bureau_result_id=result_id,
#                 account_number=account.get("account_number"),
#                 institution=account.get("institution"),
#                 account_type=account.get("account_type"),
#                 ownership_type=account.get("ownership_type"),
#                 balance=account.get("balance"),
#                 past_due_amount=account.get("past_due_amount"),
#                 open_status=account.get("open_status"),
#                 account_status=account.get("account_status"),
#                 date_opened=account.get("date_opened"),
#                 date_reported=account.get("date_reported"),
#                 source=account.get("source"),
#                 raw_account_response=account,
#             )

#         ####################################################
#         # SUMMARY
#         ####################################################
#         summary = data.get("summary", {})

#         CreditBureauRepository.save_summary(
#             credit_bureau_result_id=result_id,
#             credit_score=summary.get("credit_score"),
#             score_name=summary.get("score_name"),
#             score_version=summary.get("score_version"),
#             total_accounts=summary.get("total_accounts"),
#             active_accounts=summary.get("active_accounts"),
#             write_off_accounts=summary.get("write_off_accounts"),
#             past_due_accounts=summary.get("past_due_accounts"),
#             zero_balance_accounts=summary.get("zero_balance_accounts"),
#             total_balance=summary.get("total_balance"),
#             total_credit_limit=summary.get("total_credit_limit"),
#             total_sanction_amount=summary.get("total_sanction_amount"),
#             highest_credit=summary.get("highest_credit"),
#             highest_balance=summary.get("highest_balance"),
#             average_open_balance=summary.get("average_open_balance"),
#             total_monthly_payment=summary.get("total_monthly_payment"),
#             oldest_account=summary.get("oldest_account"),
#             recent_account=summary.get("recent_account"),
#             total_past_due=summary.get("total_past_due"),
#         )

#         ####################################################
#         # SCORE FACTORS
#         ####################################################
#         for factor in data.get("score_factors", []):
#             CreditBureauRepository.save_score_factor(
#                 credit_bureau_result_id=result_id,
#                 factor_type=factor.get("factor_type"),
#                 factor_code=factor.get("factor_code"),
#                 description=factor.get("description"),
#             )

#         ####################################################
#         # PROVIDER USAGE
#         ####################################################
#         ProviderUsageRepository.increment_usage(
#             provider_name="GRIDLINES", verification_type="CREDIT_BUREAU"
#         )

#         ####################################################
#         # RETURN
#         ####################################################
#         return {
#             "success": True,
#             "provider": "GRIDLINES",
#             "verification_status": "COMPLETED",
#             "credit_bureau_result_id": result_id,
#             "request_id": response.get("request_id"),
#             "transaction_id": response.get("transaction_id"),
#         }
import json

from services.ongrid.ongrid_client import OnGridClient
from repositories.credit_bureau_repository import CreditBureauRepository
from repositories.provider_usage_repository import ProviderUsageRepository


class CreditBureauService:
    ###############################################################
    # HELPER - EXTRACT DOCUMENT VALUE
    ###############################################################

    @staticmethod
    def _extract_document_value(document_data, document_name):
        """
        Gridlines returns national document data as arrays.

        Example:
        "pan": [
            {
                ...
            }
        ]

        This helper safely extracts the useful value regardless of
        whether Gridlines returns a direct string or an object.
        """

        if not document_data:
            return None

        value = document_data.get(document_name)

        if not value:
            return None

        # Example: ["ABCDE1234F"]
        if isinstance(value, list):
            if len(value) == 0:
                return None

            first = value[0]

            if isinstance(first, str):
                return first

            if isinstance(first, dict):
                # Try common possible fields
                for key in [
                    document_name,
                    "value",
                    "number",
                    "document_number",
                    "id",
                ]:
                    if first.get(key):
                        return first.get(key)

                # If no known field exists, return first value
                for item in first.values():
                    if item:
                        return item

        # Direct string
        if isinstance(value, str):
            return value

        # Direct dictionary
        if isinstance(value, dict):
            for key in [
                document_name,
                "value",
                "number",
                "document_number",
                "id",
            ]:
                if value.get(key):
                    return value.get(key)

        return None

    ###############################################################
    # VERIFY CREDIT BUREAU
    ###############################################################

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
            payload,
        )

        ####################################################
        # LOG RESPONSE
        ####################################################

        print("=" * 80)
        print("CREDIT BUREAU RESPONSE")
        print(json.dumps(response, indent=4, default=str))
        print("=" * 80)

        ####################################################
        # VALIDATE RESPONSE
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
                        "Credit Bureau verification failed.",
                    )
                )

        ####################################################
        # RESPONSE DATA
        ####################################################

        data = response.get("data", {})

        code = data.get("code")

        ####################################################
        # RESPONSE CODE
        ####################################################

        if code == "1005":
            print("CREDIT BUREAU PROFILE FOUND")

        elif code == "1004":
            raise Exception("No Bureau records found for this candidate.")

        else:
            raise Exception(
                data.get(
                    "message",
                    "Credit Bureau verification failed.",
                )
            )

        ####################################################
        # PROFILE DATA
        #
        # Gridlines response:
        #
        # data
        #   └── profile_data
        ####################################################

        profile_data = data.get("profile_data", {})

        if not profile_data:
            raise Exception(
                "Credit Bureau profile data not found in Gridlines response."
            )

        print("=" * 80)
        print("CREDIT BUREAU PROFILE DATA FOUND")
        print(json.dumps(profile_data, indent=4, default=str))
        print("=" * 80)

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
            api_reference_id=(
                response.get("reference_id") or response.get("request_id")
            ),
            raw_response=response,
        )

        print(
            "CREDIT BUREAU RESULT ID:",
            result_id,
        )

        ####################################################
        # PERSONAL INFORMATION
        ####################################################

        personal = profile_data.get(
            "personal_information",
            {},
        )

        ####################################################
        # NATIONAL DOCUMENT DATA
        ####################################################

        documents = profile_data.get(
            "national_document_data",
            {},
        )

        ####################################################
        # EXTRACT DOCUMENT VALUES
        ####################################################

        pan_number = CreditBureauService._extract_document_value(
            documents,
            "pan",
        )

        aadhaar_number = CreditBureauService._extract_document_value(
            documents,
            "aadhaar",
        )

        passport_number = CreditBureauService._extract_document_value(
            documents,
            "passport",
        )

        driving_license_number = CreditBureauService._extract_document_value(
            documents,
            "driving_license",
        )

        voter_id = CreditBureauService._extract_document_value(
            documents,
            "voter_id",
        )

        ration_card_number = CreditBureauService._extract_document_value(
            documents,
            "ration_card",
        )

        ####################################################
        # SAVE PERSONAL INFORMATION
        ####################################################

        CreditBureauRepository.save_personal_information(
            credit_bureau_result_id=result_id,
            full_name=personal.get("full_name"),
            first_name=personal.get("first_name"),
            last_name=personal.get("last_name"),
            gender=personal.get("gender"),
            age=personal.get("age"),
            date_of_birth=personal.get("date_of_birth"),
            pan_number=pan_number,
            aadhaar_number=aadhaar_number,
            passport_number=passport_number,
            driving_license_number=driving_license_number,
            voter_id=voter_id,
            ration_card_number=ration_card_number,
        )

        ####################################################
        # ADDRESSES
        #
        # Gridlines:
        #
        # address[]
        #   detailed_address
        #   state
        #   pincode
        #   type
        #   date_of_reporting
        ####################################################

        addresses = profile_data.get(
            "address",
            [],
        )

        if isinstance(addresses, dict):
            addresses = [addresses]

        for address in addresses:
            CreditBureauRepository.save_contact_information(
                credit_bureau_result_id=result_id,
                contact_type="ADDRESS",
                value=address.get("detailed_address"),
                state=address.get("state"),
                pincode=address.get("pincode"),
                address_type=address.get("type"),
                reported_date=address.get("date_of_reporting"),
                serial_number=None,
            )

        ####################################################
        # PHONE
        #
        # Gridlines:
        #
        # phone[]
        #   serial_number
        #   value
        #   reported_date
        ####################################################

        phone_numbers = profile_data.get(
            "phone",
            [],
        )

        if isinstance(phone_numbers, dict):
            phone_numbers = [phone_numbers]

        for phone in phone_numbers:
            CreditBureauRepository.save_contact_information(
                credit_bureau_result_id=result_id,
                contact_type="PHONE",
                value=phone.get("value"),
                state=None,
                pincode=None,
                address_type=None,
                reported_date=phone.get("reported_date"),
                serial_number=phone.get("serial_number"),
            )

        ####################################################
        # EMAIL
        #
        # Gridlines:
        #
        # email[]
        #   serial_number
        #   value
        #   reported_date
        ####################################################

        email_addresses = profile_data.get(
            "email",
            [],
        )

        if isinstance(email_addresses, dict):
            email_addresses = [email_addresses]

        for email in email_addresses:
            CreditBureauRepository.save_contact_information(
                credit_bureau_result_id=result_id,
                contact_type="EMAIL",
                value=email.get("value"),
                state=None,
                pincode=None,
                address_type=None,
                reported_date=email.get("reported_date"),
                serial_number=email.get("serial_number"),
            )

        ####################################################
        # CREDIT ACCOUNTS
        #
        # Gridlines:
        #
        # account_detail[]
        ####################################################

        accounts = profile_data.get(
            "account_detail",
            [],
        )

        if isinstance(accounts, dict):
            accounts = [accounts]

        for account in accounts:
            CreditBureauRepository.save_credit_account(
                credit_bureau_result_id=result_id,
                account_number=account.get("account_number"),
                institution=account.get("institution"),
                account_type=account.get("account_type"),
                ownership_type=account.get("ownership_type"),
                balance=account.get("balance"),
                past_due_amount=account.get("past_due_amount"),
                open_status=account.get("open"),
                account_status=account.get("account_status"),
                date_opened=account.get("date_opened"),
                date_reported=account.get("date_reported"),
                source=account.get("source"),
                raw_account_response=account,
            )

        ####################################################
        # ACCOUNT SUMMARY
        #
        # Gridlines:
        #
        # account_summary
        ####################################################

        account_summary = profile_data.get(
            "account_summary",
            {},
        )

        ####################################################
        # SCORE DETAIL
        #
        # Gridlines:
        #
        # score_detail[]
        ####################################################

        score_details = profile_data.get(
            "score_detail",
            [],
        )

        if isinstance(score_details, dict):
            score_details = [score_details]

        ####################################################
        # GET CREDIT SCORE
        ####################################################

        credit_score = None
        score_name = None
        score_version = None

        if score_details:
            first_score = score_details[0]

            credit_score = first_score.get("value")

            score_name = first_score.get("name")

            score_version = first_score.get("version")

        ####################################################
        # SAVE SUMMARY
        ####################################################

        CreditBureauRepository.save_summary(
            credit_bureau_result_id=result_id,
            credit_score=credit_score,
            score_name=score_name,
            score_version=score_version,
            total_accounts=(account_summary.get("number_of_accounts")),
            active_accounts=(account_summary.get("number_of_active_accounts")),
            write_off_accounts=(account_summary.get("number_of_write_offs")),
            past_due_accounts=(account_summary.get("number_of_past_due_accounts")),
            zero_balance_accounts=(
                account_summary.get("number_of_zero_balance_accounts")
            ),
            total_balance=(account_summary.get("total_balance_amount")),
            total_credit_limit=(account_summary.get("total_credit_limit")),
            total_sanction_amount=(account_summary.get("total_sanction_amount")),
            highest_credit=(account_summary.get("total_highest_credit")),
            highest_balance=(account_summary.get("single_highest_balance")),
            average_open_balance=(account_summary.get("average_open_balance")),
            total_monthly_payment=(account_summary.get("total_monthly_payment_amount")),
            oldest_account=(account_summary.get("oldest_account")),
            recent_account=(account_summary.get("recent_account")),
            total_past_due=(account_summary.get("total_past_due")),
        )

        ####################################################
        # SCORE FACTORS
        #
        # Gridlines:
        #
        # score_detail[]
        #   scoring_elements[]
        #       type
        #       code
        #       description
        ####################################################

        for score_detail in score_details:
            scoring_elements = score_detail.get(
                "scoring_elements",
                [],
            )

            if isinstance(scoring_elements, dict):
                scoring_elements = [scoring_elements]

            for factor in scoring_elements:
                CreditBureauRepository.save_score_factor(
                    credit_bureau_result_id=result_id,
                    factor_type=factor.get("type"),
                    factor_code=factor.get("code"),
                    description=factor.get("description"),
                )

        ####################################################
        # PROVIDER USAGE
        ####################################################

        ProviderUsageRepository.increment_usage(
            provider_name="GRIDLINES",
            verification_type="CREDIT_BUREAU",
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
            "transaction_id": response.get("transaction_id"),
        }
