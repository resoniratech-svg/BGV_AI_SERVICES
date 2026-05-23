import os
from dotenv import load_dotenv
import pytesseract

load_dotenv()

class Config:

    HOST = os.getenv("HOST")

    PORT = int(os.getenv("PORT"))

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE"))

    ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS").split(",")

    TESSERACT_PATH = os.getenv("TESSERACT_PATH")

    LOG_LEVEL = os.getenv("LOG_LEVEL")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    JWT_ACCESS_TOKEN_EXPIRES = int(
    os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600)
    )
pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_PATH
print("AI JWT SECRET:", Config.JWT_SECRET_KEY)