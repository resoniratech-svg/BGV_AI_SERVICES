from flask import Blueprint
from flask import request
from flask import jsonify

import json


ccrv_webhook_bp = Blueprint(

    "ccrv_webhook",

    __name__

)


# =====================================================
# GRIDLINES CCRV WEBHOOK
# =====================================================

@ccrv_webhook_bp.route(

    "/ccrv/webhook",

    methods=["POST"]

)
def ccrv_webhook():

    try:

        payload = request.get_json()

        print("=" * 80)
        print("CCRV WEBHOOK RECEIVED")
        print(json.dumps(payload, indent=4))
        print("=" * 80)

        ####################################################
        # TODO
        #
        # After Gridlines shares callback documentation:
        #
        # 1. Read transaction_id
        # 2. Read CCRV status
        # 3. Update ccrv_requests
        # 4. Save ccrv_results
        # 5. Save ccrv_case_results
        #
        ####################################################

        return jsonify(

            {

                "status": "success",

                "message": "Webhook received"

            }

        ), 200

    except Exception as e:

        return jsonify(

            {

                "status": "error",

                "message": str(e)

            }

        ), 500