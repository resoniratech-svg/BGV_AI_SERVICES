from difflib import SequenceMatcher

from repositories.document_repository import (
    DocumentRepository
)

from repositories.driving_license_repository import (
    DrivingLicenseRepository
)

from services.ocr.driving_license_ocr_service import (
    DrivingLicenseOCRService
)

from services.ongrid.dl_service import (
    OnGridDrivingLicenseService
)


class DrivingLicenseVerificationService:

    @staticmethod
    def normalize(value):

        if not value:
            return ""

        return (
            str(value)
            .upper()
            .replace(".", "")
            .replace(",", "")
            .replace(" ", "")
            .strip()
        )

    @staticmethod
    def compare_address(

            address1,
            address2

    ):

        if not address1 or not address2:

            return "MISMATCH"

        similarity = SequenceMatcher(

            None,

            str(address1).upper(),

            str(address2).upper()

        ).ratio()

        return (

            "MATCH"

            if similarity >= 0.85

            else "MISMATCH"

        )

    @staticmethod
    def verify_driving_license(

            candidate_id,
            bgv_id,
            front_document_id,
            back_document_id

    ):

        ###################################################
        # GET FRONT DOCUMENT
        ###################################################

        front_document = (

            DocumentRepository
            .get_uploaded_document(
                front_document_id
            )

        )

        if not front_document:

            raise Exception(
                "Driving license front image not found"
            )

        ###################################################
        # GET BACK DOCUMENT
        ###################################################

        back_document = (

            DocumentRepository
            .get_uploaded_document(
                back_document_id
            )

        )

        if not back_document:

            raise Exception(
                "Driving license back image not found"
            )

        ###################################################
        # FILE PATHS
        ###################################################

        front_image_path = front_document.get(
            "file_path"
        )

        if not front_image_path:

            raise Exception(
                "Front driving license file path missing"
            )

        back_image_path = back_document.get(
            "file_path"
        )

        if not back_image_path:

            raise Exception(
                "Back driving license file path missing"
            )

        ###################################################
        # OCR
        ###################################################

        ocr = (

            DrivingLicenseOCRService
            .process_ocr(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                front_image_path=front_image_path,

                back_image_path=back_image_path

            )

        )

        if not ocr:

            raise Exception(
                "Driving License OCR failed"
            )

        ###################################################
        # VALIDATIONS
        ###################################################

        if not ocr.get("license_number"):

            raise Exception(
                "Driving License number not extracted"
            )

        if not ocr.get("full_name"):

            raise Exception(
                "Name not extracted"
            )

        if not ocr.get("date_of_birth"):

            raise Exception(
                "Date of Birth not extracted"
            )

        if not ocr.get("address"):

            raise Exception(
                "Address not extracted"
            )

        ###################################################
        # GRIDLINES FETCH
        ###################################################

        fetch = (

            OnGridDrivingLicenseService
            .verify_driving_license(

                license_number=
                ocr["license_number"],

                date_of_birth=
                ocr["date_of_birth"]

            )

        )

        dl_data = (

            fetch.get(
                "driving_license_data",
                {}
            )

        )

        if not dl_data:

            raise Exception(
                "Driving License verification data not found"
            )

        ###################################################
        # COMPARISON
        ###################################################

        dl_match = (

            "MATCH"

            if

            DrivingLicenseVerificationService.normalize(

                ocr["license_number"]

            )

            ==

            DrivingLicenseVerificationService.normalize(

                dl_data.get(
                    "document_id"
                )

            )

            else

            "MISMATCH"

        )

        name_match = (

            "MATCH"

            if

            DrivingLicenseVerificationService.normalize(

                ocr["full_name"]

            )

            ==

            DrivingLicenseVerificationService.normalize(

                dl_data.get(
                    "name"
                )

            )

            else

            "MISMATCH"

        )

        dob_match = (

            "MATCH"

            if

            str(
                ocr["date_of_birth"]
            )

            ==

            str(
                dl_data.get(
                    "date_of_birth"
                )
            )

            else

            "MISMATCH"

        )

        address_match = (

            DrivingLicenseVerificationService
            .compare_address(

                ocr["address"],

                dl_data.get(
                    "address"
                )

            )

        )

        ###################################################
        # FINAL STATUS
        ###################################################

        verification_status = (

            "APPROVED"

            if (

                dl_match == "MATCH"

                and

                name_match == "MATCH"

                and

                dob_match == "MATCH"

                and

                address_match == "MATCH"

            )

            else

            "FAILED"

        )

        ###################################################
        # SAVE RESULT
        ###################################################

        verification_result_id = (

            DrivingLicenseRepository
            .save_driving_license_verification_result(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                driving_license_ocr_result_id=
                ocr["ocr_result_id"],

                verification_status=
                verification_status,

                license_number=
                dl_data.get(
                    "document_id"
                ),

                full_name=
                dl_data.get(
                    "name"
                ),

                dependent_name=
                dl_data.get(
                    "dependent_name"
                ),

                date_of_birth=
                dl_data.get(
                    "date_of_birth"
                ),

                issue_date=
                dl_data.get(
                    "issued_date"
                ),

                expiry_date=
                dl_data.get(
                    "valid_till"
                ),

                address=
                dl_data.get(
                    "address"
                ),

                dl_number_match_status=
                dl_match,

                name_match_status=
                name_match,

                dob_match_status=
                dob_match,

                address_match_status=
                address_match,

                provider_name="GRIDLINES",

                api_reference_id=
                fetch.get(
                    "request_id"
                ),

                raw_response=
                fetch

            )

        )

        ###################################################
        # RETURN
        ###################################################

        return {

            "success": True,

            "verification_result_id":
            verification_result_id,

            "verification_status":
            verification_status,

            "comparison": {

                "driving_license_number":
                dl_match,

                "name":
                name_match,

                "date_of_birth":
                dob_match,

                "address":
                address_match

            },

            "provider":
            "GRIDLINES"

        }