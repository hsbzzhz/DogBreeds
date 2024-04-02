from flask import Flask, request
from flask_cors import CORS

from app.controller.decision_tree import decision_bp
from app.utils.logger import getLogHandler
from settings import BaseConfig


def create_app():
    app = Flask(__name__)
    app.register_blueprint(decision_bp)

    app.config.from_object("settings.BaseConfig")

    app.logger.addHandler(getLogHandler(BaseConfig.LOGGING_PATH))

    @app.before_request
    def before_request():
        app.logger.info(request.method + ' ' + request.url)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.run(host="0.0.0.0", port=5001)


if __name__ == '__main__':
    create_app()
