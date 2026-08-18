# # from repositories.bank_statement_repository import BankStatementRepository


# # class BankStatementResultService:
# #     ###############################################################
# #     # GET BANK STATEMENT RESULT
# #     ###############################################################

# #     @staticmethod
# #     def get_result(candidate_id, bgv_id):

# #         ###########################################################
# #         # GET RESULT
# #         ###########################################################

# #         result = BankStatementRepository.get_result(candidate_id, bgv_id)

# #         ###########################################################
# #         # VALIDATION
# #         ###########################################################

# #         if not result:
# #             raise Exception("Bank Statement result not found.")

# #         ###########################################################
# #         # RETURN
# #         ###########################################################

# #         return result
# import json
# import os

# from repositories.bank_statement_repository import BankStatementRepository


# class BankStatementResultService:
#     ###############################################################
#     # GET BANK STATEMENT RESULT
#     ###############################################################

#     @staticmethod
#     def get_result(candidate_id, bgv_id):

#         ###########################################################
#         # GET RESULT METADATA
#         ###########################################################

#         result = BankStatementRepository.get_result(
#             candidate_id,
#             bgv_id,
#         )

#         ###########################################################
#         # VALIDATION
#         ###########################################################

#         if not result:
#             raise Exception("Bank Statement result not found.")

#         ###########################################################
#         # GET JSON FILE PATH
#         ###########################################################

#         json_file_path = result.get("json_file_path")

#         report_data = None

#         if json_file_path:
#             try:
#                 ###################################################
#                 # HANDLE RELATIVE PATH
#                 ###################################################

#                 if not os.path.isabs(json_file_path):
#                     json_file_path = os.path.abspath(json_file_path)

#                 ###################################################
#                 # CHECK FILE
#                 ###################################################

#                 if os.path.exists(json_file_path):
#                     with open(
#                         json_file_path,
#                         "r",
#                         encoding="utf-8",
#                     ) as file:
#                         report_data = json.load(file)

#                 else:
#                     print("=" * 80)
#                     print("BANK STATEMENT JSON FILE NOT FOUND")
#                     print(f"Path: {json_file_path}")
#                     print("=" * 80)

#             except Exception as error:
#                 print("=" * 80)
#                 print("BANK STATEMENT JSON READ ERROR")
#                 print(error)
#                 print("=" * 80)

#         ###########################################################
#         # ATTACH REPORT DATA
#         ###########################################################

#         result["report_data"] = report_data

#         ###########################################################
#         # RETURN
#         ###########################################################

#         return result
import json
import os

import requests

from repositories.bank_statement_repository import BankStatementRepository


