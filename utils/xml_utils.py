import xmltodict
import json
import xml.etree.ElementTree as ET

def convert_xml_to_dict(xml_data):
    """Convert XML data to a Python dictionary."""
    try:
        # Parse the XML data into a Python dictionary
        xml_dict = xmltodict.parse(xml_data)
        
        return xml_dict  # Return the dictionary directly
        
    except Exception as e:
        print(f"Error converting XML to DICT: {e}")
        return None


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