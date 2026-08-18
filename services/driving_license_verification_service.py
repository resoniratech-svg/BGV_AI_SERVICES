# from difflib import SequenceMatcher

# from repositories.document_repository import DocumentRepository

# from repositories.driving_license_repository import DrivingLicenseRepository

# from services.ocr.driving_license_ocr_service import DrivingLicenseOCRService

# from services.ongrid.dl_service import OnGridDrivingLicenseService


# class DrivingLicenseVerificationService:
#     @staticmethod
#     def normalize(value):

#         if not value:
#             return ""

#         return (
#             str(value)
#             .upper()
#             .replace(".", "")
#             .replace(",", "")
#             .replace(" ", "")
#             .strip()
#         )

#     @staticmethod
#     def compare_address(address1, address2):

#         if not address1 or not address2:
#             return "MISMATCH"

#         similarity = SequenceMatcher(
#             None, str(address1).upper(), str(address2).upper()
#         ).ratio()

#         return "MATCH" if similarity >= 0.85 else "MISMATCH"

#     @staticmethod
#     def verify_driving_license(
#         candidate_id, bgv_id, front_document_id, back_document_id
#     ):

#         ###################################################
#         # GET FRONT DOCUMENT
#         ###################################################

#         front_document = DocumentRepository.get_uploaded_document(front_document_id)

#         if not front_document:
#             raise Exception("Driving license front image not found")

#         ###################################################
#         # GET BACK DOCUMENT
#         ###################################################

#         back_document = DocumentRepository.get_uploaded_document(back_document_id)

#         if not back_document:
#             raise Exception("Driving license back image not found")

#         ###################################################
#         # FILE PATHS
#         ###################################################

#         front_image_path = front_document.get("file_path")

#         if not front_image_path:
#             raise Exception("Front driving license file path missing")

#         back_image_path = back_document.get("file_path")

#         if not back_image_path:
#             raise Exception("Back driving license file path missing")

#         ###################################################
#         # OCR
#         ###################################################

#         ocr = DrivingLicenseOCRService.process_ocr(
#             candidate_id=candidate_id,
#             bgv_id=bgv_id,
#             front_image_path=front_image_path,
#             back_image_path=back_image_path,
#         )

#         #         ocr = DrivingLicenseRepository.get_driving_license_ocr_by_candidate(
#         #     candidate_id
#         # )

#         #         if not ocr:
#         #             raise Exception("Driving License OCR record not found")

#         if not ocr:
#             raise Exception("Driving License OCR failed")

#         ###################################################
#         # VALIDATIONS
#         ###################################################

#         if not ocr.get("license_number"):
#             raise Exception("Driving License number not extracted")

#         if not ocr.get("full_name"):
#             raise Exception("Name not extracted")

#         if not ocr.get("date_of_birth"):
#             raise Exception("Date of Birth not extracted")

#         if not ocr.get("address"):
#             raise Exception("Address not extracted")

#         ###################################################
#         # GRIDLINES FETCH
#         ###################################################

#         dob = ocr["date_of_birth"]

#         if dob:
#             dob = dob.strftime("%Y-%m-%d")

#         fetch = OnGridDrivingLicenseService.verify_driving_license(
#             license_number=ocr["license_number"], date_of_birth=dob
#         )

#         dl_data = fetch.get("data", {}).get("driving_license_data", {})

#         if not dl_data:
#             raise Exception("Driving License verification data not found")

#         ###################################################
#         # COMPARISON
#         ###################################################

#         dl_match = (
#             "MATCH"
#             if DrivingLicenseVerificationService.normalize(ocr["license_number"])
#             == DrivingLicenseVerificationService.normalize(dl_data.get("document_id"))
#             else "MISMATCH"
#         )

#         name_match = (
#             "MATCH"
#             if DrivingLicenseVerificationService.normalize(ocr["full_name"])
#             == DrivingLicenseVerificationService.normalize(dl_data.get("name"))
#             else "MISMATCH"
#         )

#         dob_match = (
#             "MATCH"
#             if str(ocr["date_of_birth"]) == str(dl_data.get("date_of_birth"))
#             else "MISMATCH"
#         )

#         address_match = DrivingLicenseVerificationService.compare_address(
#             ocr["address"], dl_data.get("address")
#         )

#         ###################################################
#         # FINAL STATUS
#         ###################################################

