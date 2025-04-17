# services/quickbase.py

import os
import requests
from utils.xml_utils import parse_user_info, convert_xml_to_dict


user_token = os.getenv("QB_USER_TOKEN")
realm = os.getenv("QB_REALM_HOSTNAME")
app_id = os.getenv("QB_APP_ID")
group_id = "121561"


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


def get_user_roles(userId):
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

def get_user_info(email):
    url = f"https://api.quickbase.com/v1/users"
    headers = {
        "Authorization": f"QB-USER-TOKEN {user_token}",
        "QB-Realm-Hostname": realm,
        "Content-Type": "application/json"
    }
    payload = {
        "emails": [f"{email}"],
        #"appIds": [f"{app_id}"],
        "nextPageToken": ""
    }

    # New
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        print("Raw response text from Quickbase:", response.text)  # raw response
        data = response.json()
        print("Parsed JSON response from Quickbase:", data)        # parsed JSON
    
        if data.get("users"):
            user = data["users"][0]
            user_info = {
                "user_id": user.get("hashId"),
                "userName": user.get("userName"),
                "firstName": user.get("firstName"),
                "lastName": user.get("lastName"),
                "emailAddress": user.get("emailAddress")
            }
            print(f"Debugging Log - user info from Get_User_Info: {user_info}")
            return user_info
        else: 
            print("No users found in the response.")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user info: {e}")
        return None

    # Old
    # try:
    #     response = requests.post(url, json=payload, headers=headers)
    #     response.raise_for_status()
    #     data = response.json()

    #     if data.get("users"):
    #         user = data["users"][0]
    #         user_info = {
    #             "user_id": user.get("hashId"),
    #             "userName": user.get("userName"),
    #             "firstName": user.get("firstName"),
    #             "lastName": user.get("lastName"),
    #             "emailAddress": user.get("emailAddress")
    #         }
    #         print(f"Debugging Log - user info from Get_User_Info: {user_info}")
    #         return user_info
    #     else: 
    #         return None
        
    # except requests.exceptions.RequestException as e:
    #     print(f"Error fetching user info: {e}")
    #     return None

def add_member_to_group(userId):
    group_id = "121561"
    url = f"https://api.quickbase.com/v1/groups/{group_id}/members"
    headers = {
        "Authorization": f"QB-USER-TOKEN {user_token}",
        "User-Agent": "Wedding Smash User Provisioner",
        "QB-Realm-Hostname": realm,
        "Content-Type": "application/json"
    }
    payload = [userId]

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        successfullyAddedUserIds =  data.get("success", []) # this is an array
        if userId in successfullyAddedUserIds:
            return True
        else: 
            return False
        
    except requests.exceptions.RequestException as e:
        print(f"Error adding user to group: {e}")
        return None
