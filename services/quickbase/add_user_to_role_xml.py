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

def add_user_to_role_xml(user_id,role_id):
    # XML payload for the API request
    xml_payload = f"""
    <qdbapi>
        <usertoken>{user_token}</usertoken>
        <userid>{user_id}</userid>
        <roleid>{role_id}</roleid>
    </qdbapi>
    """.strip()

    # Define the URL and headers
    url = f"https://quincy.quickbase.com/db/{app_id}"
    headers = {
        "Content-Type": "application/xml",
        "QUICKBASE-ACTION": "API_AddUserToRole"
    }

    # Make the request to Quickbase
    try:
        response = requests.post(url, data=xml_payload, headers=headers)
        response.raise_for_status()  # Will raise an error if status code is not 200
        # Sample Response if user is added to the role
        # <?xml version="1.0" ?>
        # <qdbapi>
        #     <action>API_AddUserToRole</action>
        #     <errcode>0</errcode>
        #     <errtext>No error</errtext>
        # </qdbapi>

        # Sample Response if user is already in that role
        # <?xml version="1.0" ?>
        # <qdbapi>
        #     <action>API_AddUserToRole</action>
        #     <errcode>113</errcode>
        #     <errtext>User is already in specified role.</errtext>
        # </qdbapi>

        # Sample json_response
        # {
        #     "qdbapi": {
        #         "action": "API_AddUserToRole",
        #         "errcode": "0",
        #         "errtext": "No error"
        #     }
        # }

        print("API_AddUserToRole: Raw xml response text from Quickbase:", response.text)
        data = convert_xml_to_dict(response.text)
        print("API_AddUserToRole: Response from Quickbase as dictionary:", data)

        qdbapi_data = data.get("qdbapi", {})
        if qdbapi_data.get("errcode") != "0":
            print(f"Quickbase error: {qdbapi_data.get('errtext')} - {qdbapi_data.get('errdetail')}")
            return None
        else:
            return True


    except requests.exceptions.RequestException as e:
        # Handle errors in the request (e.g., network issues, bad response)
        print(f"API_AddUserToRole: Error occurred: {e}")
        return None