# middlewares.py
import time
import logging
from flask import request

# Set up a logger specifically for middleware
logger = logging.getLogger("middlewares")

def register_middlewares(app):
    @app.before_request
    def log_request_info():
        logger.info("Incoming request: %s %s", request.method, request.path)
        logger.debug("Headers: %s", dict(request.headers))
        if request.is_json:
            try:
                logger.debug("Request JSON: %s", request.get_json())
            except Exception:
                logger.debug("Request body could not be parsed as JSON.")

    @app.before_request
    def start_timer():
        request.start_time = time.time()

    @app.after_request
    def log_response_time(response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(
                "Request to %s completed in %.4f seconds with status %s",
                request.path,
                duration,
                response.status_code
            )
        return response
