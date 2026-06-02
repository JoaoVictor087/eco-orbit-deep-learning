from flask import Flask
from api.config import Config
from api.routes.predict_route import predict_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(predict_bp, url_prefix='/api/v1')

    @app.route('/health', methods=['GET'])
    def health_check():
        return {"status": "online", "service": "eco-orbit-ai"}, 200
    return app