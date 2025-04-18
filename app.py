# app.py
from flask import Flask
from flask_cors import CORS

from routes.add_user import add_user_api

app = Flask(__name__)

# Apply CORS to specific origins for the whole app
CORS(app, resources={r"/*": {"origins": "https://quincy.quickbase.com"}})

app.register_blueprint(add_user_api)