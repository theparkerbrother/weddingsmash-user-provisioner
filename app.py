# app.py
from flask import Flask
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
from middlewares import register_middlewares

from routes.add_user import add_user_api
from routes.remove_user import remove_user_api

# Set up logging - rotate file logging - console logging
log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
log_handler = RotatingFileHandler('logs/server.log', maxBytes=5_000_000, backupCount=5)
log_handler.setFormatter(log_formatter)

# Set up the root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

# Create the Flask app
app = Flask(__name__)

# Apply CORS to specific origins for the whole app
CORS(app, resources={r"/*": {"origins": "https://quincy.quickbase.com"}})

# Register middlewares for request logging and response timing
register_middlewares(app)

# Register blueprints (routes)
app.register_blueprint(add_user_api)
app.register_blueprint(remove_user_api)