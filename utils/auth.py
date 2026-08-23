from functools import wraps

from flask import jsonify

from flask_jwt_extended import (

    create_access_token,

    get_jwt,

    verify_jwt_in_request

)


def generate_token(identity, role):

    additional_claims = {

        "role": role

    }

    token = create_access_token(

        identity=str(identity),

        additional_claims=additional_claims

    )

    return token


def role_required(allowed_roles):

    def wrapper(fn):

        @wraps(fn)

        def decorator(*args, **kwargs):

            verify_jwt_in_request()

            claims = get_jwt()

            user_role = claims.get("role")

            if user_role not in allowed_roles:

                return jsonify({

                    "success": False,

                    "message": "Unauthorized access"

                }), 403

            return fn(*args, **kwargs)

        return decorator
    
    return wrapper