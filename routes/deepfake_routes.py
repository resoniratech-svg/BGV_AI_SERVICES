from flask import Blueprint
from flask import request
from flask import jsonify


from services.ongrid.deepfake_verification_service import (

    DeepfakeVerificationService

)


from services.deepfake_result_service import (

    DeepfakeResultService

)



deepfake_bp = Blueprint(

    "deepfake",

    __name__

)



# ===================================

# VERIFY

# ===================================


@deepfake_bp.route(

    "/deepfake/verify",

    methods=["POST"]

)

def verify_deepfake():



    data=request.json



    result=(


        DeepfakeVerificationService


        .verify_image(



            candidate_id=

            data["candidate_id"],



            bgv_id=

            data["bgv_id"],



            document_id=

            data["document_id"]


        )


    )



    return jsonify(result)




# ===================================

# GET RESULT

# ===================================


@deepfake_bp.route(

    "/deepfake/result/<int:candidate_id>",

    methods=["GET"]

)


def get_result(

        candidate_id

):



    result=(


        DeepfakeResultService


        .get_result(


            candidate_id

        )



    )



    return jsonify(


        result

    )




