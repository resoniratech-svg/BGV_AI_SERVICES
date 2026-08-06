import os
import base64

from repositories.document_repository import DocumentRepository

from services.ongrid.ongrid_client import OnGridClient


class PanOCRService:
    @staticmethod
    def extract_pan_data(candidate_id, bgv_id, document_id):

        # ======================================
        # GET DOCUMENT
        # ======================================

        document = DocumentRepository.get_uploaded_document(document_id)
        print("\n")
        print("=" * 80)
        print("PAN OCR START")
        print("=" * 80)

        print("candidate_id =", candidate_id)
        print("bgv_id =", bgv_id)
        print("document_id =", document_id)

        print("\nDOCUMENT")
        print(document)
        if not document:
            raise Exception("PAN document not found")

        file_path = os.path.abspath(document["file_path"])
        print("\nFILE PATH")
        print(file_path)

        print("\nFILE EXISTS")
        print(os.path.exists(file_path))
        if not os.path.exists(file_path):
            raise Exception(f"Document file not found: {file_path}")

        # ======================================
        # CONVERT TO BASE64
        # ======================================

        with open(file_path, "rb") as file:
            base64_data = base64.b64encode(file.read()).decode("utf-8")
        print("\nBASE64 CREATED")
        print("Length =", len(base64_data))
        # ======================================
        # OCR REQUEST
        # ======================================

        payload = {"base64_data": base64_data, "consent": "Y"}
        print("\nCALLING GRIDLINES OCR")
        print(payload.keys())
        response = OnGridClient.post("/pan-api/ocr", payload)
        print("\nOCR RESPONSE")
        print(response)

        print("\nRESPONSE KEYS")
        print(response.keys())

        print("\nSTATUS")
        print(response.get("status"))

        print("\nDATA")
        print(response.get("data"))
        # ======================================
        # RESPONSE VALIDATION
        # ======================================

        if not response:
            raise Exception("Empty OCR response received")

        if response.get("status") != 200:
            raise Exception(response.get("message", "PAN OCR failed"))

            # ======================================
            # OCR DATA VALIDATION
            # ======================================

        ocr_data = response.get("data", {}).get("ocr_data")

        print("\nOCR_DATA")
        print(ocr_data)

        if not ocr_data:
            raise Exception(f"OCR DATA MISSING : {response}")

        # ======================================
        # EXTRACT DATA
        # ======================================

        document_data = response["data"]["ocr_data"]["document"]
        print("\nDOCUMENT DATA")
        print(document_data)

        print("=" * 80)
        print("PAN OCR END")
        print("=" * 80)
        pan_number = document_data.get("document_id")

        full_name = document_data.get("name")

        father_name = document_data.get("father_name")

        date_of_birth = document_data.get("date_of_birth")

        # ======================================
        # RETURN DATA
        # ======================================

        return {
            "pan_number": pan_number,
            "full_name": full_name,
            "father_name": father_name,
            "date_of_birth": date_of_birth,
            "request_id": response.get("request_id"),
            "raw_response": response,
        }
