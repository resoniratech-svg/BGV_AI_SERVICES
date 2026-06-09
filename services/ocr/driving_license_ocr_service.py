import re
import os
import glob

from docx import image
from config import Config
import pytesseract

from PIL import Image

from repositories.document_repository import (
    DocumentRepository
)


class DrivingLicenseOCRService:

    @staticmethod
    def extract_driving_license_data(
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
                "Driving license document not found"
            )

        relative_path = document["file_path"]
        if relative_path.startswith("uploads/"):
            relative_path = relative_path.replace(
                "uploads/",
                "",
                1
            )

        file_path = os.path.abspath(
            document["file_path"]
        )

        # ==========================================
        # DEBUG LOGS
        # ==========================================

        print("\n")
        print("=" * 80)
        print("DRIVING LICENSE OCR DEBUG")
        print("=" * 80)

        print(
            "CURRENT WORKING DIRECTORY:",
            os.getcwd()
        )

        print(
            "DATABASE FILE PATH:",
            document["file_path"]
        )

        print(
            "ABSOLUTE PATH:",
            file_path
        )

        print(
            "FILE EXISTS:",
            os.path.exists(file_path)
        )

        print(
            "UPLOAD FILES FOUND:"
        )

        print(
            glob.glob(
                "uploads/**/*",
                recursive=True
            )
        )

        print("=" * 80)

        # ==========================================
        # FILE EXISTS CHECK
        # ==========================================

        if not os.path.exists(
            file_path
        ):

            raise Exception(
                f"Document file not found: {file_path}"
            )

        # ==========================================
        # FILE HEADER CHECK
        # ==========================================

        file_size = os.path.getsize(
            file_path
        )

        print(
            "FILE SIZE =",
            file_size
        )

        with open(
            file_path,
            "rb"
        ) as file:

            header = file.read(
                30
            )

        print(
            "FILE HEADER =",
            header
        )

        # ==========================================
        # IMAGE OPEN
        # ==========================================

        try:

            image = Image.open(
                file_path
            )

            print(
                "IMAGE FORMAT =",
                image.format
            )

            print(
                "IMAGE SIZE =",
                image.size
            )

            print(
                "IMAGE MODE =",
                image.mode
            )

        except Exception as e:

            raise Exception(
                f"PIL failed to open image: {str(e)}"
            )

        # ==========================================
        # OCR
        # ==========================================

        extracted_text = (
            pytesseract.image_to_string(
                image
            )
        )

        print(
            "OCR TEXT ="
        )

        print(
            extracted_text
        )

        print(
            "OCR TEXT RAW ="
        )

        print(
            repr(extracted_text)
        )
        dl_candidates = re.findall(
            r"[A-Z]{2}\d{2}\s*\d{4}\s*\d{4,8}",
            extracted_text
        )

        print(
            "DL CANDIDATES =",
            dl_candidates
        )

        dl_number = None

        if dl_candidates:

            dl_number = (
                dl_candidates[0]
                .replace(" ", "")
                .strip()
            )

        # ==========================================
        # DATE OF BIRTH
        # ==========================================

        date_of_birth = None

        dob_match = re.search(
            r"DOB\s*[:\-]?\s*(\d{2}[/-]\d{2}[/-]\d{4})",
            extracted_text,
            re.IGNORECASE
        )

        if dob_match:
            date_of_birth = (
                dob_match.group(1)
            )

        print(
            "EXTRACTED DL NUMBER =",
            dl_number
        )

        print(
            "EXTRACTED DOB =",
            date_of_birth
        )

        print("=" * 80)

        return {

            "driving_license_number": dl_number,

            "date_of_birth": date_of_birth,

            "raw_text": extracted_text
        }