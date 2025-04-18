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

def update_contractor_record(contractorId, userId):
    url = "https://api.quickbase.com/v1/records"
    headers = {
        "Authorization": f"QB-USER-TOKEN {smash_magic_user_token}",
        "QB-Realm-Hostname": realm,
        "Content-Type": "application/json"
    }
    payload = {
        "to": user_table_id,
        "data": [
            {
                "6": {"value": userEmail},
                "7": {"value": companyId},
                "15": {"value": "Contractor"}
            }
        ],
        "fieldsToReturn": [52]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        print("Raw response text from Quickbase:", response.text)
        response_json = response.json()
        print("Parsed JSON response from Quickbase:", response_json)

        metadata = response_json.get("metadata", {})
        record_data = response_json.get("data", [{}])[0]

        created = metadata.get("createdRecordIds", [])
        updated = metadata.get("updatedRecordIds", [])
        unchanged = metadata.get("unchangedRecordIds", [])

        permissionRecordExists = record_data.get("52", {}).get("value")

        if created or updated or unchanged:
            print("✅ Success!")
            print("User Record Created:", created)
            print("User Record Updated:", updated)
            print("User Record Unchanged:", unchanged)
            return {
                "userRecordSuccess": True,
                "permissionRecordExists": permissionRecordExists
            }
        else:
            print("❌ No changes were made to the user record.")
            return {
                "userRecordSuccess": False,
                "permissionRecordExists": permissionRecordExists
            }

    except requests.exceptions.RequestException as e:
        print(f"❌ Error adding User record: {e}")
        return {
            "userRecordSuccess": False,
            "permissionRecordExists": None
        }
