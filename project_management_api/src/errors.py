from flask import jsonify
import structlog

logger = structlog.get_logger()

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.exception("unhandled_exception", exc_info=e)
        response = {
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later."
        }
        return jsonify(response), 500
