import os
from flask import Request

def is_valid_request(req: Request) -> bool:
    expected_key = os.getenv("PIPELINE_API_KEY")
    provided_key = req.headers.get("X-API-KEY")
    return provided_key == expected_key