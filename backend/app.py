from flask import Flask
from flask_cors import CORS

from controller.images import images_bp
from settings import BaseConfig
from util.logger import get_log_handler

app = Flask(__name__)


def create_app():
    app.register_blueprint(images_bp)

    app.config.from_object("settings.BaseConfig")

    app.logger.addHandler(get_log_handler(BaseConfig.LOGGING_PATH))

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.run(host="0.0.0.0", port=5001)


if __name__ == '__main__':
    create_app()
else:
    application = app
