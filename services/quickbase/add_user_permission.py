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

def add_user_permission(userEmail,companyId):
    url = f"https://api.quickbase.com/v1/records"
    headers = {
        "Authorization": f"QB-USER-TOKEN {smash_magic_user_token}",
        "QB-Realm-Hostname": realm,
        "Content-Type": "application/json"
    }
    payload = {
        "to": f"{user_permission_table_id}",
        "data": [
            {
                "6": {
                    "value": f"{userEmail}"
                },
                "11": {
                    "value": 1
                },
                "7": {
                    "value": companyId
                },
                "14": {
                    "value": "Contractor"
                }
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        print("Raw response text from Quickbase:", response.text)  # raw response
        data = response.json()
        print("Parsed JSON response from Quickbase:", data)        # parsed JSON

        response_json = response.json()  # or however you get the response dictionary

        metadata = response_json.get("metadata", {})

        created = metadata.get("createdRecordIds", [])
        updated = metadata.get("updatedRecordIds", [])
        unchanged = metadata.get("unchangedRecordIds", [])

        # Now you can check if anything succeeded:
        if created or updated or unchanged:
            print("✅ Success!")
            print("User Permission Created:", created)
            print("User Permission Updated:", updated)
            print("User Permission Unchanged:", unchanged)
            return True
        else:
            print("❌ Error adding User Permission Record.")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"Error adding User Permission record: {e}")
        return None