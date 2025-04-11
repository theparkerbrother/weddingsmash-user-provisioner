# app.py

from flask import Flask
from routes.quickbase import api as quickbase_api

app = Flask(__name__)
app.register_blueprint(quickbase_api)

