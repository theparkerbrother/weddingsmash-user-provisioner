# app.py

from flask import Flask
from routes.add_user import add_user_api

app = Flask(__name__)
app.register_blueprint(add_user_api)