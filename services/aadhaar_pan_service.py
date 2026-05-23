from app.providers.surepass.pan_provider import (
    verify_pan
)

from app.providers.surepass.aadhaar_provider import (
    verify_aadhaar
)

from app.providers.surepass.face_match_provider import (
    verify_face_match
)


def process_pan_verification(data):

    return verify_pan(data)


def process_aadhaar_verification(data):

    return verify_aadhaar(data)


def process_face_match(data):

    return verify_face_match(data)