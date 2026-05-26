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
app = Flask(__name__)
# ==========================================
# MYSQL CONFIGURATION
# ==========================================

app.config["MYSQL_HOST"] = Config.MYSQL_HOST

app.config["MYSQL_USER"] = Config.MYSQL_USER

app.config["MYSQL_PASSWORD"] = Config.MYSQL_PASSWORD

app.config["MYSQL_DB"] = Config.MYSQL_DB

app.config["MYSQL_PORT"] = Config.MYSQL_PORT

mysql.init_app(app)
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
    