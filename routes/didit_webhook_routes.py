from flask import Blueprint
from flask import request
from flask import jsonify

import json

from app.repositories.didit_repository import (
    DiditRepository
)

didit_webhook_bp = Blueprint(
    "didit_webhook_bp",
    __name__
)


@didit_webhook_bp.route(
    "/didit/webhook",
    methods=["POST"]
)
def didit_webhook():

    data = request.json

    print(data)

    # ==========================================
    # SAVE CALLBACK LOG
    # ==========================================

    DiditRepository.save_provider_callback({

        "provider_name": "DIDIT",

        "provider_session_id": data.get(
            "session_id"
        ),

        "callback_type": "VERIFICATION_RESULT",

        "callback_payload": json.dumps(data),

        "callback_status": data.get(
            "status"
        )
    })

    # ==========================================
    # SAVE DOCUMENT DETAILS
    # ==========================================

    document_data = data.get(
        "document",
        {}
    )
    DiditRepository.update_session_status(

    provider_session_id=data.get(
        "session_id"
    ),

    status=data.get(
        "status"
    )
)
    DiditRepository.save_verification_document({

        "session_id": 1,

        "candidate_id": 1,

        "document_type": document_data.get(
            "document_type"
        ),

        "document_number": document_data.get(
            "document_number"
        ),

        "full_name": document_data.get(
            "full_name"
        ),

        "nationality": document_data.get(
            "nationality"
        ),

        "issuing_country": document_data.get(
            "issuing_country"
        ),

        "verification_status": data.get(
            "status"
        ),

        "raw_response": json.dumps(data)
    })

    return jsonify({

        "status": "success",

        "message": "Webhook processed successfully"
    }), 200