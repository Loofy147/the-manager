from flask import jsonify
import structlog
from functools import wraps

logger = structlog.get_logger()

class HttpException(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except HttpException as e:
            logger.error("http_exception", status_code=e.status_code, message=e.message)
            response = {"error": e.message}
            return jsonify(response), e.status_code
        except Exception as e:
            logger.exception("unhandled_exception", exc_info=e)
            response = {
                "error": "Internal Server Error",
                "message": "An unexpected error occurred. Please try again later."
            }
            return jsonify(response), 500
    return decorated_function

def register_error_handlers(app):
    @app.errorhandler(404)
    def handle_not_found(e):
        logger.error("not_found", path=request.path)
        response = {"error": "Not Found"}
        return jsonify(response), 404
