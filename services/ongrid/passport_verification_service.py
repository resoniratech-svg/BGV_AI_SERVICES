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

        passport_data = (
            PassportOCRService
            .extract_passport_data(
                document_id
            )
        )

        if not passport_data.get(
            "passport_number"
        ):
            raise Exception(
                "Passport number not extracted"
            )

        if not passport_data.get(
            "file_number"
        ):
            raise Exception(
                "File number not extracted"
            )

        if not passport_data.get(
            "surname"
        ):
            raise Exception(
                "Surname not extracted"
            )

        if not passport_data.get(
            "given_name"
        ):
            raise Exception(
                "Given name not extracted"
            )

        if not passport_data.get(
            "date_of_birth"
        ):
            raise Exception(
                "Date of birth not extracted"
            )

        return (
            OnGridPassportService
            .verify_passport(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                passport_number=passport_data[
                    "passport_number"
                ],

                file_number=passport_data[
                    "file_number"
                ],

                surname=passport_data[
                    "surname"
                ],

                given_name=passport_data[
                    "given_name"
                ],

                date_of_birth=passport_data[
                    "date_of_birth"
                ]
            )
        )