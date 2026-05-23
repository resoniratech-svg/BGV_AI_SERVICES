from config import Config


ALLOWED_MIME_TYPES = [
    "image/png",
    "image/jpeg",
    "application/pdf"
]


def allowed_file(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in Config.ALLOWED_EXTENSIONS


def validate_mime_type(file):

    if file.mimetype not in ALLOWED_MIME_TYPES:
        return False

    return True