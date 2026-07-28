from flask import Blueprint
from flask import request
from flask import jsonify

from services.bank_statement_verification_service import (
    BankStatementVerificationService
)

bank_statement_callback_bp = Blueprint(

    "bank_statement_callback",

    __name__

)

###############################################################
# BANK STATEMENT CALLBACK
###############################################################

@bank_statement_callback_bp.route(

    "/bank-statement/callback",

    methods=["POST"]

)
def bank_statement_callback():

    try:

        ###########################################################
        # CALLBACK PAYLOAD
        ###########################################################

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "message": "Request body is required."

            }), 400

        ###########################################################
        # PROCESS CALLBACK
        ###########################################################

        result = (

            BankStatementVerificationService
            .process_callback(

                callback_payload=data

            )

        )

        ###########################################################
        # SUCCESS
        ###########################################################

        return jsonify({

            "success": True,

            "message": "Bank Statement callback processed successfully.",

            "data": result

        }), 200

    except Exception as error:

        print("=" * 80)
        print("BANK STATEMENT CALLBACK ERROR")
        print(error)
        print("=" * 80)

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500