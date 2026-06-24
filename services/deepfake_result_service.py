
from repositories.deepfake_repository import (

    DeepfakeRepository

)



class DeepfakeResultService:



    @staticmethod
    def get_result(

        candidate_id

    ):



        result = (


            DeepfakeRepository

            .get_result(

                candidate_id

            )

        )



        if not result:



            return {


                "success":

                False,


                "verification_status":

                "NOT_VERIFIED",


                "display_message":

                "Deepfake verification has not been performed"

            }



        verification_status = (

            result.get(

                "verification_status"

            )

        )



        fake_probability = (

            result.get(

                "fake_probability"

            )

        )



        if verification_status == "REAL":



            return {


                "success":

                True,


                "verification_status":

                "REAL",


                "fake_probability":

                fake_probability,


                "display_message":


                "Candidate selfie appears genuine"

            }




        if verification_status == "FAKE":



            return {


                "success":

                False,


                "verification_status":

                "FAKE",


                "fake_probability":

                fake_probability,


                "display_message":


                "Candidate selfie appears manipulated"

            }




        return {


            "success":

            False,


            "verification_status":

            "FAILED",


            "display_message":


            "Deepfake verification failed"

        }