#         verification_status = (
#             "APPROVED"
#             if (
#                 dl_match == "MATCH"
#                 and name_match == "MATCH"
#                 and dob_match == "MATCH"
#                 and address_match == "MATCH"
#             )
#             else "FAILED"
#         )

#         ###################################################
#         # SAVE RESULT
#         ###################################################

#         verification_result_id = (
#             DrivingLicenseRepository.save_driving_license_verification_result(
#                 candidate_id=candidate_id,
#                 bgv_id=bgv_id,
#                 driving_license_ocr_result_id=ocr["ocr_result_id"],
#                 verification_status=verification_status,
#                 license_number=dl_data.get("document_id"),
#                 full_name=dl_data.get("name"),
#                 dependent_name=dl_data.get("dependent_name"),
#                 date_of_birth=dl_data.get("date_of_birth"),
#                 issue_date=dl_data.get("issued_date"),
#                 expiry_date=dl_data.get("valid_till"),
#                 address=dl_data.get("address"),
#                 dl_number_match_status=dl_match,
#                 name_match_status=name_match,
#                 dob_match_status=dob_match,
#                 address_match_status=address_match,
#                 provider_name="GRIDLINES",
#                 api_reference_id=fetch.get("request_id"),
#                 raw_response=fetch,
#             )
#         )

#         ###################################################
#         # RETURN
#         ###################################################

#         return {
#             "success": True,
#             "verification_result_id": verification_result_id,
#             "verification_status": verification_status,
#             "comparison": {
#                 "driving_license_number": dl_match,
#                 "name": name_match,
#                 "date_of_birth": dob_match,
#                 "address": address_match,
#             },
#             "provider": "GRIDLINES",
#         }

from difflib import SequenceMatcher

from repositories.document_repository import DocumentRepository
from repositories.driving_license_repository import DrivingLicenseRepository

from services.ocr.driving_license_ocr_service import DrivingLicenseOCRService
from services.ongrid.dl_service import OnGridDrivingLicenseService


