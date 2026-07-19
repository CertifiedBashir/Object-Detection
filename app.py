import io
import os
import sys
from flask import Flask
from dotenv import load_dotenv

# Force UTF-8 on Windows so EasyOCR's Unicode progress-bar characters
# (e.g. █ U+2588) don't crash with 'charmap' codec errors.
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from extensions import db, migrate
from config import config

load_dotenv()


def create_app(config_name: str = None) -> Flask:
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so Flask-Migrate / Alembic detects them
    from model import image_model, text_to_image_model  # noqa: F401

    from route.main_routes import bp
    app.register_blueprint(bp)

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(debug=True)
