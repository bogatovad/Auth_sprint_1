import os
from dotenv import load_dotenv

load_dotenv

class Config(object):
    DEBUG = False

    CSRF_ENABLED = True

    SECRET_KEY = 'YOUR_RANDOM_SECRET_KEY'

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True