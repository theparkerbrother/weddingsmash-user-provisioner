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

def send_invitation_xml(userId, companyName):
    # XML payload for the API request
    xml_payload = f"""
    <qdbapi>
        <usertoken>{smash_magic_user_token}</usertoken>
        <userid>{userId}</userid>
        <usertext>Welcome to Wedding Smash!\n\nThis is the application you will use for your work with {companyName}.\n\nClick the "GO TO THIS APP IN QUICKBASE" button below to register your account.\n\nTo register you will need to:\n1. Set up your password AND\n2. Set up your secret questions (these will be used if you ever need to reset your password).\n\nView a demo of the app by following the link below.\nhttps://vimeo.com/1077772545/ac872cfd05</usertext>
    </qdbapi>
    """.strip()

    url = f"https://{realm}/db/{app_id}"
    headers = {
        "Content-Type": "application/xml",
        "QUICKBASE-ACTION": "API_SendInvitation"
    }

    try:
        response = requests.post(url, data=xml_payload, headers=headers)
        response.raise_for_status()

        json_response = convert_xml_to_dict(response.text)
        qdbapi = json_response.get("qdbapi", {})
        errcode = qdbapi.get("errcode")
        errtext = qdbapi.get("errtext")

        if errcode == "0":
            print("✅ Invitation sent")
            return True
        else:
            print("❌ Error occurred while sending invitation.")
            print("Error Code:", errcode)
            print("Error Text:", errtext)
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Network or HTTP error while sending invitation: {e}")
        return None