class BankStatementResultService:
    ###############################################################
    # GET BANK STATEMENT RESULT
    ###############################################################

    @staticmethod
    def get_result(candidate_id, bgv_id):

        ###########################################################
        # GET RESULT METADATA
        ###########################################################

        result = BankStatementRepository.get_result(
            candidate_id,
            bgv_id,
        )

        ###########################################################
        # VALIDATION
        ###########################################################

        if not result:
            raise Exception("Bank Statement result not found.")

        ###########################################################
        # INITIALIZE REPORT DATA
        ###########################################################

        report_data = None

        ###########################################################
        # GET JSON FILE PATH
        ###########################################################

        json_file_path = result.get("json_file_path")

        ###########################################################
        # GET PROVIDER JSON URL
        ###########################################################

        provider_json_url = result.get("provider_json_url")

        ###########################################################
        # DEBUG RESULT SOURCE
        ###########################################################

        print("=" * 80)
        print("BANK STATEMENT RESULT SOURCE")
        print("Candidate ID:", candidate_id)
        print("BGV ID:", bgv_id)
        print("JSON FILE PATH:", json_file_path)
        print("PROVIDER JSON URL:", provider_json_url)
        print("=" * 80)

        ###########################################################
        # STEP 1
        # TRY LOCAL JSON FILE
        ###########################################################

        if json_file_path:
            try:
                ###################################################
                # HANDLE RELATIVE PATH
                ###################################################

                if not os.path.isabs(json_file_path):
                    json_file_path = os.path.abspath(json_file_path)

                ###################################################
                # CHECK FILE
                ###################################################

                if os.path.exists(json_file_path):
                    print("=" * 80)
                    print("BANK STATEMENT JSON FILE FOUND")
                    print("Path:", json_file_path)
                    print("=" * 80)

                    ################################################
                    # READ JSON REPORT
                    ################################################

                    with open(
                        json_file_path,
                        "r",
                        encoding="utf-8",
                    ) as file:
                        report_data = json.load(file)

                else:
                    print("=" * 80)
                    print("BANK STATEMENT JSON FILE NOT FOUND")
                    print("Path:", json_file_path)
                    print("FALLING BACK TO PROVIDER JSON URL")
                    print("=" * 80)

            except json.JSONDecodeError as error:
                print("=" * 80)
                print("BANK STATEMENT JSON DECODE ERROR")
                print("Path:", json_file_path)
                print("Error:", error)
                print("FALLING BACK TO PROVIDER JSON URL")
                print("=" * 80)

            except Exception as error:
                print("=" * 80)
                print("BANK STATEMENT JSON READ ERROR")
                print("Path:", json_file_path)
                print("Error:", error)
                print("FALLING BACK TO PROVIDER JSON URL")
                print("=" * 80)

        else:
            print("=" * 80)
            print("BANK STATEMENT JSON FILE PATH IS EMPTY")
            print("FALLING BACK TO PROVIDER JSON URL")
            print("=" * 80)

        ###########################################################
        # STEP 2
        # FETCH JSON FROM PROVIDER URL
        ###########################################################

        if report_data is None and provider_json_url:
            try:
                print("=" * 80)
                print("BANK STATEMENT PROVIDER JSON FETCH")
                print("URL:", provider_json_url)
                print("=" * 80)

                ###################################################
                # REQUEST PROVIDER JSON
                ###################################################

                response = requests.get(
                    provider_json_url,
                    timeout=30,
                )

                ###################################################
                # CHECK HTTP STATUS
                ###################################################

                response.raise_for_status()

                ###################################################
                # PARSE JSON
                ###################################################

                report_data = response.json()

                print("=" * 80)
                print("BANK STATEMENT PROVIDER JSON FETCH SUCCESS")
                print("HTTP STATUS:", response.status_code)
                print("=" * 80)

            except requests.exceptions.RequestException as error:
                print("=" * 80)
                print("BANK STATEMENT PROVIDER JSON REQUEST ERROR")
                print("URL:", provider_json_url)
                print("Error:", error)
                print("=" * 80)

            except json.JSONDecodeError as error:
                print("=" * 80)
                print("BANK STATEMENT PROVIDER JSON DECODE ERROR")
                print("URL:", provider_json_url)
                print("Error:", error)
                print("=" * 80)

            except ValueError as error:
                print("=" * 80)
                print("BANK STATEMENT PROVIDER JSON PARSE ERROR")
                print("URL:", provider_json_url)
                print("Error:", error)
                print("=" * 80)

            except Exception as error:
                print("=" * 80)
                print("BANK STATEMENT PROVIDER JSON ERROR")
                print("URL:", provider_json_url)
                print("Error:", error)
                print("=" * 80)

        elif report_data is None:
            print("=" * 80)
            print("BANK STATEMENT PROVIDER JSON URL IS EMPTY")
            print("REPORT DATA COULD NOT BE LOADED")
            print("=" * 80)

        ###########################################################
        # STEP 3
        # ATTACH REPORT DATA
        ###########################################################

        result["report_data"] = report_data

        ###########################################################
        # DEBUG REPORT DATA
        ###########################################################

        print("=" * 80)
        print("BANK STATEMENT REPORT DATA ATTACHED")
        print("REPORT DATA EXISTS:", report_data is not None)

        if isinstance(report_data, dict):
            print(
                "REPORT DATA KEYS:",
                list(report_data.keys()),
            )

        elif isinstance(report_data, list):
            print("REPORT DATA TYPE: LIST")
            print(
                "REPORT DATA LENGTH:",
                len(report_data),
            )

        else:
            print(
                "REPORT DATA TYPE:",
                type(report_data).__name__,
            )

        print("=" * 80)

        ###########################################################
        # RETURN
        ###########################################################

        return result
