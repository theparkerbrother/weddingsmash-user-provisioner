# routes/remove_user.py

from flask import Blueprint, request, jsonify

from services.quickbase import (
    update_contractor_record,
    remove_user_from_role_xml
)

from utils.auth import is_valid_request

remove_user_api = Blueprint('remove_user_api', __name__)

@remove_user_api.route('/remove-user', methods=['POST'])
def remove_user():
    if not is_valid_request(request):
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    contractorId = data.get('contractorId')
    roleId = data.get('roleId')
    userId = data.get('userId')

    missing_fields = {}
    if not contractorId:
        missing_fields["contractorId"] = "Contractor ID is required"
    if not roleId:
        missing_fields["roleId"] = "Role ID is required"
    if not userId:
        missing_fields["userId"] = "User ID is required"

    if missing_fields:
        return jsonify({"error": "Missing required data", "missing data": missing_fields}), 400
    
    result = {
        "status": None,
        "remove_from_role": None,
        "remove_user_from_contractor_record": None
    }

    role_result = remove_user_from_role_xml(userId, roleId)

    if role_result:
        result["remove_from_role"]="success"
        record_update_result = update_contractor_record(contractorId,"")
        if record_update_result != "error":
            result["remove_user_from_contractor_record"] = "success"
            result["status"] = "success"
            return jsonify({"result": result}),200
        else:
            result["remove_user_from_contractor_record"] = "error"
            result["status"] = "failure"
            return jsonify({"result": result}),500
    else:
        result["status"] = "failure"
        result["remove_from_role"] = "error"
        return jsonify({"result": result}),500
