import pdfplumber
import os

import pytesseract

from PIL import Image

from pdf2image import convert_from_path

from ocr_config.tesseract_config import *


class OCRUtils:

    @staticmethod
    def extract_text(file_path):

        extracted_text = ""

        file_extension = os.path.splitext(
            file_path
        )[1].lower()

        # ==========================================
        # PDF SUPPORT
        # ==========================================

        if file_extension == ".pdf":
            try:

                with pdfplumber.open(
                    file_path
                ) as pdf:

                    for page in pdf.pages:

                        page_text = (
                            page.extract_text()
                        )

                        if page_text:

                            extracted_text += (
                                page_text + "\n"
                            )

            except Exception:

                pages = convert_from_path(
                    file_path
                )

                for page in pages:

                    text = (
                        pytesseract.image_to_string(
                            page
                        )
                    )

                    extracted_text += (
                        text + "\n"
                    )

        # ==========================================
        # IMAGE SUPPORT
        # ==========================================

        else:

            image = Image.open(
                file_path
            )

            extracted_text = (
                pytesseract.image_to_string(
                    image
                )
            )

        return extracted_text