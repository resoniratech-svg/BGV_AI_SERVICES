from flask import Blueprint, Config
from flask import request
from flask import jsonify
from config import Config
#from services.didit_service import (
    #DiditService
#)

didit_bp = Blueprint(
    "didit_bp",
    __name__
)


#@didit_bp.route(
    #"/didit/create-session",
    #methods=["POST"]
#)
#def create_didit_session():

    #data = request.get_json()

    #result = DiditService.create_session(

    #workflow_id=data["workflow_id"],

    #candidate_id=data["candidate_id"],

    #callback_url=Config.DIDIT_WEBHOOK_URL,

    #verification_type=data["verification_type"]
    
#)

    #return jsonify(result), 200