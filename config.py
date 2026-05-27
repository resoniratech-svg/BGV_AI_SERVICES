import os
from dotenv import load_dotenv
import pytesseract

load_dotenv()


class Config:

    # ==========================================
    # BASIC CONFIG
    # ==========================================

    HOST = os.getenv("HOST")

    PORT = int(os.getenv("PORT", 5001))

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10485760))

    ALLOWED_EXTENSIONS = os.getenv(
        "ALLOWED_EXTENSIONS",
        "jpg,jpeg,png,pdf"
    ).split(",")

    TESSERACT_PATH = os.getenv("TESSERACT_PATH")

    LOG_LEVEL = os.getenv("LOG_LEVEL")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    JWT_ACCESS_TOKEN_EXPIRES = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600)
    )

    # ==========================================
    # DIDIT CONFIG
    # ==========================================
    # ==========================================
# DIDIT CONFIG
# ==========================================

    DIDIT_BASE_URL = os.getenv(
        "DIDIT_BASE_URL"
    )

    DIDIT_API_KEY = os.getenv(
        "DIDIT_API_KEY"
    )

    DIDIT_PASSPORT_WORKFLOW_ID = os.getenv(
        "DIDIT_PASSPORT_WORKFLOW_ID"
    )

    DIDIT_DL_WORKFLOW_ID = os.getenv(
        "DIDIT_DL_WORKFLOW_ID"
    )

    DIDIT_WEBHOOK_URL = os.getenv(
        "DIDIT_WEBHOOK_URL"
    )
        # ==========================================
    # MYSQL CONFIG
    # ==========================================

    MYSQL_HOST = os.getenv(
        "MYSQL_HOST"
    )

    MYSQL_USER = os.getenv(
        "MYSQL_USER"
    )

    MYSQL_PASSWORD = os.getenv(
        "MYSQL_PASSWORD"
    )

    MYSQL_DB = os.getenv(
        "MYSQL_DB"
    )

    MYSQL_PORT = int(
        os.getenv("MYSQL_PORT", 3306)
    )
# ==========================================
# RCHILLI CONFIG
# ==========================================

    # ==========================================
# RCHILLI CONFIG
# ==========================================

    # ==========================================
# RCHILLI CONFIG
# ==========================================

    RCHILLI_API_URL = os.getenv(
        "RCHILLI_API_URL"
    )

    RCHILLI_USER_KEY = os.getenv(
        "RCHILLI_USER_KEY"
    )

    RCHILLI_VERSION = os.getenv(
        "RCHILLI_VERSION"
    )

    RCHILLI_SUBUSER_ID = os.getenv(
        "RCHILLI_SUBUSER_ID"
    )
    # ==========================================
# DILISENSE AML CONFIG
# ==========================================

    # ==========================================
# DILISENSE CONFIG
# ==========================================

    DILISENSE_API_KEY = os.getenv(
        "DILISENSE_API_KEY"
    )

    DILISENSE_BASE_URL = os.getenv(
        "DILISENSE_BASE_URL"
    )

    DILISENSE_TIMEOUT = int(
        os.getenv(
            "DILISENSE_TIMEOUT",
            60
        )
    )
# ==========================================
# TESSERACT
# ==========================================

pytesseract.pytesseract.tesseract_cmd = (
    Config.TESSERACT_PATH
)

print("AI JWT SECRET:", Config.JWT_SECRET_KEY)