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


def get_user_info_xml(email):
    # XML payload for the API request
    xml_payload = f"""
    <qdbapi>
        <usertoken>{user_token}</usertoken>
        <email>{email}</email>
    </qdbapi>
    """.strip()

    # Define the URL and headers
    url = "https://quincy.quickbase.com/db/main"
    headers = {
        "Content-Type": "application/xml",
        "QUICKBASE-ACTION": "API_GetUserInfo"
    }

    # Make the request to Quickbase
    try:
        response = requests.post(url, data=xml_payload, headers=headers)
        response.raise_for_status()  # Will raise an error if status code is not 200
        # Sample Response if user exists
        # <?xml version="1.0" ?>
        # <qdbapi>
        #     <action>API_GetUserInfo</action>
        #     <errcode>0</errcode>
        #     <errtext>No error</errtext>
        #     <user id="67596619.btyw">
        #         <firstName>test</firstName>
        #         <lastName>87</lastName>
        #         <login>test87@ivorygrove.com</login>
        #         <email>test87@ivorygrove.com</email>
        #         <screenName></screenName>
        #         <isVerified>0</isVerified>
        #         <externalAuth>0</externalAuth>
        #     </user>
        # </qdbapi>

        # Sample Response if user doesn't exist
        # <?xml version="1.0" ?>
        # <qdbapi>
        #     <action>API_GetUserInfo</action>
        #     <errcode>2</errcode>
        #     <errtext>Invalid input</errtext>
        #     <errdetail>The user with the specified email address or user name does not exist.</errdetail>
        # </qdbapi>

        # Sample json_response
        # {
        #     "qdbapi": {
        #         "action": "API_GetUserInfo",
        #         "errcode": "0",
        #         "errtext": "No error",
        #         "user": {
        #             "@id": "67596619.btyw",
        #             "firstName": "test",
        #             "lastName": "87",
        #             "login": "test87@ivorygrove.com",
        #             "email": "test87@ivorygrove.com",
        #             "screenName": None,
        #             "isVerified": "0",
        #             "externalAuth": "0"
        #         }
        #     }
        # }

        print("API_GetUserInfo: Raw xml response text from Quickbase:", response.text)
        data = convert_xml_to_dict(response.text)
        print("API_GetUserInfo: Response from Quickbase as dictionary:", data)

        qdbapi_data = data.get("qdbapi", {})
        if qdbapi_data.get("errcode") != "0":
            print(f"Quickbase error: {qdbapi_data.get('errtext')} - {qdbapi_data.get('errdetail')}")
            return None

        user_id = qdbapi_data.get("user", {}).get("@id")
        if user_id:
            print(f"User ID found for {email}: {user_id}")
            return user_id
        else:
            print(f"User object found but no ID for {email}")
            return None

    except requests.exceptions.RequestException as e:
        # Handle errors in the request (e.g., network issues, bad response)
        print(f"Error occurred while getting user info: {e}")
        return None