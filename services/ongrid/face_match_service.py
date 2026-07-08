import os
import json
import base64
import tempfile


from repositories.aadhaar_repository import (
    AadhaarRepository
)

from repositories.document_repository import (
    DocumentRepository
)

from repositories.face_match_repository import (
    FaceMatchRepository
)


from services.ongrid.ongrid_client import (
    OnGridClient
)



class FaceMatchService:



    @staticmethod
    def verify_face(

            candidate_id,

            bgv_id,

            document_id

    ):


        ########################################
        # Aadhaar verification result
        ########################################

        aadhaar = (

            AadhaarRepository

            .get_aadhaar_verification_result(

                candidate_id

            )

        )


        if not aadhaar:

            raise Exception(

                "Aadhaar verification not found"

            )



        resident_image = (

            aadhaar.get(

                "resident_image"

            )

        )


        if not resident_image:

            raise Exception(

                "Resident image not available"

            )



        
        # Candidate uploaded selfie
        

        document = (

            DocumentRepository

            .get_uploaded_document(

                document_id

            )

        )


        if not document:

            raise Exception(

                "Candidate selfie not found"

            )



        selfie_path = os.path.abspath(

            document["file_path"]

        )


        if not os.path.exists(

                selfie_path

        ):

            raise Exception(

                "Selfie file missing"

            )



        # Convert resident image
       


        image_bytes = (

            base64.b64decode(

                resident_image

            )

        )



        temp_file = tempfile.NamedTemporaryFile(

            suffix=".jpg",

            delete=False

        )


        temp_file.write(

            image_bytes

        )



        temp_file.close()


        aadhaar_path = (

            temp_file.name

        )



        ########################################
        # Gridlines request
        ########################################


        with open(

                aadhaar_path,

                "rb"

        ) as img1, open(

                selfie_path,

                "rb"

        ) as img2:



            files = {


                "file_1":

                img1,


                "file_2":

                img2

            }



            data = {


                "consent":

                "Y"

            }



            response = (

                OnGridClient

                .post_multipart(

                    "/face-api/verify",

                    files,

                    data

                )

            )



        os.remove(

            aadhaar_path

        )



        ########################################
        # Validation
        ########################################


        if not response:

            raise Exception(

                "Face match response empty"

            )



        if response.get(

                "status"

        ) != 200:


            raise Exception(

                response

            )



        code = (

            response.get(

                "data",

                {}

            )

            .get(

                "code"

            )

        )



        confidence = (

            response.get(

                "data",

                {}

            )

            .get(

                "confidence",

                0

            )

        )



        ########################################
        # Threshold
        ########################################


        verification_status = (


            "MATCH"


            if


            confidence >= 0.70


            else


            "NOT_MATCH"

        )



        ########################################
        # Save DB
        ########################################


        FaceMatchRepository.save_result(


            candidate_id=

            candidate_id,


            bgv_id=

            bgv_id,


            document_id=

            document_id,


            confidence_score=

            confidence,


            verification_status=

            verification_status,


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

            "MATCH",


            "verification_status":

            verification_status,


            "confidence":

            confidence,


            "provider":

            "GRIDLINES",


            "response":

            response

        }
