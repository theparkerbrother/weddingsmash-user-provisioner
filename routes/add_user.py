# routes/add_user.py

from flask import Blueprint, request, jsonify
from services.quickbase import get_user_info_xml, get_user_roles, add_member_to_group, provision_user_xml, add_user_to_role_xml
from utils.auth import is_valid_request

add_user_api = Blueprint('add_user_api', __name__)

@add_user_api.route('/add-user', methods=['POST'])
def add_user():
    if not is_valid_request(request):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    email = data.get('email')
    roleId = data.get('roleId')
    fname = data.get('fname')
    lname = data.get('lname')

    # Validate inputs
    if not email:
        return jsonify({"error": "Email is required"}), 400
    if not roleId:
        return jsonify({"error": "Role ID is required"}), 400
    if not fname:
        return jsonify({"error": "First name is required"}), 400
    if not lname:
        return jsonify({"error": "Last name is required"}), 400

    # Get user info from Quickbase
    user_id = get_user_info_xml(email)

    if user_id:
        roles = get_user_roles(user_id)
        # user_info["roles"] = roles or []

        role_exists = any(role.get('@id') == str(roleId) for role in roles)

        if role_exists:
            return jsonify({
                "message": f"Role {roleId} is already assigned to user."
            }), 200

        if add_user_to_role_xml(user_id, roleId):
            return jsonify({"message": f"User exists, added to role {roleId}"}), 200
        else:
            return jsonify({"error": f"User exists but could not be added to role {roleId}"}), 500

    else:
        # User does not exist — try provisioning
        new_user_id = provision_user_xml(email, roleId, fname, lname)

        if not new_user_id:
            return jsonify({"error": "Failed to provision new user"}), 500
        else:
            return jsonify({"message": f"User provisioned and added to role {roleId}"}), 200






