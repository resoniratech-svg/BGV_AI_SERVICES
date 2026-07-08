import json

from services.ocr.aadhaar_ocr_service import (
    AadhaarOCRService
)

from repositories.aadhaar_repository import (
    AadhaarRepository
)


class AadhaarVerificationService:


    @staticmethod
    def verify_aadhaar(

        candidate_id,
        bgv_id,
        document_id

    ):

        # ==========================================
        # OCR EXTRACTION
        # ==========================================

        ocr_data = (

            AadhaarOCRService
            .extract_aadhaar_data(

                candidate_id=
                candidate_id,

                bgv_id=
                bgv_id,

                document_id=
                document_id

            )

        )

        full_name = (

            ocr_data.get(
                "full_name"
            )

        )

        date_of_birth = (

            ocr_data.get(
                "date_of_birth"
            )

        )

        gender = (

            ocr_data.get(

                 "gender"

    )

)

        if not full_name:

            raise Exception(

                "Name not extracted from Aadhaar"

            )

        if not date_of_birth:

            raise Exception(

                "Date of birth not extracted from Aadhaar"

            )
        
        if not gender:

            raise Exception(

                "Gender not extracted from Aadhaar"

            )

        # ==========================================
        # SAVE OCR RESULT
        # ==========================================

        aadhaar_ocr_result_id = (

            AadhaarRepository
            .save_aadhaar_ocr_result(

                candidate_id=
                candidate_id,

                bgv_id=
                bgv_id,

                document_id=
                document_id,

                full_name=
                full_name,

                date_of_birth=
                date_of_birth,


                gender=
                gender,

                provider_name=
                "GRIDLINES",

                api_reference_id=

                ocr_data.get(

                    "request_id"

                ),

                raw_response=

                json.dumps(

                    ocr_data

                )

            )

        )

        
        # ==========================================
        # GET SESSION
        # ==========================================

        session = (

            AadhaarRepository
            .get_aadhaar_session(

                candidate_id

            )

        )

        if not session:

            raise Exception(

                "Aadhaar consent session not found"

            )

        if (

            session[

                "session_status"

            ]

            !=

            "SUCCESS"

        ):

            raise Exception(

                "Candidate has not completed Aadhaar consent"

            )

        try:

            response = json.loads(

                session["raw_response"]

            )

        except Exception:

            raise Exception(

                "Invalid Aadhaar session response"

            )

        # ==========================================
        # EXTRACT UIDAI DATA
        # ==========================================

        ovse_data = (

            response.get(

                "data",

                {}

            ).get(

                "ovse_data",

                {}

            )

        )

        address = (

            ovse_data.get(

                "address"

            )

            or

            ""

)
         
        resident_image = (

            ovse_data.get(

                "resident_image"

            )

            or

            ""

) 
        if not resident_image:

            raise Exception(

                "Resident image not received from UIDAI"

            )


        resident_name = (

            ovse_data.get(

                "resident_name"

            )

            or

            ""

        )
        if not resident_name:

            raise Exception(

                "Resident name not received from UIDAI"

            )

        uidai_dob = (

            ovse_data.get(

                "dob"

            )

            or

            ""

        )

        if not uidai_dob:

            raise Exception(

                "Date of birth not received from UIDAI"

            )

        uidai_gender = (

            ovse_data.get(

                "gender"

            )

            or

            ""

        )
        if not uidai_gender:

            raise Exception(

                "Gender not received from UIDAI"

            )

        # ==========================================
        # NAME MATCH
        # ==========================================
        ocr_name = full_name.strip().upper()
        uidai_name = resident_name.strip().upper()

        name_match_status = (
            "MATCH"
            if ocr_name == uidai_name
            else "NOT_MATCH"
        )

        # ==========================================
        # DOB MATCH
        # ==========================================
        ocr_dob = date_of_birth.strip()
        uidai_dob_clean = uidai_dob.strip()

        dob_match_status = (
            "MATCH"
            if ocr_dob == uidai_dob_clean
            else "NOT_MATCH"
        )

        # ==========================================
        # GENDER MATCH
        # ==========================================
        ocr_gender = gender.strip().upper()
        uidai_gender_clean = uidai_gender.strip().upper()

        gender_match_status = (
            "MATCH"
            if ocr_gender == uidai_gender_clean
            else "NOT_MATCH"
        )

        # ==========================================
        # FINAL STATUS
        # ==========================================

        verification_status = (

            "VERIFIED"

            if (

                name_match_status

                ==

                "MATCH"

                and

                dob_match_status

                ==

                "MATCH"

                and

                gender_match_status

                ==

                "MATCH"

            )

            else

            "FAILED"

)
        # ==========================================
        # SAVE RESULT
        # ==========================================

        AadhaarRepository.save_aadhaar_verification_result(

            candidate_id=
            candidate_id,

            bgv_id=
            bgv_id,

            aadhaar_ocr_result_id=
            aadhaar_ocr_result_id,

            verification_status=
            verification_status,

            resident_name=
            resident_name,

            date_of_birth=
            uidai_dob,
           
            resident_image=
            resident_image,

            address=
            address,

            name_match_status=
            name_match_status,

            dob_match_status=
            dob_match_status,

            gender_match_status=
            gender_match_status,

            provider_name=
            "GRIDLINES",

            api_reference_id=

            response.get(

                "request_id"

            ),

            raw_response=

            json.dumps(

                response

            )

        )

        return {

            "success":

            verification_status

            ==

            "VERIFIED",


            "verification_status":

            verification_status,


            "name_match_status":

            name_match_status,


            "dob_match_status":

            dob_match_status,
           

           "gender_match_status":

            gender_match_status,

            "provider":

            "GRIDLINES",


            "response":

            response

        }
