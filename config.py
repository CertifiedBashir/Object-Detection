import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()


def _db_url() -> str:
    user     = os.getenv('DB_USER',     'root')
    password = quote_plus(os.getenv('DB_PASSWORD', ''))
    host     = os.getenv('DB_HOST',     'localhost')
    port     = os.getenv('DB_PORT',     '3306')
    name     = os.getenv('DB_NAME',     'object_detection_db')
    return f'mysql+pymysql://{user}:{password}@{host}:{port}/{name}'


class Config:
    SECRET_KEY                  = os.getenv('SECRET_KEY', 'change-me')
    SQLALCHEMY_DATABASE_URI     = _db_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH          = 16 * 1024 * 1024   # 16 MB upload limit


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
    'default':     DevelopmentConfig,
}
