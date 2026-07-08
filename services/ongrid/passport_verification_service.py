from services.didit.passport_service import (
    DiditPassportService
)

from services.ocr.passport_ocr_service import (
    PassportOCRService
)

from services.ongrid.passport_service import (
    OnGridPassportService
)


class PassportVerificationService:

    @staticmethod
    def verify_passport(
        document_id,
        candidate_id,
        bgv_id
    ):

        ###########################################################
        # STEP 1
        # TRY DIDIT FIRST
        ###########################################################

        try:

            return (

                DiditPassportService
                .verify_passport(

                    candidate_id=candidate_id,

                    bgv_id=bgv_id,

                    document_id=document_id

                )

            )

        except Exception as e:

            error = str(e).lower()

            print("=" * 80)
            print("DIDIT FAILED")
            print(error)
            print("=" * 80)

            ###################################################
            # FALLBACK ONLY FOR PROVIDER FAILURES
            ###################################################

            provider_failure = (

                "429" in error
                or
                "500" in error
                or
                "502" in error
                or
                "503" in error
                or
                "504" in error
                or
                "timeout" in error
                or
                "timed out" in error
                or
                "connection" in error
                or
                "connection aborted" in error
                or
                "connection refused" in error
                or
                "max retries exceeded" in error
                or 
                "credits" in error
                or 
                "top up" in error
                or 
                "enough credits" in error
            )

            ###################################################
            # LOCAL ERRORS
            ###################################################

            if not provider_failure:

                raise Exception(str(e))

        ###########################################################
        # STEP 2
        # GRIDLINES OCR
        ###########################################################

        passport_ocr = (

            PassportOCRService
            .extract_passport_data(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                document_id=document_id

            )

        )

        if not passport_ocr:

            raise Exception(
                "Passport OCR failed"
            )

        ###########################################################
        # VALIDATIONS
        ###########################################################

        if not passport_ocr.get("passport_number"):

            raise Exception(
                "Passport number not extracted"
            )

        if not passport_ocr.get("file_number"):

            raise Exception(
                "File number not extracted"
            )

        if not passport_ocr.get("given_name"):

            raise Exception(
                "Given name not extracted"
            )

        if not passport_ocr.get("surname"):

            raise Exception(
                "Surname not extracted"
            )

        if not passport_ocr.get("date_of_birth"):

            raise Exception(
                "Date of birth not extracted"
            )

        ###########################################################
        # STEP 3
        # GRIDLINES PASSPORT FETCH
        ###########################################################

        return (

    OnGridPassportService
    .verify_passport(

        candidate_id=candidate_id,

        bgv_id=bgv_id,

        passport_ocr_result_id=
        passport_ocr["passport_ocr_result_id"],

        passport_number=
        passport_ocr["passport_number"],

        file_number=
        passport_ocr["file_number"],

        given_name=
        passport_ocr["given_name"],

        surname=
        passport_ocr["surname"],

        date_of_birth=
        passport_ocr["date_of_birth"],

        issue_date=
        passport_ocr["issue_date"],

        expiry_date=
        passport_ocr["expiry_date"],

        nationality=
        passport_ocr["nationality"],

        country=
        passport_ocr["country"]

    )

)