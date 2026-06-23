
from services.ongrid.ongrid_client import (
    OnGridClient
)


class DeepfakeStatusService:


    @staticmethod
    def get_status(

        transaction_id

    ):


        headers = {


            "X-Transaction-ID":

            transaction_id

        }


        response = (

            OnGridClient.get(

                "/profile-api/deepfake/image/status",

                headers=headers

            )

        )


        if not response:


            raise Exception(

                "Empty Deepfake response"

            )


        if response.get(

                "status"

        ) != 200:


            raise Exception(

                response.get(

                    "message",

                    "Deepfake status failed"

                )

            )


        data = (

            response.get(

                "data",

                {}

            )

        )


        code = (

            data.get(

                "code"

            )

        )


        # 1012


        if code == "1012":


            return {


                "completed":

                False,


                "message":

                "Deepfake processing in progress"


            }



        # 1013


        if code != "1013":


            raise Exception(


                data.get(

                    "message",

                    "Deepfake lookup failed"

                )

            )



        faces = (

            data.get(

                "deepfake_data",

                {}

            )

            .get(

                "faces",

                []

            )

        )



        fake_probability = 0



        if len(

                faces

        ) > 0:



            fake_probability = (

                faces[0]

                .get(

                    "fake_probability",

                    0

                )

            )



        return {


            "completed":

            True,


            "fake_probability":

            fake_probability,


            "request_id":

            response.get(

                "request_id"

            ),


            "raw_response":

            response

        }
