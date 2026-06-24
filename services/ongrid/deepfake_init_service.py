import os

from repositories.document_repository import (
    DocumentRepository
)

from services.ongrid.ongrid_client import (
    OnGridClient
)


class DeepfakeInitService:


    @staticmethod
    def initialize(

        candidate_id,
        bgv_id,
        document_id

    ):


        document = (

            DocumentRepository
            .get_uploaded_document(

                document_id

            )

        )


        if not document:

            raise Exception(

                "Profile image not found"

            )


        file_path = os.path.abspath(

            document["file_path"]

        )


        ###########################################
        # FILE EXISTS
        ###########################################

        if not os.path.exists(

                file_path

        ):

            raise Exception(

                f"File not found : {file_path}"

            )


        ###########################################
        # FILE FORMAT
        ###########################################

        allowed_extensions = (

            ".jpg",
            ".jpeg",
            ".png",
            ".gif"

        )


        extension = (

            os.path.splitext(

                file_path

            )[1]

            .lower()

        )


        if extension not in allowed_extensions:


            raise Exception(

                "Unsupported image format. "

                "Allowed formats are "

                "jpg, jpeg, png and gif"

            )


        ###########################################
        # FILE SIZE
        ###########################################

        size_mb = (

            os.path.getsize(

                file_path

            )

            /

            1024

            /

            1024

        )


        if size_mb > 10:


            raise Exception(

                f"Image size "

                f"{round(size_mb,2)} MB "

                f"exceeds "

                f"10 MB limit"

            )


        ###########################################
        # REQUEST DATA
        ###########################################

        data = {

            "consent":

            "Y"

        }


        with open(

                file_path,

                "rb"

        ) as f:


            files = {

                "file":

                f

            }


            response = (

                OnGridClient
                .post_multipart(

                    "/profile-api/deepfake/image/init",

                    files,

                    data

                )

            )


        print("=" * 80)
        print("DEEPFAKE INIT RESPONSE")
        print(response)
        print("=" * 80)


        ###########################################
        # RESPONSE VALIDATION
        ###########################################

        if not response:


            raise Exception(

                "Empty Deepfake response"

            )


        if response.get(

                "status"

        ) != 200:


            raise Exception(

                response

            )


        transaction_id = (

            response.get(

                "transaction_id"

            )

        )


        if not transaction_id:


            raise Exception(

                "Transaction ID not received"

            )


        return {


            "transaction_id":

            transaction_id,


            "request_id":

            response.get(

                "request_id"

            ),


            "response":

            response

        }