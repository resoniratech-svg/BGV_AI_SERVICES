from flask import Blueprint
from flask import request
from flask import jsonify

from services.salary_slip_ocr_service import (
    SalarySlipOCRService
)

from repositories.salary_slip_repository import (
    SalarySlipRepository
)


salary_slip_bp = Blueprint(

    "salary_slip_bp",

    __name__

)


###############################################################
# SALARY SLIP OCR
###############################################################

@salary_slip_bp.route(

    "/salary-slip/ocr",

    methods=["POST"]

)
def salary_slip_ocr():

    try:

        ###################################################
        # REQUEST
        ###################################################

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "message": "Request body is required."

            }), 400

        ###################################################
        # INPUTS
        ###################################################

        candidate_id = data.get(

            "candidate_id"

        )

        bgv_id = data.get(

            "bgv_id"

        )

        document_id = data.get(

            "document_id"

        )

        ###################################################
        # VALIDATIONS
        ###################################################

        required_fields = {

            "candidate_id": candidate_id,

            "bgv_id": bgv_id,

            "document_id": document_id

        }

        for field, value in required_fields.items():

            if value is None or str(value).strip() == "":

                return jsonify({

                    "success": False,

                    "message": f"{field} is required."

                }), 400

        ###################################################
        # OCR
        ###################################################

        result = (

            SalarySlipOCRService
            .verify_salary_slip(

                candidate_id=candidate_id,

                bgv_id=bgv_id,

                document_id=document_id

            )

        )

        return jsonify(

            result

        ), 200

    except Exception as error:

        print("=" * 80)
        print("SALARY SLIP OCR ERROR")
        print(error)
        print("=" * 80)

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500


###############################################################
# GET SALARY SLIP OCR RESULT
###############################################################

@salary_slip_bp.route(

    "/salary-slip/result/<int:candidate_id>",

    methods=["GET"]

)
def get_salary_slip_result(

        candidate_id

):

    try:

        result = (

            SalarySlipRepository
            .get_salary_slip_ocr_result(

                candidate_id

            )

        )

        if not result:

            return jsonify({

                "success": False,

                "message": "Salary Slip OCR result not found."

            }), 404

        return jsonify({

            "success": True,

            "data": result

        }), 200

    except Exception as error:

        print("=" * 80)
        print("SALARY SLIP RESULT ERROR")
        print(error)
        print("=" * 80)

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500