class DrivingLicenseVerificationService:
    # =====================================================
    # NORMALIZE VALUE
    # =====================================================

    @staticmethod
    def normalize(value):

        if value is None:
            return ""

        return (
            str(value)
            .upper()
            .replace(".", "")
            .replace(",", "")
            .replace(" ", "")
            .replace("-", "")
            .strip()
        )

    # =====================================================

    # COMPARE NAME
    # =====================================================

    @staticmethod
    def compare_name(name1, name2):

        if not name1 or not name2:
            return "MISMATCH"

        import re

        def get_name_tokens(value):
            value = str(value).upper()

            # Replace punctuation with spaces
            value = re.sub(r"[^A-Z0-9]+", " ", value)

            # Split into words
            return {token for token in value.split() if token}

        tokens1 = get_name_tokens(name1)
        tokens2 = get_name_tokens(name2)

        if not tokens1 or not tokens2:
            return "MISMATCH"

        print("=" * 80)
        print("NAME COMPARISON")
        print("OCR NAME:", name1)
        print("GRIDLINES NAME:", name2)
        print("OCR NAME TOKENS:", tokens1)
        print("GRIDLINES NAME TOKENS:", tokens2)
        print("=" * 80)

        # Exact token match regardless of order
        if tokens1 == tokens2:
            return "MATCH"

        # Calculate common-token ratio
        common_tokens = tokens1.intersection(tokens2)

        smaller_token_count = min(
            len(tokens1),
            len(tokens2),
        )

        if smaller_token_count == 0:
            return "MISMATCH"

        match_ratio = len(common_tokens) / smaller_token_count

        print("COMMON NAME TOKENS:", common_tokens)
        print("NAME MATCH RATIO:", match_ratio)

        return "MATCH" if match_ratio >= 0.80 else "MISMATCH"

    # =====================================================
    # NORMALIZE DATE
    # =====================================================

    @staticmethod
    def normalize_date(value):

        if value is None:
            return ""

        if hasattr(value, "strftime"):
            return value.strftime("%Y-%m-%d")

        value = str(value).strip()

        if not value:
            return ""

        from datetime import datetime

        for date_format in (
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%Y/%m/%d",
            "%d.%m.%Y",
            "%d %m %Y",
            "%d %b %Y",
            "%d %B %Y",
            "%b %d %Y",
            "%B %d %Y",
        ):
            try:
                parsed = datetime.strptime(
                    value,
                    date_format,
                )

                return parsed.strftime("%Y-%m-%d")

            except ValueError:
                continue

        return value

    # =====================================================
    # COMPARE ADDRESS
    # =====================================================

    # =====================================================
    # NORMALIZE ADDRESS
    # =====================================================

    @staticmethod
    def normalize_address(value):

        if not value:
            return ""

        value = str(value).upper()

        # Replace common separators with spaces
        for char in [",", ".", "-", "/", "\\"]:
            value = value.replace(char, " ")

        # Remove common address noise
        words = value.split()

        normalized_words = []

        for word in words:
            if word in {
                "INDIA",
                "IND",
            }:
                continue

            normalized_words.append(word)

        return " ".join(sorted(normalized_words))

    # =====================================================
    # COMPARE ADDRESS
    # =====================================================

    @staticmethod
    def compare_address(address1, address2):

        if not address1 or not address2:
            return "MISMATCH"

        normalized_address1 = DrivingLicenseVerificationService.normalize_address(
            address1
        )

        normalized_address2 = DrivingLicenseVerificationService.normalize_address(
            address2
        )

        if not normalized_address1 or not normalized_address2:
            return "MISMATCH"

        # -------------------------------------------------
        # EXACT MATCH AFTER NORMALIZATION
        # -------------------------------------------------

        if normalized_address1 == normalized_address2:
            return "MATCH"

        # -------------------------------------------------
        # TOKEN-BASED COMPARISON
        # -------------------------------------------------

        words1 = set(normalized_address1.split())
        words2 = set(normalized_address2.split())

        if not words1 or not words2:
            return "MISMATCH"

        common_words = words1.intersection(words2)

        # Compare against the smaller address.
        #
        # This allows OCR to contain additional information
        # such as:
        #
        # GANGADHARA
        # PINCODE
        # DISTRICT
        #
        # while Gridlines may return a shorter address.

        smaller_word_count = min(
            len(words1),
            len(words2),
        )

        token_match_ratio = len(common_words) / smaller_word_count

        print("=" * 80)
        print("ADDRESS COMPARISON")
        print("OCR NORMALIZED ADDRESS:", normalized_address1)
        print("GRIDLINES NORMALIZED ADDRESS:", normalized_address2)
        print("COMMON WORDS:", common_words)
        print("TOKEN MATCH RATIO:", token_match_ratio)
        print("=" * 80)

        if token_match_ratio >= 0.80:
            return "MATCH"

        # -------------------------------------------------
        # FALLBACK SIMILARITY
        # -------------------------------------------------

        similarity = SequenceMatcher(
            None,
            normalized_address1,
            normalized_address2,
        ).ratio()

        print("ADDRESS SEQUENCE SIMILARITY:", similarity)

        return "MATCH" if similarity >= 0.80 else "MISMATCH"

    # =====================================================
    # VERIFY DRIVING LICENSE
    # =====================================================

    @staticmethod
    def verify_driving_license(
        candidate_id,
        bgv_id,
        front_document_id,
        back_document_id,
    ):

        print("=" * 80)
        print("STARTING DRIVING LICENSE VERIFICATION")
        print("=" * 80)

        print(
            "CANDIDATE ID:",
            candidate_id,
        )

        print(
            "BGV ID:",
            bgv_id,
        )

        print(
            "FRONT DOCUMENT ID:",
            front_document_id,
        )

        print(
            "BACK DOCUMENT ID:",
            back_document_id,
        )

        # =================================================
        # GET FRONT DOCUMENT
        # =================================================

        front_document = DocumentRepository.get_uploaded_document(front_document_id)

        if not front_document:
            raise Exception("Driving license front image not found")

        # =================================================
        # GET BACK DOCUMENT
        # =================================================

        back_document = DocumentRepository.get_uploaded_document(back_document_id)

        if not back_document:
            raise Exception("Driving license back image not found")

        # =================================================
        # GET FRONT FILE PATH
        # =================================================

        front_image_path = front_document.get("file_path")

        if not front_image_path:
            raise Exception("Front driving license file path missing")

        # =================================================
        # GET BACK FILE PATH
        # =================================================

        back_image_path = back_document.get("file_path")

        if not back_image_path:
            raise Exception("Back driving license file path missing")

        print(
            "FRONT IMAGE:",
            front_image_path,
        )

        print(
            "BACK IMAGE:",
            back_image_path,
        )

        # =================================================
        # STEP 1
        # DRIVING LICENSE OCR
        # =================================================

        print("=" * 80)
        print("STEP 1: STARTING DRIVING LICENSE OCR")
        print("=" * 80)

        ocr = DrivingLicenseOCRService.process_ocr(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            front_image_path=front_image_path,
            back_image_path=back_image_path,
        )

        if not ocr:
            raise Exception("Driving License OCR failed")

        print("=" * 80)
        print("DRIVING LICENSE OCR RESULT")
        print("=" * 80)

        print(ocr)

        print("=" * 80)

        # =================================================
        # VALIDATE OCR DATA
        # =================================================

        license_number = ocr.get("license_number")

        full_name = ocr.get("full_name")

        date_of_birth = ocr.get("date_of_birth")

        address = ocr.get("address")

        if not license_number:
            raise Exception("Driving License number not extracted from OCR")

        if not full_name:
            raise Exception("Driving License name not extracted from OCR")

        if not date_of_birth:
            raise Exception("Driving License date of birth not extracted from OCR")

        if not address:
            raise Exception("Driving License address not extracted from OCR")

        # =================================================
        # NORMALIZE OCR DOB
        # =================================================

        dob = DrivingLicenseVerificationService.normalize_date(date_of_birth)

        print(
            "OCR LICENSE NUMBER:",
            license_number,
        )

        print(
            "OCR NAME:",
            full_name,
        )

        print(
            "OCR DOB:",
            dob,
        )

        print(
            "OCR ADDRESS:",
            address,
        )

        # =================================================
        # STEP 2
        # GRIDLINES FETCH
        # =================================================

        print("=" * 80)
        print("STEP 2: CALLING GRIDLINES DRIVING LICENSE FETCH")
        print("=" * 80)

        fetch = OnGridDrivingLicenseService.verify_driving_license(
            license_number=license_number,
            date_of_birth=dob,
        )

        if not fetch:
            raise Exception(
                "No response received from Gridlines Driving License service"
            )

        # =================================================
        # EXTRACT GRIDLINES DATA
        # =================================================

        data = fetch.get("data", {})

        dl_data = data.get("driving_license_data", {})

        if not dl_data:
            raise Exception(
                "Driving License verification data not found in Gridlines response"
            )

        print("=" * 80)
        print("GRIDLINES DRIVING LICENSE DATA")
        print("=" * 80)

        print(dl_data)

        print("=" * 80)

        # =================================================
        # PROVIDER BASIC VALUES
        # =================================================

        provider_license_number = dl_data.get("document_id")

        provider_name = dl_data.get("name")

        provider_dob = dl_data.get("date_of_birth")

        provider_address = dl_data.get("address")

        provider_dependent_name = dl_data.get("dependent_name")

        # =================================================
        # PROVIDER VALIDITY
        # =================================================

        validity = dl_data.get("validity", {})

        non_transport = validity.get("non_transport", {})

        transport = validity.get("transport", {})

        # =================================================
        # ISSUE / EXPIRY DATE
        #
        # Prefer NON-TRANSPORT because it is always
        # relevant for a normal Driving License.
        #
        # Fallback to transport if required.
        # =================================================

        provider_issue_date = non_transport.get("issue_date") or transport.get(
            "issue_date"
        )

        provider_expiry_date = non_transport.get("expiry_date") or transport.get(
            "expiry_date"
        )

        # =================================================
        # RTO DETAILS
        # =================================================

        rto_details = dl_data.get("rto_details", {})

        provider_state = rto_details.get("state")

        provider_authority = rto_details.get("authority")

        # =================================================
        # PLACE OF ISSUE
        #
        # Gridlines does not return a direct
        # "place_of_issue" field.
        #
        # Therefore use RTO authority.
        # =================================================

        provider_place_of_issue = provider_authority or provider_state

        # =================================================
        # NORMALIZE PROVIDER DOB
        # =================================================

        provider_dob = DrivingLicenseVerificationService.normalize_date(provider_dob)

        # =================================================
        # NORMALIZE PROVIDER DATES
        # =================================================

        provider_issue_date = DrivingLicenseVerificationService.normalize_date(
            provider_issue_date
        )

        provider_expiry_date = DrivingLicenseVerificationService.normalize_date(
            provider_expiry_date
        )

        # =================================================
        # DEBUG PROVIDER VALUES
        # =================================================

        print("=" * 80)
        print("GRIDLINES NORMALIZED VALUES")
        print("=" * 80)

        print(
            "LICENSE NUMBER:",
            provider_license_number,
        )

        print(
            "NAME:",
            provider_name,
        )

        print(
            "DOB:",
            provider_dob,
        )

        print(
            "ADDRESS:",
            provider_address,
        )

        print(
            "ISSUE DATE:",
            provider_issue_date,
        )

        print(
            "EXPIRY DATE:",
            provider_expiry_date,
        )

        print(
            "STATE:",
            provider_state,
        )

        print(
            "RTO AUTHORITY:",
            provider_authority,
        )

        print(
            "PLACE OF ISSUE:",
            provider_place_of_issue,
        )

        print("=" * 80)

        # =================================================
        # STEP 3
        # COMPARE OCR VS GRIDLINES
        #
        # IMPORTANT:
        #
        # Gridlines only provides the authoritative
        # verification data.
        #
        # The comparison is performed by OUR CODE.
        # =================================================

        # =================================================
        # LICENSE NUMBER
        # =================================================

        dl_match = (
            "MATCH"
            if DrivingLicenseVerificationService.normalize(license_number)
            == DrivingLicenseVerificationService.normalize(provider_license_number)
            else "MISMATCH"
        )

        # =================================================
        # NAME
        # =================================================

        name_match = DrivingLicenseVerificationService.compare_name(
            full_name,
            provider_name,
        )

        # =================================================
        # DATE OF BIRTH
        # =================================================

        dob_match = "MATCH" if dob == provider_dob else "MISMATCH"

        # =================================================
        # ADDRESS
        # =================================================

        address_match = DrivingLicenseVerificationService.compare_address(
            address,
            provider_address,
        )

        # =================================================
        # COMPARISON RESULT
        # =================================================

        print("=" * 80)
        print("DRIVING LICENSE OCR VS GRIDLINES COMPARISON")
        print("=" * 80)

        print(
            "LICENSE NUMBER :",
            dl_match,
        )

        print(
            "NAME           :",
            name_match,
        )

        print(
            "DATE OF BIRTH  :",
            dob_match,
        )

        print(
            "ADDRESS        :",
            address_match,
        )

        print("=" * 80)

        # =================================================
        # FINAL VERIFICATION
        # =================================================

        all_match = (
            dl_match == "MATCH"
            and name_match == "MATCH"
            and dob_match == "MATCH"
            and address_match == "MATCH"
        )

        verification_status = "APPROVED" if all_match else "FAILED"

        print(
            "FINAL VERIFICATION STATUS:",
            verification_status,
        )

        # =================================================
        # SAVE VERIFICATION RESULT
        # =================================================

        verification_result_id = (
            DrivingLicenseRepository.save_driving_license_verification_result(
                candidate_id=candidate_id,
                bgv_id=bgv_id,
                driving_license_ocr_result_id=(ocr["ocr_result_id"]),
                verification_status=(verification_status),
                license_number=(provider_license_number),
                full_name=(provider_name),
                dependent_name=(provider_dependent_name),
                date_of_birth=(provider_dob),
                issue_date=(provider_issue_date),
                expiry_date=(provider_expiry_date),
                place_of_issue=(provider_place_of_issue),
                address=(provider_address),
                dl_number_match_status=(dl_match),
                name_match_status=(name_match),
                dob_match_status=(dob_match),
                address_match_status=(address_match),
                provider_name="GRIDLINES",
                api_reference_id=(fetch.get("request_id")),
                raw_response=fetch,
            )
        )

        # =================================================
        # FINAL RESPONSE
        # =================================================

        return {
            "success": True,
            "verification_result_id": (verification_result_id),
            "verification_status": (verification_status),
            "comparison": {
                "driving_license_number": (dl_match),
                "name": (name_match),
                "date_of_birth": (dob_match),
                "address": (address_match),
            },
            "ocr_data": {
                "license_number": (license_number),
                "full_name": (full_name),
                "date_of_birth": (dob),
                "address": (address),
            },
            "provider_data": {
                "license_number": (provider_license_number),
                "full_name": (provider_name),
                "date_of_birth": (provider_dob),
                "dependent_name": (provider_dependent_name),
                "address": (provider_address),
                "issue_date": (provider_issue_date),
                "expiry_date": (provider_expiry_date),
                "place_of_issue": (provider_place_of_issue),
                "rto_state": (provider_state),
                "rto_authority": (provider_authority),
            },
            "provider": "GRIDLINES",
        }
