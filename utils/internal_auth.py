from flask import request


def validate_internal_api_key():

    api_key = request.headers.get(
        "X-API-KEY"
    )

    return api_key == "your_internal_secret"