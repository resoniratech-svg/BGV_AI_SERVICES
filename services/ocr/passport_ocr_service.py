import re

import pytesseract

from PIL import Image

from repositories.document_repository import (
    DocumentRepository
)


class PassportOCRService:

    @staticmethod
    def extract_passport_data(
        document_id
    ):

        document = (
            DocumentRepository
            .get_uploaded_document(
                document_id
            )
        )

        if not document:

            raise Exception(
                "Passport document not found"
            )

        image = Image.open(
            document["file_path"]
        )

        extracted_text = (
            pytesseract.image_to_string(
                image
            )
        )

        # ==========================================
        # PASSPORT NUMBER
        # ==========================================

        passport_number = None

        passport_patterns = [

            r"\b[A-Z][0-9]{7}\b",

            r"\b[A-Z]{1}[0-9]{6,8}\b"
        ]

        for pattern in passport_patterns:
            passport_match = re.search(

                pattern,

                extracted_text
            )

            if passport_match:
                passport_number = (
                    passport_match.group()
                )

                break
        # ==========================================
        # FILE NUMBER
        # ==========================================

        file_number = None

        file_match = re.search(

            r"\bV[A-Z0-9]{6,15}\b",

            extracted_text
        )

        if file_match:

            file_number = (
                file_match.group()
            )

        # ==========================================
        # DATE OF BIRTH
        # ==========================================

        date_of_birth = None

        dob_match = re.search(

            r"\b\d{2}[/-]\d{2}[/-]\d{4}\b",

            extracted_text
        )

        if dob_match:

            date_of_birth = (
                dob_match.group()
            )

        # ==========================================
        # GIVEN NAME
        # ==========================================

        given_name = None

        given_name_match = re.search(

            r"Given Name[s]?\s*[:\-]?\s*([A-Z\s]+)",

            extracted_text,

            re.IGNORECASE
        )

        if given_name_match:

            given_name = (
                given_name_match.group(1)
                .strip()
            )

        # ==========================================
        # SURNAME
        # ==========================================

        surname = None

        surname_match = re.search(

            r"Surname\s*[:\-]?\s*([A-Z\s]+)",

            extracted_text,

            re.IGNORECASE
        )

        if surname_match:

            surname = (
                surname_match.group(1)
                .strip()
            )

        return {

            "passport_number": passport_number,

            "file_number": file_number,

            "date_of_birth": date_of_birth,

            "given_name": given_name,

            "surname": surname,

            "raw_text": extracted_text
        }