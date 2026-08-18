from flask import Blueprint, request, jsonify

from services.bank_statement_verification_service import (
    BankStatementVerificationService,
)
from services.bank_statement_result_service import BankStatementResultService

bank_statement_bp = Blueprint("bank_statement", __name__)


###############################################################
# BANK STATEMENT UPLOAD
###############################################################


@bank_statement_bp.route("/upload", methods=["POST"])
def upload_bank_statement():

    try:
        #######################################################
        # REQUEST JSON
        #######################################################

        data = request.get_json()

        #######################################################
        # REQUIRED VALUES
        #######################################################

        candidate_id = data.get("candidate_id")

        bgv_id = data.get("bgv_id")

        #######################################################
        # OPTIONAL VALUES
        #######################################################

        bank_name = data.get("bank_name")

        bank_statement_password = data.get("bank_statement_password")

        #######################################################
        # VALIDATION
        #######################################################

        if not candidate_id:
            return jsonify(
                {"success": False, "message": "candidate_id is required."}
            ), 400

        if not bgv_id:
            return jsonify({"success": False, "message": "bgv_id is required."}), 400

        #######################################################
        # VERIFY
        #######################################################

        result = BankStatementVerificationService.upload_bank_statement(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            bank_name=bank_name,
            bank_statement_password=bank_statement_password,
        )

        #######################################################
        # RETURN
        #######################################################

        return jsonify(result), 200

    except Exception as exception:
        return jsonify({"success": False, "message": str(exception)}), 500
    ###############################################################


# GET BANK STATEMENT RESULT
###############################################################


@bank_statement_bp.route("/result/<int:candidate_id>", methods=["GET"])
def get_bank_statement_result(candidate_id):

    try:
        bgv_id = request.args.get("bgv_id")

        if not bgv_id:
            return jsonify({"success": False, "message": "bgv_id is required."}), 400

        result = BankStatementResultService.get_result(
            candidate_id,
            bgv_id,
        )

        return jsonify({"success": True, "data": result}), 200

    except Exception as error:
        print("=" * 80)
        print("BANK STATEMENT RESULT ERROR")
        print(error)
        print("=" * 80)

        return jsonify({"success": False, "message": str(error)}), 500
