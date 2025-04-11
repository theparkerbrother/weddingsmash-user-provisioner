# routes/add_user.py

from flask import Blueprint, request, jsonify
from services.quickbase import get_user_info

add_user_api = Blueprint('add_user_api', __name__)

@add_user_api.route('/add-user', methods=['POST'])
def add_user():
    data = request.json
    email = data.get('email')  # Retrieve the email from the request body

    if not email:
        return jsonify({"error": "Email is required"}), 400

    user_info = get_user_info(email)

    if user_info:
        return jsonify({"user_info": user_info}), 200
    else:
        return jsonify({"error": "Failed to retrieve user info"}), 500


