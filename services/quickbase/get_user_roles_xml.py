import os
import requests
from utils.xml_utils import parse_user_info, convert_xml_to_dict


user_token = os.getenv("QB_USER_TOKEN")
realm = os.getenv("QB_REALM_HOSTNAME")
app_id = os.getenv("QB_APP_ID")
smash_magic_user_token = os.getenv("SMASH_MAGIC_USER_TOKEN")
group_id = "121561"
user_table_id = "brs2v3sdf"
user_permission_table_id = "brqhzreui"
contractor_table_id = "brhbgd4w3"

def get_user_roles_xml(userId):
    # XML payload for the API request
    xml_payload = f"""
    <qdbapi>
        <usertoken>{user_token}</usertoken>
        <userid>{userId}</userid>
        <inclgrps>1</inclgrps>
    </qdbapi>
    """.strip()

    # Define the URL and headers
    url = f"https://{realm}/db/{app_id}"
    headers = {
        "Content-Type": "application/xml",
        "QUICKBASE-ACTION": "API_GetUserRole"
    }

    # Make the request to Quickbase
    try:
        response = requests.post(url, data=xml_payload, headers=headers)
        response.raise_for_status()  # Will raise an error if status code is not 200

        json_response = convert_xml_to_dict(response.text)
        roles_data = json_response.get("qdbapi", {}).get("user", {}).get("roles")
        if not roles_data:
            return ["No roles data found"]  # No roles section found

        roles = roles_data.get("role", [])
        if isinstance(roles, dict):
            roles = [roles]

        return roles
    except requests.exceptions.RequestException as e:
        # Handle errors in the request (e.g., network issues, bad response)
        print(f"Error occurred while getting user roles: {e}")
        return None