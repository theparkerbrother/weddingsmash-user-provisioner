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