from services.ocr.driving_license_ocr_service import (
    DrivingLicenseOCRService
)

from services.ongrid.dl_service import (
    OnGridDrivingLicenseService
)

from datetime import datetime
class OnGridDrivingLicenseVerificationService:

    @staticmethod
    def verify_driving_license(
        candidate_id,
        bgv_id,
        document_id
    ):

        dl_data = (
            DrivingLicenseOCRService
            .extract_driving_license_data(
                document_id
            )
        )
        print("OCR RESULT =", dl_data)
        if not dl_data.get(
            "driving_license_number"
        ):

            raise Exception(
                "Driving license number not extracted"
            )

        if not dl_data.get(
            "date_of_birth"
        ):

            raise Exception(
                "Date of birth not extracted"
            )

        dob = datetime.strptime(
            dl_data["date_of_birth"],
            "%d-%m-%Y"
        ).strftime("%Y-%m-%d")
        return (
            OnGridDrivingLicenseService
            .verify_driving_license(
                candidate_id=candidate_id,
                bgv_id=bgv_id,
                dl_number=dl_data[
                    "driving_license_number"
                ],
                date_of_birth=dob
            )
        )