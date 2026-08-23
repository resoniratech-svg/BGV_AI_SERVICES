import os
from pathlib import Path
from dotenv import load_dotenv
import pytesseract

BASE_DIR = Path(__file__).resolve().parent

ENV_FILE = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_FILE)


class Config:
    # ==========================================
    # BASIC CONFIG
    # ==========================================

    HOST = os.getenv("HOST")

    PORT = int(os.getenv("PORT", 5001))

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10485760))

    ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS", "jpg,jpeg,png,pdf").split(",")

    TESSERACT_PATH = os.getenv("TESSERACT_PATH")

    LOG_LEVEL = os.getenv("LOG_LEVEL")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))
    # ==========================================
    # DIDIT CONFIG
    # ==========================================

    DIDIT_BASE_URL = os.getenv("DIDIT_BASE_URL")

    DIDIT_API_KEY = os.getenv("DIDIT_API_KEY")

    DIDIT_PASSPORT_WORKFLOW_ID = os.getenv("DIDIT_PASSPORT_WORKFLOW_ID")

    DIDIT_DL_WORKFLOW_ID = os.getenv("DIDIT_DL_WORKFLOW_ID")

    DIDIT_WEBHOOK_URL = os.getenv("DIDIT_WEBHOOK_URL")
    # ==========================================
    # MYSQL CONFIG
    # ==========================================

    MYSQL_HOST = os.getenv("MYSQL_HOST")

    MYSQL_USER = os.getenv("MYSQL_USER")

    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

    MYSQL_DB = os.getenv("MYSQL_DB")

    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    # ==========================================
    # RCHILLI CONFIG
    # ==========================================

    RCHILLI_API_URL = os.getenv("RCHILLI_API_URL")

    RCHILLI_USER_KEY = os.getenv("RCHILLI_USER_KEY")

    RCHILLI_VERSION = os.getenv("RCHILLI_VERSION")

    RCHILLI_SUBUSER_ID = os.getenv("RCHILLI_SUBUSER_ID")

    # ==========================================
    # DILISENSE CONFIG
    # ==========================================

    DILISENSE_API_KEY = os.getenv("DILISENSE_API_KEY")

    DILISENSE_BASE_URL = os.getenv("DILISENSE_BASE_URL")

    DILISENSE_TIMEOUT = int(os.getenv("DILISENSE_TIMEOUT", 60))
    INDIANKANOON_API_TOKEN = os.getenv("INDIANKANOON_API_TOKEN")

    INDIANKANOON_BASE_URL = os.getenv("INDIANKANOON_BASE_URL")
    # ==========================================
    # GRIDLINES
    # ==========================================

    GRIDLINES_ENV = os.getenv("GRIDLINES_ENV")

    # GRIDLINES_SANDBOX_URL = os.getenv("GRIDLINES_SANDBOX_URL")

    GRIDLINES_PRODUCTION_URL = (
        os.getenv("GRIDLINES_PRODUCTION_URL", "").strip().rstrip("/")
    )

    GRIDLINES_API_KEY = os.getenv("GRIDLINES_API_KEY", "").strip()

    AADHAAR_TEMPLATE_ID = os.getenv("AADHAAR_TEMPLATE_ID")

    if not GRIDLINES_API_KEY:
        print("WARNING: GRIDLINES_API_KEY is not loaded")

    if not GRIDLINES_PRODUCTION_URL:
        print("WARNING: GRIDLINES_PRODUCTION_URL is not loaded")
    # ==========================================
    # CALLBACK URL
    # ==========================================

    CCRV_CALLBACK_URL = "http://localhost:5001/api/v1/ccrv/callback"

    BANK_STATEMENT_CALLBACK_URL = (
        os.getenv("BANK_STATEMENT_CALLBACK_URL", "").strip().rstrip("/")
    )

    if not BANK_STATEMENT_CALLBACK_URL:
        print("WARNING: BANK_STATEMENT_CALLBACK_URL is not loaded")


# ==========================================
# TESSERACT
# ==========================================

pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_PATH

print("AI JWT SECRET:", Config.JWT_SECRET_KEY)
