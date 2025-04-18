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