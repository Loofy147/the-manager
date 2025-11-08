import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from flask_jwt_extended import JWTManager
from src.routes.role import role_bp
from src.routes.project import project_bp
from src.routes.contract import contract_bp
from src.routes.ai_model import ai_model_bp
from src.config import Config
from src.logging import configure_logging
from src.errors import register_error_handlers
import structlog
from flask import request

configure_logging()
logger = structlog.get_logger()

def create_app(config_object=Config):
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    app.config.from_object(config_object)

    # Enable CORS for all routes
    CORS(app, origins="*")

    JWTManager(app)

    register_error_handlers(app)

    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(role_bp, url_prefix='/api')
    app.register_blueprint(project_bp, url_prefix='/api')
    app.register_blueprint(contract_bp, url_prefix='/api')
    app.register_blueprint(ai_model_bp, url_prefix='/api')

    db.init_app(app)

    # Import all models to ensure they are registered
    from src.models.role import Role, UserRole
    from src.models.project import Project, Task, ProjectTeam
    from src.models.contract import Contract, Cost, Budget
    from src.models.ai_model import AIModel, Dataset, Report, Metrics

    with app.app_context():
        db.create_all()

    @app.before_request
    def log_request():
        logger.info(
            "request",
            method=request.method,
            path=request.path,
            remote_addr=request.remote_addr,
            headers=dict(request.headers),
        )

    @app.route('/', defaults={'path': ''})
    @app.route('/healthz')
    def healthz():
        return "OK"

    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if static_folder_path is None:
                return "Static folder not configured", 404

        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "index.html not found", 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
