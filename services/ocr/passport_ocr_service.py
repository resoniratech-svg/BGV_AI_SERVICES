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

        normalized_text = (
            extracted_text
            .replace("\r", "\n")
        )

        print("\n" + "=" * 80)
        print("PASSPORT OCR DEBUG")
        print("=" * 80)
        print(normalized_text)
        print("=" * 80)

        # ==========================================
        # PASSPORT NUMBER
        # ==========================================

        passport_number = None

        passport_patterns = [

            r"\b[A-Z][0-9]{7}\b",

            r"\b[A-Z]{1}[0-9]{6,8}\b"
        ]

        for pattern in passport_patterns:

            match = re.search(
                pattern,
                normalized_text
            )

            if match:

                passport_number = (
                    match.group()
                    .strip()
                )

                break

        # ==========================================
        # FILE NUMBER
        # ==========================================

        file_number = None

        file_patterns = [

            r"\bV[A-Z0-9]{6,15}\b",

            r"\b[A-Z]{1}[0-9]{10,15}\b"
        ]

        for pattern in file_patterns:

            match = re.search(
                pattern,
                normalized_text
            )

            if match:

                file_number = (
                    match.group()
                    .strip()
                )

                break

        # ==========================================
        # DATE OF BIRTH
        # ==========================================

        date_of_birth = None

        # MRZ line 2 extraction
        mrz_line_match = re.search(

            r"([A-Z]\d{7}<\d[A-Z0-9]{3}\d{6}\d[MF])",

            normalized_text
        )

        if mrz_line_match:
            print("=" * 80)
            print("MRZ MATCH =", mrz_line_match)
            print("=" * 80)

            mrz_line = mrz_line_match.group(1)

            dob_raw = mrz_line[13:19]

            year = int(dob_raw[:2])

            if year >= 50:

                year += 1900

            else:

                year += 2000

            month = dob_raw[2:4]

            day = dob_raw[4:6]

            date_of_birth = (
                f"{day}/{month}/{year}"
            )
        # ==========================================
        # SURNAME
        # ==========================================

        surname = None

        surname_patterns = [

            r"Surname\s*[:\-]?\s*([A-Z ]+)",

            r"Surname\s*\n+\s*([A-Z ]+)"
        ]

        for pattern in surname_patterns:

            match = re.search(
                pattern,
                normalized_text,
                re.IGNORECASE
            )

            if match:

                surname = (
                    match.group(1)
                    .replace("\n", " ")
                    .strip()
                )

                break

        # ==========================================
        # GIVEN NAME
        # ==========================================

        given_name = None

        given_name_patterns = [

            r"Given\s*Name(?:s)?\s*[:\-]?\s*([A-Z ]+)",

            r"Given\s*Name(?:s)?\s*\n+\s*([A-Z ]+)"
        ]

        for pattern in given_name_patterns:

            match = re.search(
                pattern,
                normalized_text,
                re.IGNORECASE
            )

            if match:

                given_name = (
                    match.group(1)
                    .replace("\n", " ")
                    .strip()
                )

                break

        # ==========================================
        # MRZ FALLBACK
        # ==========================================

        if not surname or not given_name:

            mrz_match = re.search(

                r"P<[A-Z]{3}([A-Z]+)<<([A-Z<]+)",

                normalized_text
            )

            if mrz_match:

                if not surname:

                    surname = (
                        mrz_match.group(1)
                        .replace("<", " ")
                        .strip()
                    )

                if not given_name:

                    given_name = (
                        mrz_match.group(2)
                        .replace("<", " ")
                        .strip()
                    )

        print("\n" + "=" * 80)
        print("PASSPORT OCR RESULT")
        print("=" * 80)
        print("PASSPORT NUMBER :", passport_number)
        print("FILE NUMBER     :", file_number)
        print("SURNAME         :", surname)
        print("GIVEN NAME      :", given_name)
        print("DATE OF BIRTH   :", date_of_birth)
        print("=" * 80)

        return {

            "passport_number": passport_number,

            "file_number": file_number,

            "date_of_birth": date_of_birth,

            "given_name": given_name,

            "surname": surname,

            "raw_text": normalized_text
        }