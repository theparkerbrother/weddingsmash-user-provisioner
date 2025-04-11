# services/quickbase.py

import os
import requests

import xml.etree.ElementTree as ET

def parse_user_info(xml_data):
    # Parse the XML response
    root = ET.fromstring(xml_data)
    
    # Extract data points and return them in a dictionary
    user_info = {
        "user_id": root.find(".//user").attrib["id"],
        "first_name": root.find(".//firstName").text,
        "last_name": root.find(".//lastName").text,
        "login": root.find(".//login").text,
        "email": root.find(".//email").text,
        "screen_name": root.find(".//screenName").text,
        "is_verified": root.find(".//isVerified").text,
        "external_auth": root.find(".//externalAuth").text,
    }
    return user_info

def get_user_info(email):
    # Get the user token from the environment variable
    user_token = os.getenv("QB_USER_TOKEN")

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

        user_info = parse_user_info(response.text)

        # Process the response here
        return user_info  # Or use `response.json()` if response is JSON
    except requests.exceptions.RequestException as e:
        # Handle errors in the request (e.g., network issues, bad response)
        print(f"Error occurred while getting user info: {e}")
        return None

