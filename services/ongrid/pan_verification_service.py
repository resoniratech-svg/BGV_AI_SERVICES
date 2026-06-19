from services.ocr.pan_ocr_service import (
    PanOCRService
)

from services.ongrid.pan_service import (
    OnGridPANService
)

from repositories.pan_repository import (
    PanRepository
)

import json


class OnGridPANVerificationService:

    @staticmethod
    def verify_pan(
        candidate_id,
        bgv_id,
        document_id
    ):

        pan_data = (

            PanOCRService
            .extract_pan_data(

                candidate_id=
                candidate_id,

                bgv_id=
                bgv_id,

                document_id=
                document_id

            )

        )


        if not pan_data:

            raise Exception(
                "PAN OCR failed"
            )

        if not pan_data.get(
            "pan_number"
        ):

            raise Exception(
                "PAN number not extracted"
            )

        if not pan_data.get(
            "full_name"
        ):

            raise Exception(
                "PAN holder name not extracted"
            )

        if not pan_data.get(
            "date_of_birth"
        ):

            raise Exception(
                "Date of birth not extracted"
            )

        dob = pan_data.get(
            "date_of_birth"
        )

        # =====================================
        # SAVE OCR RESULT
        # =====================================

        pan_ocr_result_id = (

            PanRepository
            .save_pan_ocr_result(

                candidate_id=
                candidate_id,

                bgv_id=
                bgv_id,

                document_id=
                document_id,

                pan_number=
                pan_data.get(
                    "pan_number"
                ),

                full_name=
                pan_data.get(
                    "full_name"
                ),

                father_name=
                pan_data.get(
                    "father_name"
                ),

                date_of_birth=
                dob,

                provider_name=
                "GRIDLINES",

                api_reference_id=
                pan_data.get(
                    "request_id"
                ),

                raw_response=
                json.dumps(
                    pan_data.get(
                        "raw_response"
                    )
                )

            )

        )

        # =====================================
        # CALL PAN VERIFY
        # =====================================

        return (

            OnGridPANService
            .verify_pan(

                candidate_id=
                candidate_id,

                bgv_id=
                bgv_id,

                pan_ocr_result_id=
                pan_ocr_result_id,

                pan_number=
                pan_data.get(
                    "pan_number"
                ),

                full_name=
                pan_data.get(
                    "full_name"
                ),

                date_of_birth=
                dob

            )

        )