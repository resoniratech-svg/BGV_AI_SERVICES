import json


from services.ongrid.deepfake_init_service import DeepfakeInitService


from services.ongrid.deepfake_status_service import DeepfakeStatusService


from repositories.deepfake_repository import DeepfakeRepository


class DeepfakeVerificationService:
    @staticmethod
    def verify_image(candidate_id, bgv_id, document_id):

        init_response = DeepfakeInitService.initialize(
            candidate_id, bgv_id, document_id
        )

        transaction_id = init_response.get("transaction_id")

        if not transaction_id:
            raise Exception("Deepfake transaction id not received")

        status_response = DeepfakeStatusService.get_status(transaction_id)

        if not status_response:
            raise Exception("Deepfake status response empty")

        if not status_response.get("completed"):
            raise Exception("Deepfake processing in progress")

        fake_probability = status_response.get("fake_probability", 0)

        verification_status = "REAL" if fake_probability < 0.50 else "FAKE"

        DeepfakeRepository.save_result(
            candidate_id=candidate_id,
            bgv_id=bgv_id,
            document_id=document_id,
            transaction_id=transaction_id,
            fake_probability=fake_probability,
            verification_status=verification_status,
            provider_name="GRIDLINES",
            api_reference_id=status_response.get("request_id"),
            raw_response=json.dumps(status_response.get("raw_response")),
        )

        return {
            "success": verification_status == "REAL",
            "verification_status": verification_status,
            "fake_probability": fake_probability,
            "provider": "GRIDLINES",
            "response": status_response.get("raw_response"),
        }
