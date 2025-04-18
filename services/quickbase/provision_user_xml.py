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

def provision_user_xml(email, roleId, fname, lname):
    # XML payload for the API request
    xml_payload = f"""
    <qdbapi>
        <usertoken>{user_token}</usertoken>
        <email>{email}</email>
        <roleid>{roleId}</roleid>
        <fname>{fname}</fname>
        <lname>{lname}</lname>
    </qdbapi>
    """.strip()

    # Define the URL and headers
    url = f"https://quincy.quickbase.com/db/{app_id}"
    headers = {
        "Content-Type": "application/xml",
        "QUICKBASE-ACTION": "API_ProvisionUser"
    }

    # Make the request to Quickbase
    try:
        response = requests.post(url, data=xml_payload, headers=headers)
        response.raise_for_status()  # Will raise an error if status code is not 200
        # Sample Response
        # <?xml version="1.0" ?>
        # <qdbapi>
        #     <action>api_provisionuser</action>
        #     <errcode>0</errcode>
        #     <errtext>No error</errtext>
        #     <userid>112248.5nzg</userid>
        # </qdbapi>
        json_response = convert_xml_to_dict(response.text)
        user_id = json_response.get("qdbapi", {}).get("userid")

        if user_id:
            return user_id
        else:
            print("Error occurred in provisioning user.")
            return None
        
    except requests.exceptions.RequestException as e:
        # Handle errors in the request (e.g., network issues, bad response)
        print(f"Error occurred in provisioning user: {e}")
        return None