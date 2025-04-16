# routes/add_user.py

from flask import Blueprint, request, jsonify
from services.quickbase import get_user_info, get_user_roles, add_member_to_group, provision_user_xml
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

    if not email:
        return jsonify({"error": "Email is required"}), 400

    if not roleId:
        return jsonify({"error": "Role ID is required"}), 400
    
    if not fname:
        return jsonify({"error": "fname is required"}), 400

    if not lname:
        return jsonify({"error": "lname is required"}), 400

    user_info = get_user_info(email)

    if user_info:
        # Quickbase User already exists
        user_id = user_info.get("user_id")  # Make sure this key matches what your function returns
        if user_id:
            roles = get_user_roles(user_id)
            user_info["roles"] = roles  # Attach the roles to the user info
            
            # Check if the provided roleId exists in the user's roles
            role_exists = any(role.get('@id') == str(roleId) for role in roles)
            
            if role_exists:
                # User has already been added in specified role
                return jsonify({"message": f"Role {roleId} is found for the user.", "user_info": user_info}), 200
            else:
                # User has NOT been added in specified role
                if add_member_to_group(user_id) == True:
                    return jsonify({"message": f"User added"}), 200
                else:
                    return jsonify({"message": f"User already exists, but could not be added in the role"}), 500
        else:
            user_info["roles"] = []  # Or handle as you like if no user_id was found

        return jsonify({"user_info": user_info}), 200
    else:
        # Quickbase User does NOT exist
        user_id = provision_user_xml(email, roleId, fname, lname)
        if user_id:
            if add_member_to_group(user_id) == True:
                return jsonify({"message": f"User provisioned and added"}), 200
            else: 
                return jsonify({"message": f"User provisioned but not added to the application"}), 500
        else:
                return jsonify({"error": "user not added"}), 500
        # return jsonify({"message": "User does not exist"}), 200




