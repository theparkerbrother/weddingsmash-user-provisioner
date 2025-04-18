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

def update_contractor_record(contractorId, email):
    url = "https://api.quickbase.com/v1/records"
    headers = {
        "Authorization": f"QB-USER-TOKEN {smash_magic_user_token}",
        "QB-Realm-Hostname": realm,
        "Content-Type": "application/json"
    }
    payload = {
        "to": contractor_table_id,
        "data": [
            {
                "3": {"value": contractorId},     # Record ID field
                "321": {"value": email},          # Team Member User field
            }
        ],
        "fieldsToReturn": [321]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        print("Raw response text from Quickbase:", response.text)
        response_json = response.json()
        print("Parsed JSON response from Quickbase:", response_json)

        metadata = response_json.get("metadata", {})
        updated = metadata.get("updatedRecordIds", [])

        if updated and updated[0] == contractorId:
            return "Team Member User field Updated"
        else:
            return "No update required"

    except requests.exceptions.RequestException as e:
        print(f"❌ Error updating contractor record: {e}")
        return "error"
