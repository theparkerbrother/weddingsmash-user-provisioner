# routes/add_user.py

from flask import Blueprint, request, jsonify
from services.quickbase import (
    get_user_info_xml,
    get_user_roles_xml,
    add_member_to_group,
    provision_user_xml,
    add_user_to_role_xml,
    add_update_user_record,
    add_user_permission,
    send_invitation_xml
)
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
    companyId = data.get('companyId')
    companyName = data.get('companyName')

    missing_fields = {}
    if not email:
        missing_fields["email"] = "Email is required"
    if not roleId:
        missing_fields["roleId"] = "Role ID is required"
    if not fname:
        missing_fields["fname"] = "First name is required"
    if not lname:
        missing_fields["lname"] = "Last name is required"
    if not companyId:
        missing_fields["companyId"] = "Company ID is required"
    if not companyName:
        missing_fields["companyName"] = "Company Name is required"

    if missing_fields:
        return jsonify({"error": "Missing required data", "missing data": missing_fields}), 400

    result = {
        "status": None,
        "provisioning": None,
        "user_record": None,
        "user_permission_record": None,
        "invitation": None
    }

    def userAndPermissionRecords(email, companyId, userId, companyName):
        user_record_result = add_update_user_record(email, companyId)

        if user_record_result["userRecordSuccess"]:
            result["user_record"] = "User record is ready!"
        else:
            result["user_record"] = "User record could not be created."

        if user_record_result["permissionRecordExists"] is True:
            result["user_permission_record"] = "User permission record already exists!"
            permission_created_or_exists = True
        else:
            user_permission_record_created = add_user_permission(email, companyId)
            if user_permission_record_created:
                result["user_permission_record"] = "User permission record created!"
                permission_created_or_exists = True
            else:
                result["user_permission_record"] = "User permission record could not be created."
                permission_created_or_exists = False

        if user_record_result["userRecordSuccess"] and permission_created_or_exists:
            invite = send_invitation_xml(userId,companyName)
            if invite:
                result["invitation"] = "Invite sent"
                return True
            else:
                result["invitation"] = "Invite failed to send"
                return False
        else:
            return False

    user_id = get_user_info_xml(email)

    if user_id:
        roles = get_user_roles_xml(user_id)
        role_exists = any(role.get('@id') == str(roleId) for role in roles)

        if role_exists:
            result["provisioning"] = f"Role {roleId} is already assigned to user."
            userAndPermissionRecordsReady = userAndPermissionRecords(email, companyId, user_id, companyName)
            if userAndPermissionRecordsReady:
                result["status"] = "success"
                return jsonify({"result": result}), 200
            else:
                result["status"] = "failure"
                return jsonify({"result": result}), 500

        if add_user_to_role_xml(user_id, roleId):
            result["provisioning"] = f"User exists, added to role {roleId}"
            userAndPermissionRecordsReady = userAndPermissionRecords(email, companyId, user_id, companyName)
            if userAndPermissionRecordsReady:
                result["status"] = "success"
                return jsonify({"result": result}), 200
            else:
                result["status"] = "failure"
                return jsonify({"result": result}), 500
        else:
            result["provisioning"] = f"User exists but could not be added to role {roleId}"
            result["status"] = "failure"
            return jsonify({"result": result}), 500

    else:
        new_user_id = provision_user_xml(email, roleId, fname, lname)

        if not new_user_id:
            result["provisioning"] = "Failed to provision new user"
            result["status"] = "failure"
            return jsonify({"result": result}), 500
        else:
            result["provisioning"] = f"User provisioned and added to role {roleId}"
            userAndPermissionRecordsReady = userAndPermissionRecords(email, companyId, user_id, companyName)
            if userAndPermissionRecordsReady:
                result["status"] = "success"
                return jsonify({"result": result}), 200
            else:
                result["status"] = "failure"
                return jsonify({"result": result}), 500
