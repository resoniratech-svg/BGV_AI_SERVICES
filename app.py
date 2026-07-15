from flask import Flask, request, jsonify
from flask_cors import CORS

from flask_jwt_extended import JWTManager

import os

from config import Config
from db import mysql
from routes.ai_routes import ai_bp
from routes.health_routes import health_bp
from utils.auth import generate_token
from routes.didit_routes import didit_bp
from routes.didit_webhook_routes import didit_webhook_bp
from routes.rchilli_routes import (
    rchilli_bp
)
from routes.dilisense_routes import (
    dilisense_bp
)
from routes.indiankanoon_routes import (
    indiankanoon_bp
)
from routes.court_record_routes import (
    court_record_bp
)

from routes.report_routes import (
    report_bp
)

from routes.passport_routes import (
    passport_bp
)
from routes.document_routes import (
    document_bp
)
from routes.driving_license_routes import (
    driving_license_bp
)
from routes.aadhaar_routes import (
    aadhaar_bp
)
from routes.pan_routes import (
    pan_bp
)

from routes.deepfake_routes import (
    deepfake_bp
)

from routes.face_match_routes import (

    face_match_bp

)
from routes.credit_bureau_routes import (
    credit_bureau_bp
)
from routes.consent_routes import (
    consent_bp
)
from routes.ccrv_callback_routes import (
    ccrv_callback_bp
)
from routes.ccrv_routes import (
    ccrv_bp
)
from routes.salary_slip_routes import (
    salary_slip_bp
)
from routes.employment_routes import (
    employment_bp
)



app = Flask(__name__)
# JWT Configuration
app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY

jwt = JWTManager(app)

# CORS
CORS(app)

# Upload Folder Configuration
app.config["UPLOAD_FOLDER"] = Config.UPLOAD_FOLDER

os.makedirs(
    Config.UPLOAD_FOLDER,
    exist_ok=True
)

# Register Blueprint
app.register_blueprint(
    ai_bp,
    url_prefix="/api/v1"
)

app.register_blueprint(
    health_bp,
    url_prefix="/api/v1"
)
app.register_blueprint(
    didit_bp,
    url_prefix="/api/v1"
)
app.register_blueprint(
    didit_webhook_bp,
    url_prefix="/api/v1"
)
app.register_blueprint(
    rchilli_bp,
    url_prefix="/api/v1"
)

app.register_blueprint(

    dilisense_bp,

    url_prefix="/api/v1"
)
app.register_blueprint(

    indiankanoon_bp,

    url_prefix="/api/v1"
)
app.register_blueprint(

    court_record_bp,

    url_prefix="/api/v1"
)

app.register_blueprint(

    report_bp,

    url_prefix="/api/v1"
)
app.register_blueprint(
    passport_bp,
    url_prefix="/api/v1"
)

app.register_blueprint(
    driving_license_bp,
    url_prefix="/api/v1"
)
app.register_blueprint(
    document_bp,
    url_prefix="/api/v1"
)
app.register_blueprint(
    aadhaar_bp,
    url_prefix="/api/v1"
)
app.register_blueprint(
    pan_bp,
    url_prefix="/api/v1"
)
app.register_blueprint(

    deepfake_bp,

    url_prefix="/api/v1"

)

app.register_blueprint(

    face_match_bp,

    url_prefix="/api/v1"

)
app.register_blueprint(

    credit_bureau_bp,

    url_prefix="/api/v1"

)
app.register_blueprint(

    consent_bp,

    url_prefix="/api/v1"

)
app.register_blueprint(

    ccrv_callback_bp,

    url_prefix="/api/v1"

)
app.register_blueprint(
    ccrv_bp,
    url_prefix="/api/v1"
)
app.register_blueprint(
    salary_slip_bp,
    url_prefix="/api/v1"
)
app.register_blueprint(

    employment_bp,

    url_prefix="/api/v1"

)

# LOGIN API
@app.route("/login", methods=["POST"])
def login():

    data = request.json

    username = data.get("username")

    password = data.get("password")

    # ROLE CHECKS
    if username == "admin" and password == "admin123":

        role = "SUPER_ADMIN"

    elif username == "hr" and password == "hr123":

        role = "HR"

    elif username == "reviewer" and password == "review123":

        role = "REVIEWER"

    else:

        return jsonify({

            "success": False,

            "message": "Invalid credentials"

        }), 401

    # GENERATE TOKEN
    token = generate_token(
        username,
        role
    )

    return jsonify({

        "success": True,

        "role": role,

        "access_token": token

    })


# MAIN
if __name__ == "__main__":

    print("STARTING PRODUCTION BGV AI SERVICE...")

    app.run(

        host=Config.HOST,

        port=Config.PORT,

        debug=True
    )

    