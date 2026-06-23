from flask import Blueprint
from flask import request
from flask import jsonify


from services.ongrid.face_match_service import (
    FaceMatchService
)

from services.face_match_result_service import (
    FaceMatchResultService
)


face_match_bp = Blueprint(

    "face_match",

    __name__

)


# =====================================================
# VERIFY FACE MATCH
# =====================================================

@face_match_bp.route(

    "/face-match/verify",

    methods=["POST"]

)

def verify_face_match():

    try:

        data = request.json


        result = (

            FaceMatchService

            .verify_face(

                candidate_id=

                data["candidate_id"],


                bgv_id=

                data["bgv_id"],


                document_id=

                data["document_id"]

            )

        )


        return jsonify(

            {

                "status":

                "success",


                "message":

                "Face match completed",


                "data":

                result

            }

        ), 200


    except Exception as e:


        return jsonify(

            {

                "status":

                "error",


                "message":

                str(e)

            }

        ), 400




# =====================================================
# GET FACE MATCH RESULT
# =====================================================

@face_match_bp.route(

    "/face-match/result/<int:candidate_id>",

    methods=["GET"]

)

def get_face_match_result(

        candidate_id

):


    try:


        result = (

            FaceMatchResultService

            .get_result(

                candidate_id

            )

        )


        return jsonify(

            {

                "status":

                "success",


                "data":

                result

            }

        ), 200


    except Exception as e:


        return jsonify(

            {

                "status":

                "error",


                "message":

                str(e)

            }

        ), 400
