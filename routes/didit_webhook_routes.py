from flask import Blueprint
from flask import request
from flask import jsonify

import json

from app.repositories.didit_repository import (
    DiditRepository
)

from repositories.driving_license_repository import (
    DrivingLicenseRepository
)

from repositories.passport_repository import (
    PassportRepository
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

    try:

        data = request.json

        print(data)

        # ==========================================
        # DOCUMENT DATA
        # ==========================================

        document_data = data.get(
            "document",
            {}
        )

        document_type = (
            document_data.get(
                "document_type",
                ""
            )
            .strip()
            .upper()
        )

        # ==========================================
        # SAVE CALLBACK LOG
        # ==========================================

        DiditRepository.save_provider_callback({

            "provider_name": "DIDIT",

            "provider_session_id": data.get(
                "session_id"
            ),

            "callback_type": "VERIFICATION_RESULT",

            "callback_payload": json.dumps(
                data
            ),

            "callback_status": data.get(
                "status"
            )
        })

        # ==========================================
        # UPDATE SESSION STATUS
        # ==========================================

        DiditRepository.update_session_status(

            provider_session_id=data.get(
                "session_id"
            ),

            status=data.get(
                "status"
            )
        )

        # ==========================================
        # SAVE VERIFICATION DOCUMENT
        # ==========================================

        DiditRepository.save_verification_document({

            "session_id": 1,

            "candidate_id": 1,

            "document_type": document_type,

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

            "raw_response": json.dumps(
                data
            )
        })

        # ==========================================
        # SAVE DRIVING LICENSE RESULT
        # ==========================================

        if document_type == "DRIVING_LICENSE":

            DrivingLicenseRepository.save_driving_license_result(

                candidate_id=1,

                bgv_id=1,

                verification_status=data.get(
                    "status"
                ),

                license_number=document_data.get(
                    "document_number"
                ),

                full_name=document_data.get(
                    "full_name"
                ),

                date_of_birth=document_data.get(
                    "date_of_birth"
                ),

                issue_date=document_data.get(
                    "issue_date"
                ),

                expiry_date=document_data.get(
                    "expiry_date"
                ),

                provider_name="Didit",

                raw_response=json.dumps(
                    data
                )
            )

        # ==========================================
        # SAVE PASSPORT RESULT
        # ==========================================

        elif document_type == "PASSPORT":

            PassportRepository.save_passport_result(

                candidate_id=1,

                bgv_id=1,

                verification_status=data.get(
                    "status"
                ),

                passport_number=document_data.get(
                    "document_number"
                ),

                full_name=document_data.get(
                    "full_name"
                ),

                nationality=document_data.get(
                    "nationality"
                ),

                country=document_data.get(
                    "issuing_country"
                ),

                date_of_birth=document_data.get(
                    "date_of_birth"
                ),

                issue_date=document_data.get(
                    "issue_date"
                ),

                expiry_date=document_data.get(
                    "expiry_date"
                ),

                provider_name="Didit",

                raw_response=json.dumps(
                    data
                )
            )

        return jsonify({

            "status": "success",

            "message": "Webhook processed successfully"
        }), 200

    except Exception as error:

        print(str(error))

        return jsonify({

            "status": "failed",

            "message": "Webhook processing failed",

            "error": str(error)
        }), 500